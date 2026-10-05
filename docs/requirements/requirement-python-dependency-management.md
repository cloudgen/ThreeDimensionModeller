**file**: docs/requirements/requirement-python-dependency-management.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-python-dependency-management`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file owns the **pip requirement strings** ThreeDimensionModeller declares. The machine copy is `pyproject.toml` `[project].dependencies`. The two lists are one set. Packaging law owns the manifest shape. Runtime-prerequisite law owns the fact that no host encoder is required. How status lines are written is `requirement-python-cli-logging`. The model build is `requirement-domain-threedimensionmodeller`.

The status library floor is `ChronicleLogger>=1.3.1`, required, not optional. The vision stack is numpy, the headless OpenCV wheel, and scikit-image. Each of those entries has a version floor. The text menu is drawn by this package, so it is not a pip wheel.

### 1.1 Human-facing

**In one sentence:** Before a model or a status log can run, pip must be able to install ChronicleLogger at least 1.3.1, numpy at least 2.3.0, opencv-python-headless at least 5.0.0.93, and scikit-image at least 0.25.0, as written in `pyproject.toml`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Install the declared wheels with pip | `python -m pip install ThreeDimensionModeller` |
| The other role | The manifest that lists those strings | `pyproject.toml` |
| Not this file | The menu picture and the outline steps | TUI and the domain file |

| Includes | Excludes |
|----------|----------|
| Version floors for ChronicleLogger and the image stack | A host encoder, a GUI OpenCV wheel, and a pip wheel for the text menu |
| One list shared by the manifest and this file | A second `requirements.txt` authority |

| Surface | What you open | What for |
|---------|---------------|----------|
| `pyproject.toml` | `[project].dependencies` | The live strings |
| `three-dimension-modeller` | console script | Uses those libraries after install |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install the package | You get the status logger and the image stack. An empty folder still does not import the image stack. | `python -m pip install ThreeDimensionModeller` |
| Install the vision wheel | Outlines import `cv2` from the headless build. That build does not open a window. | `python -m pip install 'opencv-python-headless>=5.0.0.93'` |

## 2. Core Rules (Mandatory)

1. **MUST** declare runtime pip libraries only in `pyproject.toml` `[project].dependencies`.
2. **MUST** attach a PEP 440 version specifier to every entry. A bare name is not a declaration.
3. **MUST** keep the strings in Implementation Notes identical to that list.
4. **MUST** use the headless OpenCV wheel for silhouette masks. **MUST NOT** declare the GUI wheel `opencv-python`.
5. **MUST NOT** declare a menu distribution. The text menu is painted by this package (`requirement-python-tui`, class `MenuPainter`).
6. **MUST** keep the status-log floor at ChronicleLogger 1.3.1. It **MUST NOT** be optional. That is the release `requirement-python-cli-logging` consumes.
7. **MUST NOT** declare FFmpeg, or any other host encoder, as a pip package.
8. **MUST NOT** install operating-system packages, and **MUST NOT** use admin privilege, to satisfy these strings.
9. **MUST NOT** add `requirements.txt` as a second authority.

### 2.1 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Status-log spec** | `ChronicleLogger>=1.3.1` |
| **Array spec** | `numpy>=2.3.0` |
| **Vision spec** | `opencv-python-headless>=5.0.0.93` |
| **Mesh spec** | `scikit-image>=0.25.0` |
| **Menu distribution** | Not declared. Painter is class `MenuPainter` |
| **GUI build forbidden** | `opencv-python` is not declared |
| **Host encoder** | Not declared. Not required |
| **Manifest** | `pyproject.toml` `[project].dependencies` |
| **Why this logger floor** | 1.3.1 is the ChronicleLogger release whose `logname`, `logName`, `baseDir`, `isDebug`, and `log_message` match `requirement-python-cli-logging` |
| **Why these vision floors** | `opencv-python-headless` 5.0.0.93 imports `cv2` with `findContours`, `threshold`, `morphologyEx`, and `floodFill`, and it does not open a window. `scikit-image>=0.25.0` provides `skimage.measure.marching_cubes`. The build imports `numpy` itself. Pillow and rembg are not declared |
| **Empty folder** | A folder with no supported image returns 0 and does not import this image stack (`requirement-domain-threedimensionmodeller`) |

### 2.2 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT**: One manifest and one law file for the pip strings.
- **Principle 2 – Intentional**: The logger floor is required. The vision wheel is the headless build.
- **Principle 1 – Caution**: A bare name can install a GUI build that needs a window library.
- **Principle 10 – Least privilege**: pip as this login; no root package install.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, these wheels stay a normal-user pip install. **This requirement:** do not satisfy `ChronicleLogger>=1.3.1`, `numpy>=2.3.0`, `opencv-python-headless>=5.0.0.93`, or `scikit-image>=0.25.0` with admin privilege, a system package manager, or `sudo pip`.

## Sample code

```toml
[project]
dependencies = [
    "ChronicleLogger>=1.3.1",
    "numpy>=2.3.0",
    "opencv-python-headless>=5.0.0.93",
    "scikit-image>=0.25.0",
]
```

`opencv-python` is not in this list. There is no menu wheel. There is no encoder package.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Pin the vision wheel that imports without opening a window.
- **Intentional:** The text menu stays in this package. ChronicleLogger stays required.
- **Anti-fragile:** Headless OpenCV does not depend on a GL library.
- **Over-protect:** Tests read the manifest and the strings in this file.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Drop the version specifier from any dependency.
2. Replace `opencv-python-headless` with `opencv-python` while outlines only draw on a canvas.
3. Add a menu distribution while the painter is class `MenuPainter` in this package.
4. Lower the ChronicleLogger floor below 1.3.1, or mark that library optional, while status lines use `log_message`.
5. Add FFmpeg or another encoder as a pip dependency.
6. Add a root installer for these libraries.
7. Leave this file’s strings different from `pyproject.toml`.
8. Put the pip strings back into packaging or runtime as a second authority.

**Violating this rule is a dependency-honesty regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `opencv-python-headless>=5.0.0.93` is a dependency |
| AC-2 | No menu distribution is declared |
| AC-3 | `ChronicleLogger>=1.3.1` is a required dependency |
| AC-4 | No dependency entry lacks a version specifier |
| AC-5 | `opencv-python` is not a dependency |
| AC-6 | `numpy>=2.3.0`, `opencv-python-headless>=5.0.0.93`, and `scikit-image>=0.25.0` are dependencies |
| AC-7 | This file and `pyproject.toml` list the same four strings |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `docs/requirements/index.md` | Registry |
| `requirement-python-packaging` | Manifest shape; points here for the strings |
| `requirement-runtime-prerequisites` | No host encoder; pip strings point here |
| `requirement-python-tui` | Menu writer in this package; no menu wheel here |
| `requirement-python-cli-logging` | Status logger that needs the ChronicleLogger floor |
| `requirement-domain-threedimensionmodeller` | The model build that imports the image stack |
| `requirement-class-software-dev` | Residual points here |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-DEP-01** | `tests/test_dependencies.py` | have | Every manifest entry has a version specifier. The four strings are the list |
| **TP-DEP-02** | `tests/test_dependencies.py` | have | Headless wheel; GUI wheel `opencv-python` absent |
| **TP-DEP-03** | `tests/test_dependencies.py` | have | This file matches the manifest |
| **TP-DEP-04** | `tests/test_dependencies.py` | have | Installed wheels meet the floors when present. A missing wheel does not fail the case |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-05 | Active 1.0.0 | Pip strings for ThreeDimensionModeller 1.0.0. Logger floor `ChronicleLogger>=1.3.1`. Build floors `numpy>=2.3.0`, `opencv-python-headless>=5.0.0.93`, `scikit-image>=0.25.0`. Pillow and rembg are not declared. No GUI wheel. No menu wheel. No encoder package |

---

**Last Updated**: 2026-10-05
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
