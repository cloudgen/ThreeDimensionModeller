# =============================================================================
# Outline images to a glTF model and an HTML viewer.
# requirement-domain-threedimensionmodeller — one folder in, model.glb and
# viewer.html in model/. ./convert.py calls convert_folder. The text menu
# and the model verb do too.
# The vision stack loads only when this folder has a supported image.
# A slow start shows its sentence before the work.
# requirement-domain-threedimensionmodeller — building the 3D model.
# =============================================================================
from __future__ import annotations

import argparse
import base64
import json
import os
import struct
import sys
from pathlib import Path


SUPPORTED_INPUT_EXTENSIONS = (".webp", ".png", ".jpg", ".jpeg")
OUTPUT_DIR_NAME = "model"
GLB_NAME = "model.glb"
VIEWER_NAME = "viewer.html"
DEFAULT_GRID = 96
MIN_GRID = 16
MAX_GRID = 160


def list_subfolders(folder):
    """General Purpose: Immediate child folders, hidden names omitted, sorted.

    Names are the directory entries. A missing folder yields an empty tuple.
    """
    place = Path(folder)
    try:
        names = [
            entry.name
            for entry in place.iterdir()
            if entry.is_dir() and entry.name and not entry.name.startswith(".")
        ]
    except OSError:
        return ()
    names.sort(key=str.lower)
    return tuple(names)


def list_images(folder):
    """General Purpose: Supported images in this folder. Subfolders are not scanned."""
    place = Path(folder)
    try:
        files = [
            entry
            for entry in place.iterdir()
            if entry.is_file() and entry.suffix.lower() in SUPPORTED_INPUT_EXTENSIONS
        ]
    except OSError:
        return ()
    files.sort(key=lambda item: item.name.lower())
    return tuple(files)


def folder_for_pick(name, place=None):
    """General Purpose: '.' is this folder. Any other token is one child name.

    A name with a separator, or '.' / '..', is refused.
    """
    root = Path(place if place is not None else os.getcwd()).expanduser().resolve()
    if name == ".":
        return root
    if (
        not name
        or name in (".", "..")
        or name != Path(name).name
        or "/" in name
        or "\\" in name
    ):
        raise ValueError(name)
    return root / name


def output_dir_for(folder):
    """General Purpose: The output folder next to the images being converted."""
    return Path(folder) / OUTPUT_DIR_NAME


def selected_choice_line(choice, process):
    """General Purpose: The one sentence shown before a slow process starts.

    requirement-domain-threedimensionmodeller owns the words. A function that
    returns the sentence is enough. This is not a module-level message constant.
    """
    return "{0} has been selected. {1} takes time to finish.".format(choice, process)


def _image_stack():
    """Import the vision stack once. The menu can list folders without it."""
    import cv2
    import numpy as np
    from skimage import measure

    return cv2, np, measure


def _read_views(path):
    """General Purpose: Azimuth and elevation rows from a views JSON file.

    A bare list or an object with a views array are both accepted.
    Each row needs file, azimuth, and elevation. file is one basename.
    """
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = raw.get("views") if isinstance(raw, dict) else raw
    if not isinstance(rows, list) or not rows:
        raise ValueError("views JSON needs a non-empty list")
    parsed = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each view must be an object")
        name = row.get("file")
        if not isinstance(name, str) or not name or name != Path(name).name:
            raise ValueError("view file must be a basename")
        if "/" in name or "\\" in name or name in (".", ".."):
            raise ValueError("view file must be a basename")
        parsed.append(
            {
                "file": name,
                "azimuth": float(row["azimuth"]),
                "elevation": float(row["elevation"]),
            }
        )
    return tuple(parsed)


def _equal_views(images):
    """General Purpose: Even azimuth steps at elevation 0, in name order."""
    count = len(images)
    if count == 0:
        return ()
    step = 360.0 / count
    return tuple(
        {"file": image.name, "azimuth": step * index, "elevation": 0.0}
        for index, image in enumerate(images)
    )


def outline_to_solid_mask(image_path, cv2, np):
    """General Purpose: Fill the area enclosed by the outer outline.

    A short close seals small gaps in the line. When that fill is empty,
    flood the outside from the corner and keep the interior.
    """
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("could not read image")
    _threshold, thresh = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    contours, _hierarchy = cv2.findContours(
        closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    mask = np.zeros_like(thresh)
    if contours:
        cv2.drawContours(mask, contours, -1, 255, thickness=cv2.FILLED)
    filled = int(np.count_nonzero(mask))
    height, width = mask.shape[:2]
    if filled < 50:
        flood = closed.copy()
        flood_mask = np.zeros((height + 2, width + 2), np.uint8)
        cv2.floodFill(flood, flood_mask, (0, 0), 128)
        interior = np.where(flood == 0, 255, 0).astype(np.uint8)
        if int(np.count_nonzero(interior)) > filled:
            mask = interior
    return mask


def _camera_axes(azimuth_deg, elevation_deg, np):
    """General Purpose: Image right and up for a camera looking at the origin.

    Azimuth 0 places the camera on +Z. Positive elevation raises the camera.
    """
    azimuth = np.radians(azimuth_deg)
    elevation = np.radians(elevation_deg)
    view_dir = np.array(
        [
            np.sin(azimuth) * np.cos(elevation),
            np.sin(elevation),
            np.cos(azimuth) * np.cos(elevation),
        ],
        dtype=np.float64,
    )
    forward = -view_dir
    world_up = np.array([0.0, 1.0, 0.0], dtype=np.float64)
    if abs(float(np.dot(forward, world_up))) > 0.99:
        world_up = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    right = np.cross(forward, world_up)
    right = right / np.linalg.norm(right)
    up = np.cross(right, forward)
    up = up / np.linalg.norm(up)
    return right, up


def reconstruct_visual_hull(masks_with_angles, grid_res, np):
    """General Purpose: Keep voxels that project inside every solid mask.

    masks_with_angles is (mask, azimuth_deg, elevation_deg). The grid is the
    cube [-1, 1] on each axis. Each mask's bounding box is the projection
    of that cube, so the object does not need to sit in the middle of the photo.
    """
    voxels = np.ones((grid_res, grid_res, grid_res), dtype=bool)
    linspace = np.linspace(-1.0, 1.0, grid_res)
    xs, ys, zs = np.meshgrid(linspace, linspace, linspace, indexing="ij")
    points = np.stack([xs.ravel(), ys.ravel(), zs.ravel()], axis=1)
    counts = []
    for mask, azimuth, elevation in masks_with_angles:
        solid = mask > 0
        rows, cols = np.where(solid)
        if cols.size == 0:
            counts.append(0)
            voxels[:] = False
            continue
        min_x = float(cols.min())
        max_x = float(cols.max())
        min_y = float(rows.min())
        max_y = float(rows.max())
        center_x = (min_x + max_x) / 2.0
        center_y = (min_y + max_y) / 2.0
        half = max((max_x - min_x) / 2.0, (max_y - min_y) / 2.0, 1.0)
        right, up = _camera_axes(azimuth, elevation, np)
        horizontal = points @ right
        vertical = points @ up
        column = np.rint(center_x + horizontal * half).astype(np.int32)
        row = np.rint(center_y - vertical * half).astype(np.int32)
        height, width = mask.shape[:2]
        inside = (column >= 0) & (column < width) & (row >= 0) & (row < height)
        keep = np.zeros(points.shape[0], dtype=bool)
        keep[inside] = solid[row[inside], column[inside]]
        voxels &= keep.reshape((grid_res, grid_res, grid_res))
        counts.append(int(np.count_nonzero(voxels)))
    return voxels, tuple(counts)


def mesh_from_voxels(voxels, measure, np):
    """General Purpose: Marching-cubes surface in Y-up coordinates, centered."""
    if not np.any(voxels):
        return None
    volume = voxels.astype(np.float32)
    padded = np.pad(volume, 1, mode="constant", constant_values=0)
    grid = voxels.shape[0]
    step = 2.0 / (grid - 1) if grid > 1 else 1.0
    verts, faces, normals, _values = measure.marching_cubes(
        padded, level=0.5, spacing=(step, step, step)
    )
    origin = -1.0 - step
    coords = np.asarray(verts, dtype=np.float32) + np.float32(origin)
    center = coords.mean(axis=0)
    coords = coords - center
    extent = float(np.max(np.linalg.norm(coords, axis=1)))
    if extent > 0:
        coords = coords / np.float32(extent)
    faces = np.asarray(faces, dtype=np.uint32)
    normals = np.asarray(normals, dtype=np.float32)
    return coords, faces, normals


def _pad4(blob):
    extra = (4 - (len(blob) % 4)) % 4
    if extra:
        return blob + (b"\x00" * extra)
    return blob


def write_glb(path, positions, normals, indices):
    """General Purpose: Write one binary glTF 2.0 mesh with normals."""
    pos = positions.astype("<f4", copy=False).reshape(-1, 3)
    nrm = normals.astype("<f4", copy=False).reshape(-1, 3)
    idx = indices.astype("<u4", copy=False).reshape(-1)
    pos_bytes = np_tobytes(pos)
    nrm_bytes = np_tobytes(nrm)
    idx_bytes = np_tobytes(idx)
    blob = pos_bytes + nrm_bytes + idx_bytes
    nvert = int(pos.shape[0])
    nidx = int(idx.shape[0])
    pos_min = [float(value) for value in pos.min(axis=0)]
    pos_max = [float(value) for value in pos.max(axis=0)]
    document = {
        "asset": {"version": "2.0", "generator": "ThreeDimensionModeller"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "materials": [
            {
                "doubleSided": True,
                "pbrMetallicRoughness": {
                    "baseColorFactor": [0.72, 0.76, 0.8, 1.0],
                    "metallicFactor": 0.05,
                    "roughnessFactor": 0.55,
                },
            }
        ],
        "meshes": [
            {
                "primitives": [
                    {
                        "attributes": {"POSITION": 0, "NORMAL": 1},
                        "indices": 2,
                        "material": 0,
                        "mode": 4,
                    }
                ]
            }
        ],
        "buffers": [{"byteLength": len(blob)}],
        "bufferViews": [
            {
                "buffer": 0,
                "byteOffset": 0,
                "byteLength": len(pos_bytes),
                "target": 34962,
            },
            {
                "buffer": 0,
                "byteOffset": len(pos_bytes),
                "byteLength": len(nrm_bytes),
                "target": 34962,
            },
            {
                "buffer": 0,
                "byteOffset": len(pos_bytes) + len(nrm_bytes),
                "byteLength": len(idx_bytes),
                "target": 34963,
            },
        ],
        "accessors": [
            {
                "bufferView": 0,
                "componentType": 5126,
                "count": nvert,
                "type": "VEC3",
                "min": pos_min,
                "max": pos_max,
            },
            {
                "bufferView": 1,
                "componentType": 5126,
                "count": nvert,
                "type": "VEC3",
            },
            {
                "bufferView": 2,
                "componentType": 5125,
                "count": nidx,
                "type": "SCALAR",
            },
        ],
    }
    json_bytes = _pad4(json.dumps(document, separators=(",", ":")).encode("utf-8"))
    bin_bytes = _pad4(blob)
    total = 12 + 8 + len(json_bytes) + 8 + len(bin_bytes)
    header = struct.pack("<4sII", b"glTF", 2, total)
    json_chunk = struct.pack("<I4s", len(json_bytes), b"JSON") + json_bytes
    bin_chunk = struct.pack("<I4s", len(bin_bytes), b"BIN\x00") + bin_bytes
    Path(path).write_bytes(header + json_chunk + bin_chunk)
    return nvert, nidx // 3


def np_tobytes(array):
    """General Purpose: Contiguous little-endian bytes for one numeric array."""
    import numpy as np

    return np.ascontiguousarray(array).tobytes()


def viewer_html(positions, normals, indices):
    """General Purpose: One HTML file that draws this mesh with no network."""
    pos_b64 = base64.b64encode(np_tobytes(positions.astype("<f4"))).decode("ascii")
    nrm_b64 = base64.b64encode(np_tobytes(normals.astype("<f4"))).decode("ascii")
    idx_b64 = base64.b64encode(np_tobytes(indices.astype("<u4"))).decode("ascii")
    page = _VIEWER_PAGE
    page = page.replace("__POS__", pos_b64)
    page = page.replace("__NRM__", nrm_b64)
    page = page.replace("__IDX__", idx_b64)
    return page


_VIEWER_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ThreeDimensionModeller</title>
<style>
html, body { margin: 0; height: 100%; background: #121418; color: #d5dde6; font-family: sans-serif; }
canvas { display: block; width: 100%; height: 100%; }
p { position: fixed; left: 12px; bottom: 10px; margin: 0; font-size: 13px; }
</style>
</head>
<body>
<canvas id="view"></canvas>
<p>ThreeDimensionModeller — drag to orbit, wheel to zoom. model.glb is the glTF file.</p>
<script>
const posB64 = "__POS__";
const nrmB64 = "__NRM__";
const idxB64 = "__IDX__";
function b64floats(text) {
  const raw = atob(text);
  const bytes = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
  return new Float32Array(bytes.buffer);
}
function b64uints(text) {
  const raw = atob(text);
  const bytes = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
  return new Uint32Array(bytes.buffer);
}
const positions = b64floats(posB64);
const normals = b64floats(nrmB64);
const indices = b64uints(idxB64);
const canvas = document.getElementById("view");
const gl = canvas.getContext("webgl2", { antialias: true });
if (!gl) {
  document.body.insertAdjacentHTML("beforeend", "<p>This browser has no WebGL2.</p>");
} else {
  const vs = `#version 300 es
  layout(location=0) in vec3 aPos;
  layout(location=1) in vec3 aNrm;
  uniform mat4 uMvp;
  uniform mat3 uN;
  out vec3 vNrm;
  void main() {
    vNrm = normalize(uN * aNrm);
    gl_Position = uMvp * vec4(aPos, 1.0);
  }`;
  const fs = `#version 300 es
  precision mediump float;
  in vec3 vNrm;
  out vec4 outColor;
  void main() {
    vec3 n = normalize(vNrm);
    vec3 light = normalize(vec3(0.35, 0.85, 0.45));
    float shade = 0.28 + 0.72 * max(dot(n, light), 0.0);
    outColor = vec4(vec3(0.73, 0.78, 0.84) * shade, 1.0);
  }`;
  function shader(type, source) {
    const item = gl.createShader(type);
    gl.shaderSource(item, source);
    gl.compileShader(item);
    return item;
  }
  const program = gl.createProgram();
  gl.attachShader(program, shader(gl.VERTEX_SHADER, vs));
  gl.attachShader(program, shader(gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(program);
  gl.useProgram(program);
  function buffer(data, target) {
    const buf = gl.createBuffer();
    gl.bindBuffer(target, buf);
    gl.bufferData(target, data, gl.STATIC_DRAW);
    return buf;
  }
  buffer(positions, gl.ARRAY_BUFFER);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);
  buffer(normals, gl.ARRAY_BUFFER);
  gl.enableVertexAttribArray(1);
  gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 0, 0);
  buffer(indices, gl.ELEMENT_ARRAY_BUFFER);
  const uMvp = gl.getUniformLocation(program, "uMvp");
  const uN = gl.getUniformLocation(program, "uN");
  gl.enable(gl.DEPTH_TEST);
  gl.disable(gl.CULL_FACE);
  let yaw = 0.7;
  let pitch = 0.35;
  let distance = 2.6;
  let dragging = false;
  let lastX = 0;
  let lastY = 0;
  canvas.addEventListener("pointerdown", (event) => {
    dragging = true;
    lastX = event.clientX;
    lastY = event.clientY;
    canvas.setPointerCapture(event.pointerId);
  });
  canvas.addEventListener("pointerup", () => { dragging = false; });
  canvas.addEventListener("pointermove", (event) => {
    if (!dragging) return;
    yaw += (event.clientX - lastX) * 0.01;
    pitch += (event.clientY - lastY) * 0.01;
    pitch = Math.max(-1.2, Math.min(1.2, pitch));
    lastX = event.clientX;
    lastY = event.clientY;
  });
  canvas.addEventListener("wheel", (event) => {
    event.preventDefault();
    distance *= event.deltaY > 0 ? 1.08 : 0.92;
    distance = Math.max(1.2, Math.min(8.0, distance));
  }, { passive: false });
  function perspective(fovy, aspect, near, far) {
    const f = 1 / Math.tan(fovy / 2);
    const nf = 1 / (near - far);
    return new Float32Array([
      f / aspect, 0, 0, 0,
      0, f, 0, 0,
      0, 0, (far + near) * nf, -1,
      0, 0, 2 * far * near * nf, 0
    ]);
  }
  function look(eye, target, up) {
    function norm(v) {
      const n = Math.hypot(v[0], v[1], v[2]) || 1;
      return [v[0] / n, v[1] / n, v[2] / n];
    }
    function cross(a, b) {
      return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]];
    }
    function sub(a, b) { return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]; }
    const z = norm(sub(eye, target));
    const x = norm(cross(up, z));
    const y = cross(z, x);
    return new Float32Array([
      x[0], y[0], z[0], 0,
      x[1], y[1], z[1], 0,
      x[2], y[2], z[2], 0,
      -(x[0]*eye[0] + x[1]*eye[1] + x[2]*eye[2]),
      -(y[0]*eye[0] + y[1]*eye[1] + y[2]*eye[2]),
      -(z[0]*eye[0] + z[1]*eye[1] + z[2]*eye[2]),
      1
    ]);
  }
  function multiply(a, b) {
    const out = new Float32Array(16);
    for (let col = 0; col < 4; col++) {
      for (let row = 0; row < 4; row++) {
        out[col * 4 + row] =
          a[row] * b[col * 4] +
          a[4 + row] * b[col * 4 + 1] +
          a[8 + row] * b[col * 4 + 2] +
          a[12 + row] * b[col * 4 + 3];
      }
    }
    return out;
  }
  function frame() {
    const width = canvas.clientWidth || 1;
    const height = canvas.clientHeight || 1;
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
    }
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.07, 0.08, 0.1, 1);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    const eye = [
      distance * Math.cos(pitch) * Math.sin(yaw),
      distance * Math.sin(pitch),
      distance * Math.cos(pitch) * Math.cos(yaw)
    ];
    const view = look(eye, [0, 0, 0], [0, 1, 0]);
    const proj = perspective(0.9, canvas.width / canvas.height, 0.05, 40);
    const mvp = multiply(proj, view);
    gl.uniformMatrix4fv(uMvp, false, mvp);
    const nmat = new Float32Array([
      view[0], view[1], view[2],
      view[4], view[5], view[6],
      view[8], view[9], view[10]
    ]);
    gl.uniformMatrix3fv(uN, false, nmat);
    gl.drawElements(gl.TRIANGLES, indices.length, gl.UNSIGNED_INT, 0);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
</script>
</body>
</html>
"""


def _done(code, lines, on_notice, announced):
    if announced and lines and lines[0] != announced[0]:
        lines.insert(0, announced[0])
    elif announced and not lines:
        lines = list(announced)
    return code, lines


def convert_folder(
    folder,
    output_dir=None,
    views_path=None,
    grid=None,
    choice="model",
    on_notice=None,
):
    """General Purpose: Build model.glb and viewer.html from outline images.

    With no views file, images are spaced evenly in azimuth at elevation 0.
    A views.json in the folder is used when views_path is omitted.
    requirement-domain-threedimensionmodeller.
    """
    announced = []
    place = Path(folder).expanduser()
    if not place.is_dir():
        return _done(
            1,
            [
                "ERROR: {0} is not a folder.".format(place),
                "   Next: three-dimension-modeller model",
            ],
            on_notice,
            announced,
        )
    place = place.resolve()
    grid_res = DEFAULT_GRID if grid is None else grid
    try:
        grid_res = int(grid_res)
    except (TypeError, ValueError):
        grid_res = -1
    if grid_res < MIN_GRID or grid_res > MAX_GRID:
        return _done(
            1,
            [
                "ERROR: grid must be an integer from {0} to {1}.".format(
                    MIN_GRID, MAX_GRID
                ),
                "   Next: three-dimension-modeller model --grid {0}".format(DEFAULT_GRID),
            ],
            on_notice,
            announced,
        )
    images = list_images(place)
    view_file = None
    if views_path:
        view_file = Path(views_path).expanduser()
    elif (place / "views.json").is_file():
        view_file = place / "views.json"
    try:
        if view_file is not None:
            if not view_file.is_file():
                raise ValueError("views file is missing")
            views = _read_views(view_file)
        else:
            views = _equal_views(images)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return _done(
            1,
            [
                "ERROR: Could not read views: {0}".format(exc),
                "   Next: three-dimension-modeller model --views views.json",
            ],
            on_notice,
            announced,
        )
    if not views:
        return _done(
            0,
            ["No supported images found in {0}".format(place)],
            on_notice,
            announced,
        )
    by_name = {image.name: image for image in images}
    missing = [row["file"] for row in views if row["file"] not in by_name]
    if missing and len(missing) == len(views):
        return _done(
            1,
            [
                "ERROR: None of the named outlines are in {0}".format(place),
                "   Next: three-dimension-modeller model",
            ],
            on_notice,
            announced,
        )
    dest = Path(output_dir).expanduser().resolve() if output_dir else output_dir_for(place)
    try:
        dest.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return _done(
            1,
            [
                "ERROR: Could not create the output directory: {0}".format(exc),
                "   Next: three-dimension-modeller model",
            ],
            on_notice,
            announced,
        )
    sentence = selected_choice_line(choice, "Building the 3D model")
    announced.append(sentence)
    if on_notice is not None:
        on_notice(sentence)
    try:
        cv2, np, measure = _image_stack()
    except ImportError:
        return _done(
            1,
            [
                sentence,
                "ERROR: numpy, opencv-python-headless, and scikit-image are required.",
                '   Next: python -m pip install "ThreeDimensionModeller"',
            ],
            on_notice,
            announced,
        )
    lines = [sentence]
    failed = False
    masks = []
    for row in views:
        image = by_name.get(row["file"])
        if image is None:
            failed = True
            lines.append("ERROR: Missing outline {0}".format(row["file"]))
            continue
        try:
            mask = outline_to_solid_mask(image, cv2, np)
        except (OSError, ValueError) as exc:
            failed = True
            lines.append("ERROR: Failed on {0}: {1}".format(image.name, exc))
            continue
        foreground = int(np.count_nonzero(mask))
        if foreground < 50:
            failed = True
            lines.append("ERROR: No closed outline in {0}".format(image.name))
            continue
        masks.append((mask, row["azimuth"], row["elevation"], image.name, foreground))
        lines.append(
            "Mask {0}: {1} foreground pixels, azimuth {2}, elevation {3}".format(
                image.name, foreground, row["azimuth"], row["elevation"]
            )
        )
    if not masks:
        lines.append("ERROR: No outline could be filled.")
        lines.append("   Next: three-dimension-modeller model")
        return _done(1, lines, on_notice, announced)
    voxels, counts = reconstruct_visual_hull(
        [(mask, azimuth, elevation) for mask, azimuth, elevation, _name, _count in masks],
        grid_res,
        np,
    )
    for index, count in enumerate(counts):
        lines.append(
            "Carved {0}: {1} voxels remain.".format(masks[index][3], count)
        )
    mesh = mesh_from_voxels(voxels, measure, np)
    if mesh is None:
        lines.append(
            "ERROR: The visual hull is empty. Check overlap and the view angles."
        )
        lines.append("   Next: three-dimension-modeller model --views views.json")
        return _done(1, lines, on_notice, announced)
    positions, faces, normals = mesh
    glb_path = dest / GLB_NAME
    html_path = dest / VIEWER_NAME
    try:
        vertex_count, triangle_count = write_glb(glb_path, positions, normals, faces)
        html_path.write_text(viewer_html(positions, normals, faces), encoding="utf-8")
    except OSError as exc:
        lines.append("ERROR: Could not write the model: {0}".format(exc))
        lines.append("   Next: three-dimension-modeller model")
        return _done(1, lines, on_notice, announced)
    lines.append(
        "Saved model -> {0} ({1} vertices, {2} triangles)".format(
            glb_path.name, vertex_count, triangle_count
        )
    )
    lines.append("Saved viewer -> {0}".format(html_path.name))
    lines.append("Model saved in: {0}".format(dest))
    return _done(1 if failed else 0, lines, on_notice, announced)


def main(argv=None):
    """General Purpose: ./convert.py entry. Same conversion as the model verb."""
    parser = argparse.ArgumentParser(
        prog="convert.py",
        description="Build a glTF model and an HTML viewer from outline images.",
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=None,
        help="Folder of outline images (default: current directory)",
    )
    parser.add_argument(
        "--input-dir",
        "-i",
        default=None,
        help="Same as the folder argument",
    )
    parser.add_argument(
        "--output",
        "--output-dir",
        "-o",
        dest="output",
        default=None,
        help="Output folder (default: <folder>/model)",
    )
    parser.add_argument(
        "--views",
        default=None,
        help="JSON file of file, azimuth, and elevation for each outline",
    )
    parser.add_argument(
        "--grid",
        type=int,
        default=None,
        help="Voxels on each axis, {0} to {1} (default: {2})".format(
            MIN_GRID, MAX_GRID, DEFAULT_GRID
        ),
    )
    args = parser.parse_args(argv)
    if args.folder and args.input_dir:
        print("ERROR: Pass the folder once.", file=sys.stderr)
        print("   Next: ./convert.py --input-dir photos", file=sys.stderr)
        return 1
    folder = args.folder or args.input_dir or "."
    spoken = []

    def _notice(line):
        print(line, flush=True)
        spoken.append(line)

    code, lines = convert_folder(
        folder,
        output_dir=args.output,
        views_path=args.views,
        grid=args.grid,
        choice="convert.py",
        on_notice=_notice,
    )
    rest = lines[len(spoken):]
    if rest:
        print("\n".join(rest))
    return code


if __name__ == "__main__":
    sys.exit(main())
