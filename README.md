# Cobble Skies — packwiz-репозиторій

Cobblemon × Create: Aeronautics, NeoForge 1.21.1. Звідси Modrinth App автоматично підтягує оновлення збірки при кожному запуску гри.

Адреса для автооновлення: `https://raw.githubusercontent.com/AlCaOV/cobble-skies/main/pack.toml`

## Як приєднатися (для друзів)

1. Встанови **Modrinth App** і імпортуй файл `Cobble-Skies-1.9.0.mrpack` (Create profile → From file). Виділи грі 8 ГБ пам'яті.
2. Відкрий профіль → **Options → Hooks** → у поле **Pre-launch** встав:
   ```
   cmd /c update.bat
   ```
3. У профілі перевір версію NeoForge — має бути **21.1.264** (Settings → Loader version). Автооновлення моди підтягує, а версію завантажувача — ні.
4. Запускай гру. Перед кожним стартом `update.bat` звіряє моди/конфіги з цим репозиторієм і докачує лише те, що змінилось. Журнал — у файлі `update.log` у папці профілю.

Якщо хочеш оновити вручну — просто двічі клацни `update.bat` у папці профілю.

## Як випускати нову версію 

1. Збери нову `.mrpack` як завжди (або додай моди командами `packwiz modrinth add <slug>` — тоді крок 2 пропусти).
2. Перегенеруй репозиторій зі збірки:
   ```
   python gen.py Cobble-Skies-1.9.0.mrpack . 1.8.0
   ```
   Скрипт перепише `pack.toml`, `index.toml`, `*.pw.toml` та файли з `overrides/`, не чіпаючи `README.md`, `installer/` і `.git`.
3. `git add -A && git commit -m "1.8.0" && git push`

Після push усі гравці отримають зміни при наступному запуску гри.

## Структура

- `pack.toml` — метадані збірки, версії Minecraft/NeoForge, хеш індексу.
- `index.toml` — список усіх файлів із хешами. `options.txt` позначено `preserve = true`, тому особисті налаштування гравців не перезаписуються.
- `mods/`, `resourcepacks/`, `shaderpacks/`, `config/openloader/packs/` — `*.pw.toml` метафайли, що вказують на Modrinth CDN.
- `mods/CRE-v0.0.3-NeoForge.jar` — пропатчений Cobblemon Ride Expansion (лежить тут, бо на Modrinth такої збірки немає).
- `mods/thaumaturge-1.21.1-NeoForge-1.0.4.jar`, `mods/create_thaumaturgy-1.21.1-0.1.0.jar` — 1.21.1-збірки Thaumaturge (з Discord розробників) і Create: Thaumaturgy (CurseForge); на Modrinth їх немає.
- `config/` — конфіги, які мають бути однакові в усіх.
- `installer/` — `packwiz-installer-bootstrap.jar` і `update.bat`, ті самі, що вкладені в базовий `.mrpack`.
