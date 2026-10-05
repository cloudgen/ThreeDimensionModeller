# ThreeDimensionModeller - A glTF model and an HTML viewer from outline images

![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
[![CIAO](https://img.shields.io/badge/Philosophy-CIAO%20(Caution%20%E2%80%A2%20Intentional%20%E2%80%A2%20Anti--fragile%20%E2%80%A2%20Over--engineered)-purple.svg)](https://github.com/cloudgen/ciao)
[![Stars](https://img.shields.io/github/stars/cloudgen/ThreeDimensionModeller?style=flat-square)](https://github.com/cloudgen/ThreeDimensionModeller)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)]()
[![PyPI](https://img.shields.io/pypi/v/ThreeDimensionModeller?style=flat-square)](https://pypi.org/project/ThreeDimensionModeller/)

ThreeDimensionModeller builds one glTF model and one HTML viewer from outline images in a folder. The files are `model.glb` and `viewer.html`. Supported inputs are webp, png, jpg, and jpeg.

On a terminal, starting it with no arguments opens a text menu. The menu does not convert images by itself, and it does not call pip.

The sample conversion is [`sample-images/model/viewer.html`](https://cloudgen.github.io/ThreeDimensionModeller/sample-images/model/viewer.html). The picture is that page. The picture address is absolute, so the package index and GitHub both show it.

[![Converted model in the HTML viewer](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/model-viewer.png)](https://cloudgen.github.io/ThreeDimensionModeller/sample-images/model/viewer.html)

## Features

- Text menu on a terminal: **model**, **system-log**, **language**, **self-management**, and **Exit**
- The first row shows the current folder and a local clock (`HH:MM:SS`) when the row has room
- Numbered rows line up. A rounded input box sits along the bottom, as wide as the terminal, with the name and version on the status line under the box
- **model** (1) lists **1** current folder, each subfolder, and **0** back. The chosen folder becomes one 3D model
- The typed verb `model` builds that model in the terminal and does not draw the menu. With no folder, it uses the current directory
- **system-log** (3) opens view-log, clear-log, and log-folder. **language** (4) picks the menu language. **self-management** (8) opens version, about, and the pip lifecycle rows
- Console script `three-dimension-modeller` and module entry `python -m ThreeDimensionModeller`
- Typed verbs: `help`, `version`, `about`, `model`, `self-install`, `version-check`, `self-update`, `self-uninstall`
- Checkout script `./convert.py` runs the same conversion

## Advantages

1. **A folder of outlines in, one model out.** `three-dimension-modeller model` builds a model from outline images in the current directory and does not draw the menu. On the menu, row **1 model** asks for the current folder or a subfolder, then writes `model.glb` and `viewer.html` in that folder's `model` directory. With no arguments on a terminal, the text menu opens and waits. With no terminal and no verb, the program prints help and returns 0. There is no `--json`.
2. **Built-in languages.** Row **4** lists thirteen languages: English, Simplified Chinese, Traditional Chinese, Spanish, Arabic, French, Portuguese, Russian, German, Japanese, Korean, Dutch, and Greek. The choice is saved for the next run. The note on row 1 follows the menu language.
3. **Lifecycle and diagnostics.** `version-check`, `self-update`, `self-install`, and `self-uninstall` are menu rows **84**–**87** and typed verbs. `self-uninstall` on the command line needs `--force`. They call pip and do not use root. **system-log** (**3**) views a log, clears a log, and shows the log folder. **about** (**83**) stays in English.

## Quick Installation

**Python dependencies:** `ChronicleLogger>=1.3.1`, `numpy>=2.3.0`, `opencv-python-headless>=5.0.0.93`, and `scikit-image>=0.25.0` (required). Pip installs them with ThreeDimensionModeller. The inputs are outline images already drawn. No model download and no external media tool are required.

### PyPI (registry)

```bash
pip install ThreeDimensionModeller
```

This installs the console entry **`three-dimension-modeller`** and the package **`ThreeDimensionModeller`**. Packaging name SSOT is `pyproject.toml` `[project].name` = `ThreeDimensionModeller`. This tree is **1.0.0**. The PyPI badge above shows the live index.

### Local install (checkout)

From a checkout (editable / unreleased work):

```bash
git clone https://github.com/cloudgen/ThreeDimensionModeller.git
cd ThreeDimensionModeller
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e .
```

### Main menu

After install, on a terminal, `three-dimension-modeller` with no arguments prints this screen. The verb is bold and the note after the colon is italic. `9` leaves. `0` on a submenu goes back. After a command finishes, the main menu is shown again. A number that is not on the list prints an error and lets you choose again.

Picture of the English menu. Current directory `/tmp/clips`. The rows are the text the menu paints. The frame is the 80-column box.

```text
$ three-dimension-modeller
Path: /tmp/clips                                                       12:06:45

1. **model**          : *build a 3D model from outline images in a chosen folder*
3. **system-log**     : *view, clear, and the log folder*
4. **language**       : *display language for this menu*
8. **self-management**: *version, about, and pip lifecycle*
9. **Exit**           : *leave*




╭─────────────────────────────────────────────────────────────────────────────╮
│ >                                                                           │
╰─────────────────────────────────────────────────────────────────────────────╯
  ThreeDimensionModeller 1.0.0  │  main menu  │  Up/Down  •  Enter
```

**system-log** (3):

```text
Path: /tmp/clips                                                       12:06:45

31. **view-log**  : *list a log file and show it*
32. **clear-log** : *empty one log file*
33. **log-folder**: *show the log folder*
 0. **Back**      : *return to the main menu*




╭─────────────────────────────────────────────────────────────────────────────╮
│ >                                                                           │
╰─────────────────────────────────────────────────────────────────────────────╯
  ThreeDimensionModeller 1.0.0  │  system-log  │  Up/Down  •  Enter
```

**language** (4). The short on each language row is that language’s own name. Numbers 40 and 54–59 are not printed. `0` goes back and does not save.

```text
Path: /tmp/clips                                                       12:06:46

41. **English**   : *use English for this menu*
42. **简体中文**      : *use 简体中文 for this menu*
43. **繁體中文**      : *use 繁體中文 for this menu*
44. **Español**   : *use Español for this menu*
45. **العربية**   : *use العربية for this menu*
46. **Français**  : *use Français for this menu*
47. **Português** : *use Português for this menu*
48. **Русский**   : *use Русский for this menu*
49. **Deutsch**   : *use Deutsch for this menu*
50. **日本語**       : *use 日本語 for this menu*
51. **한국어**       : *use 한국어 for this menu*
52. **Nederlands**: *use Nederlands for this menu*
53. **Ελληνικά**  : *use Ελληνικά for this menu*
 0. **Back**      : *return to the main menu*

╭─────────────────────────────────────────────────────────────────────────────╮
│ >                                                                           │
╰─────────────────────────────────────────────────────────────────────────────╯
  ThreeDimensionModeller 1.0.0  │  language  │  Up/Down  •  Enter
```

**self-management** (8):

```text
Path: /tmp/clips                                                       14:05:09

82. **version**       : *show the installed version*
83. **about**         : *version and this computer*
84. **version-check** : *compare this install with pip*
85. **self-update**   : *upgrade this package with pip*
86. **self-uninstall**: *remove this package with pip*
87. **self-install**  : *install this package with pip*
 0. **Back**          : *return to the main menu*

╭─────────────────────────────────────────────────────────────────────────────╮
│ >                                                                           │
╰─────────────────────────────────────────────────────────────────────────────╯
  ThreeDimensionModeller 1.0.0  │  self-management  │  Up/Down  •  Enter
```

Choose a number, or type the command name in the box. The block caret appears in that box while it is focused.

## Usage

```bash
three-dimension-modeller
# or
python -m ThreeDimensionModeller
```

On a terminal, that opens the main menu above. It does not build a model yet, and it does not call pip. With no terminal, the same command prints help and returns 0.

**model** (1) opens a folder list: **1** current folder, then each subfolder, and **0** back. The chosen folder is built into `model.glb` and `viewer.html`. By default those files go in that folder's `model` directory. A `views.json` in the folder, or `--views`, names each outline with azimuth and elevation in degrees. `--grid` sets the voxel count on each axis (16 to 160, default 96). Any key on the result page returns to the main menu. The typed verb builds the model in the terminal and does not draw the menu:

```bash
three-dimension-modeller model
three-dimension-modeller model photos --views views.json --grid 96
three-dimension-modeller model --output photos/built
```

```bash
three-dimension-modeller help
three-dimension-modeller version
three-dimension-modeller about
three-dimension-modeller model
three-dimension-modeller version-check
three-dimension-modeller self-update
three-dimension-modeller self-install
three-dimension-modeller self-uninstall --force
```

`version` prints `ThreeDimensionModeller 1.0.0` and does not call pip. `about` shows one English page: the product identity, a host check of this computer, and a star box. It does not call pip. `model` uses the current directory when no folder is given and does not draw the menu. `help` prints usage.

`version-check` runs `python -m pip index versions ThreeDimensionModeller`. `self-update` runs `python -m pip install --upgrade ThreeDimensionModeller`. `self-install` runs `python -m pip install ThreeDimensionModeller`. `self-uninstall` runs `python -m pip uninstall -y ThreeDimensionModeller` and needs `--force` on the command line. Those pip verbs do not use sudo. Empty arguments do not install or update.

Exit codes: non-zero for an unknown verb, a missing folder, a bad views file, an empty visual hull, a pip failure, or a menu that cannot open. Menu **Exit** (9) returns 0. `model` returns 0 when the folder exists and the model is written. An empty folder returns 0 and does not load the vision stack.

Import for scripts (thin entry):

```python
from ThreeDimensionModeller import main
# interactive session; a terminal opens the text menu
```

## Screenshots

Each heading is the file name. The paragraph is what that picture shows: the words on the screen, the characters in the input box, or the scene. Package **1.0.0**. These pictures are captures of ThreeDimensionModeller. Row 1 is **model**. The folder board is `model-folder.png`. `model-viewer.png` is the converted model in `sample-images/model/viewer.html`, and that picture links to the viewer. The package index can fetch a picture only after that file is on the public `main` branch. Every picture address is an absolute `https` URL.

### `language-menu.png`

Row **4** has opened the language list. **41 English** is highlighted, with the note "use English for this menu." The other rows are **42 简体中文**, **43 繁體中文**, **44 Español**, **45 العربية**, **46 Français**, **47 Português**, **48 Русский**, **49 Deutsch**, **50 日本語**, **51 한국어**, **52 Nederlands**, and **53 Ελληνικά**. Each note says to use that language for this menu. **0 Back** says "return to the main menu." The path label is `Path`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `language`.

![Language list, 41 English highlighted](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/language-menu.png)

### `main-menu-en.png`

English main menu. There is no saved-language line above the box. The path label is `Path`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 model** is highlighted: "build a 3D model from outline images in a chosen folder." Then **3 system-log** "view, clear, and the log folder," **4 language** "display language for this menu," **8 self-management** "version, about, and pip lifecycle," and **9 Exit** "leave." The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `main menu`.

![English main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-en.png)

### `main-menu-zh-hans.png`

Simplified Chinese main menu. The line above the box says `菜单语言是简体中文`. The path label is `路径`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 model** is highlighted: "把所选文件夹中的轮廓图做成三维模型." **3** is `系统日志`, **4** is `语言`, **8** is `自我管理`, and **9** is `离开`. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `主菜单`.

![Simplified Chinese main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-zh-hans.png)

### `main-menu-zh-hant.png`

Traditional Chinese main menu. The line above the box says `選單語言是繁體中文`. The path label is `路徑`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 model** is highlighted: "把所選資料夾中的輪廓圖做成三維模型." **3** is `系統日誌`, **4** is `語言`, **8** is `自我管理`, and **9** is `離開`. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `主選單`.

![Traditional Chinese main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-zh-hant.png)

### `main-menu-es.png`

Spanish main menu. The line above the box says `El idioma del menú es español`. The path label is `Ruta`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 model** is highlighted: "construye un modelo 3D con los contornos de una carpeta elegida." **3** is `registro`, **4** is `idioma`, **8** is `autogestión`, and **9** is `Salir`. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `menú principal`.

![Spanish main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-es.png)

### `main-menu-ar.png`

Arabic main menu. The line above the box says `لغة القائمة هي العربية`. The path label is `المسار`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. The numbers stay on the left. Arabic words on each row are shaped and read right to left. **1 model** is highlighted and stays `model`: "يبني نموذجا ثلاثي الأبعاد من حدود المجلد المختار." **3** is `سجل النظام`, **4** is `لغة`, **8** is `إدارة ذاتية`, and **9** is `خروج`. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `القائمة الرئيسية`.

![Arabic main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-ar.png)

### `main-menu-fr.png`

French main menu. The line above the box says `La langue du menu est le français`. The path label is `Chemin`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 model** is highlighted and stays `model`: "construit un modèle 3D à partir des contours d'un dossier choisi." **3** is `journal`, **4** is `langue`, **8** is `autogestion`, and **9** is `Quitter`. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `menu principal`.

![French main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-fr.png)

### `main-menu-pt.png`

Portuguese main menu. The line above the box says `O idioma do menu é português`. The path label is `Caminho`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 model** is highlighted and stays `model`: "constrói um modelo 3D a partir dos contornos de uma pasta escolhida." **3** is `registo`, **4** is `idioma`, **8** is `autogestão`, and **9** is `Sair`. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `menu principal`.

![Portuguese main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-pt.png)

### `main-menu-ru.png`

Russian main menu. The line above the box says `Язык меню — русский`. The path label is `Путь`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 model** is highlighted and stays `model`: "собрать трёхмерную модель из контуров выбранной папки." **3** is `системный журнал`, **4** is `язык`, **8** is `самоуправление`, and **9** is `Выход`. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `главное меню`.

![Russian main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-ru.png)

### `main-menu-de.png`

German main menu. The line above the box says `Die Menüsprache ist Deutsch`. The path label is `Pfad`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 model** is highlighted and stays `model`: "aus Umrissen eines gewählten Ordners ein 3D-Modell bauen." **3** is `Systemprotokoll`, **4** is `Sprache`, **8** is `Selbstverwaltung`, and **9** is `Beenden`. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `Hauptmenü`.

![German main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-de.png)

### `main-menu-ja.png`

Japanese main menu. The line above the box says `メニューの言語は日本語`. The path label is `パス`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 model** is highlighted and stays `model`: "選んだフォルダの輪郭画像から3Dモデルを作る." **3** is `システムログ`, **4** is `言語`, **8** is `自己管理`, and **9** is `終了`. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `メインメニュー`.

![Japanese main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-ja.png)

### `main-menu-ko.png`

Korean main menu. The line above the box says `메뉴 언어는 한국어`. The path label is `경로`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 model** is highlighted and stays `model`: "고른 폴더의 윤곽 이미지로 3D 모델을 만듭니다." **3** is `시스템 로그`, **4** is `언어`, **8** is `자기관리`, and **9** is `종료`. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `주 메뉴`.

![Korean main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-ko.png)

### `main-menu-nl.png`

Dutch main menu. The line above the box says `De menutaal is Nederlands`. The path label is `Pad`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 model** is highlighted and stays `model`: "maak een 3D-model van contouren in een gekozen map." **3** is `systeemlog`, **4** is `taal`, **8** is `zelfbeheer`, and **9** is `Afsluiten`. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `hoofdmenu`.

![Dutch main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-nl.png)

### `main-menu-el.png`

Greek main menu. The line above the box says `Η γλώσσα του μενού είναι ελληνικά`. The path label is `Διαδρομή`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 model** is highlighted and stays `model`: "φτιάχνει ένα τρισδιάστατο μοντέλο από τα περιγράμματα ενός φακέλου." **3** is `αρχείο καταγραφής`, **4** is `γλώσσα`, **8** is `αυτοδιαχείριση`, and **9** is `Έξοδος`. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `κύριο μενού`.

![Greek main menu](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/main-menu-el.png)

### `model-folder.png`

The folder board for row **1**. The path label is `Path`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. **1 current** is highlighted: "build a 3D model from outline images in this folder." **2 photos** says "build a 3D model from outline images in this subfolder." **0 Back** says "return to the main menu." The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `model`.

![Folder board, current folder highlighted](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/model-folder.png)

### `self-management.png`

Row **8** has opened self-management. **82 version** is highlighted: "show the installed version." Then **83 about** "version and this computer", **84 version-check** "compare this install with pip", **85 self-update** "upgrade this package with pip", **86 self-uninstall** "remove this package with pip", **87 self-install** "install this package with pip", and **0 Back** "return to the main menu." The path label is `Path`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `self-management`.

![Self-management, 82 version highlighted](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/self-management.png)

### `tui-about.png`

**about** (83) on the result page. The title is `ThreeDimensionModeller (1.0.0) — result`. The page prints `ThreeDimensionModeller 1.0.0`, `Domain: Build a glTF model and an HTML viewer from outline images in a folder`, `Runtime tools: none`, and `Entry points: three-dimension-modeller, python -m ThreeDimensionModeller`. The host check is stamped `2026-10-05 17:48:52.787448` and headed `[CHECK SYSTEM]:`. Visible lines include Python 3.12.11, C Library GCC 13.3.0, Ubuntu 24.04.5 LTS, amd64, the current user, the shell `/bin/bash`, the Python executable `python3`, python2 location, python3 location, an empty conda location, pyenv location, `Inside docker container: False`, and `Cython String: cpython-312-x86_64-linux-gnu`. The footer says `Up/Down scrolls this page.` and `Press a key to return to the main menu.` There is no input box and no clock. The page stays in English.

![About host check, English](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/tui-about.png)

### `system-log.png`

Row **3** has opened system-log. **31 view-log** is highlighted: "list a log file and show it." Then **32 clear-log** "empty one log file", **33 log-folder** "show the log folder", and **0 Back** "return to the main menu." The path label is `Path`. The path is `/tmp/clips`. The clock is `17:48:52` on the right of that row. The input box shows `>` and no typed text. The status line says `ThreeDimensionModeller 1.0.0` and `system-log`.

![System log, 31 view-log highlighted](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/system-log.png)

### `model-viewer.png`

A capture of the converted model in `sample-images/model/viewer.html`. The page background is near black. The mesh is light gray and built from stacked outline slices: a wide upper mass, an opening through the middle, and a lower mass with a flat slab. The line at the bottom left reads "ThreeDimensionModeller — drag to orbit, wheel to zoom. model.glb is the glTF file." This is not a text-menu capture. The picture links to that viewer.

[![Converted model in the HTML viewer](https://raw.githubusercontent.com/cloudgen/ThreeDimensionModeller/main/screenshots/model-viewer.png)](https://cloudgen.github.io/ThreeDimensionModeller/sample-images/model/viewer.html)

## Examples

```bash
cd /path/to/folder/with/outline-images
three-dimension-modeller
```

```bash
three-dimension-modeller version
```

`version` prints `ThreeDimensionModeller 1.0.0` and does not call pip. A run that is not the text menu can also print ChronicleLogger status lines above that. The text menu keeps those lines off the screen.

```bash
three-dimension-modeller model --views views.json --grid 96
```

That builds `model/model.glb` and `model/viewer.html` from outline images in the current directory and does not draw the menu. On a terminal, row **1** asks for the current folder or a subfolder, then does the same build. `./convert.py` is the same build from a checkout. A views file lists each outline basename with azimuth and elevation in degrees. Without one, the outlines are spaced evenly around the object at elevation 0.

## Platform Compatibility

| Platform | Status |
|----------|--------|
| Linux | Primary; tested development path |
| macOS | Supported when CPython is on PATH |
| Windows | Supported when CPython is on PATH (venv activate differs) |
| Architectures | Any with CPython |

The text menu needs a terminal. With no terminal and no verb, the program prints help and returns 0. It does not wait.

## Related Projects

- [ThreeDimensionModeller on GitHub](https://github.com/cloudgen/ThreeDimensionModeller) — this program’s source
- [ThreeDimensionModeller on PyPI](https://pypi.org/project/ThreeDimensionModeller/) — this program on PyPI
- [OutlineImage on GitHub](https://github.com/cloudgen/OutlineImage) — writes a detailed outline image for each picture in a folder, and this program reads those images
- [OutlineImage on PyPI](https://pypi.org/project/OutlineImage/) — that program on PyPI
- [AnimeDlp](https://github.com/Wilgat/AnimeDlp) — command-line downloader for anime video sites
- [ChronicleLogger](https://github.com/Wilgat/ChronicleLogger) — status logger this program depends on (`ChronicleLogger>=1.3.1`)
- [VideoSpeed](https://github.com/Wilgat/VideoSpeed) — cuts, changes speed, and boomerangs a clip. That program is not this one
- [CIAO](https://github.com/cloudgen/ciao) — Caution, Intentional, Anti-fragile, Over-engineered
- [CIAO-Lite](https://github.com/cloudgen/ciao-lite) — short agent contract
- [safe-rm](https://github.com/cloudgen/safe-rm) — guarded `rm`

## Contributing

1. Keep product law under `docs/requirements/` in sync when behavior changes.
2. Prefer small, CIAO-safe changes. The model build lives in `src/ThreeDimensionModeller/model.py`. `./convert.py` calls that module.
3. Version dual SSOT: bump **`pyproject.toml`** and **`src/ThreeDimensionModeller/__init__.py`** `__version__` together.
4. Open issues and pull requests on GitHub.

## License

MIT — see [`LICENSE.md`](./LICENSE.md). Also declared in `pyproject.toml`.

## Last Update

2026-10-05 — **1.0.0** working tree: the package name is **ThreeDimensionModeller** and the console script is `three-dimension-modeller`. The public source is `https://github.com/cloudgen/ThreeDimensionModeller`. `model` builds `model.glb` and `viewer.html` from outline images in a folder. The default directory is that folder's `model`. Menu row 1 lists **1** current folder, each subfolder, and **0** back, then runs that build. `screenshots/model-viewer.png` is a capture of `sample-images/model/viewer.html`, and that picture links to the viewer. Picture addresses are absolute `https` URLs. Menu pictures are captures of this product, including the folder board. Version badge matches `pyproject.toml` and `__version__`. `ChronicleLogger>=1.3.1`, `numpy>=2.3.0`, `opencv-python-headless>=5.0.0.93`, and `scikit-image>=0.25.0` are required.
