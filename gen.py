"""Generate a packwiz repository from a Modrinth .mrpack (modrinth.index.json + overrides/)."""
import json, hashlib, os, re, shutil, sys, urllib.parse

SRC = sys.argv[1]          # unpacked mrpack dir OR .mrpack file
if SRC.endswith(".mrpack"):
    import zipfile, tempfile
    tmp = tempfile.mkdtemp(prefix="mrpack_")
    zipfile.ZipFile(SRC).extractall(tmp)
    SRC = tmp
OUT = sys.argv[2]          # packwiz repo dir
PACK_VERSION = sys.argv[3]

idx = json.load(open(os.path.join(SRC, "modrinth.index.json")))
KEEP = {".git", "README.md", "installer", "gen.py"}
if os.path.exists(OUT):
    for n in os.listdir(OUT):
        if n in KEEP: continue
        p = os.path.join(OUT, n)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
os.makedirs(OUT, exist_ok=True)

def toml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

def side_of(env):
    c = env.get("client", "required"); s = env.get("server", "required")
    if c != "unsupported" and s == "unsupported": return "client"
    if s != "unsupported" and c == "unsupported": return "server"
    return "both"

index_files = []  # (path, hash, metafile, preserve)

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

# 1. metafiles for every downloadable entry
for e in idx["files"]:
    path = e["path"]                       # e.g. mods/foo.jar
    url = e["downloads"][0]
    m = re.search(r"cdn\.modrinth\.com/data/([^/]+)/versions/([^/]+)/", url)
    folder, fname = os.path.split(path)
    stem = re.sub(r"\.(jar|zip)$", "", fname)
    meta_rel = os.path.join(folder, stem + ".pw.toml")
    name = stem
    lines = [
        f"name = {toml_str(name)}",
        f"filename = {toml_str(fname)}",
        f"side = {toml_str(side_of(e.get('env', {})))}",
        "",
        "[download]",
        f"url = {toml_str(url)}",
        'hash-format = "sha512"',
        f"hash = {toml_str(e['hashes']['sha512'])}",
    ]
    if m:
        lines += ["", "[update]", "[update.modrinth]",
                  f"mod-id = {toml_str(m.group(1))}",
                  f"version = {toml_str(m.group(2))}"]
    meta_abs = os.path.join(OUT, meta_rel)
    os.makedirs(os.path.dirname(meta_abs), exist_ok=True)
    with open(meta_abs, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    index_files.append((meta_rel.replace(os.sep, "/"), sha256_file(meta_abs), True, False))

# 2. overrides copied verbatim
ov = os.path.join(SRC, "overrides")
PRESERVE = {"options.txt"}
for root, _, files in os.walk(ov):
    for fn in files:
        src = os.path.join(root, fn)
        rel = os.path.relpath(src, ov).replace(os.sep, "/")
        dst = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        index_files.append((rel, sha256_file(dst), False, rel in PRESERVE))

# 3. index.toml
index_files.sort()
out = ['hash-format = "sha256"', ""]
for rel, h, meta, pres in index_files:
    out += ["[[files]]", f"file = {toml_str(rel)}", f"hash = {toml_str(h)}"]
    if meta: out.append("metafile = true")
    if pres: out.append("preserve = true")
    out.append("")
with open(os.path.join(OUT, "index.toml"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out))
ih = sha256_file(os.path.join(OUT, "index.toml"))

# 4. pack.toml
deps = idx["dependencies"]
pack = [
    f"name = {toml_str(idx['name'])}",
    'author = "Markiian"',
    f"version = {toml_str(PACK_VERSION)}",
    'pack-format = "packwiz:1.1.0"',
    "",
    "[index]",
    'file = "index.toml"',
    'hash-format = "sha256"',
    f"hash = {toml_str(ih)}",
    "",
    "[versions]",
    f"minecraft = {toml_str(deps['minecraft'])}",
    f"neoforge = {toml_str(deps['neoforge'])}",
    "",
]
with open(os.path.join(OUT, "pack.toml"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(pack))

print("metafiles:", sum(1 for x in index_files if x[2]), "plain files:", sum(1 for x in index_files if not x[2]))
