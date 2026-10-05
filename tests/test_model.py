# model — folder build and menu row 1.
# The typed verb builds a folder and does not draw the menu.
# Menu row 1 lists the current folder, each subfolder, and Back.
import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from ThreeDimensionModeller.cli import Cli
from ThreeDimensionModeller.menu_model import MenuModel
from ThreeDimensionModeller.menu_painter import MenuPainter
from ThreeDimensionModeller.model import (
    convert_folder,
    list_images,
    main as convert_main,
    selected_choice_line,
)
from ThreeDimensionModeller.tui import Tui


class TestModel(unittest.TestCase):
    """Typed model builds a folder. Menu row 1 picks that folder."""

    def test_cli_model_builds_the_current_folder_and_skips_the_menu(self):
        app = Cli()
        self.assertIn("model", Cli.PRODUCT_VERBS)
        self.assertNotIn("outline", Cli.PRODUCT_VERBS)
        self.assertNotIn("hello", Cli.PRODUCT_VERBS)
        self.assertNotIn("join", Cli.PRODUCT_VERBS)
        self.assertNotIn("list-videos", Cli.PRODUCT_VERBS)
        self.assertFalse(Cli.opens_text_screen(["model"]))
        previous = Cli.stdout_is_tty
        Cli.stdout_is_tty = staticmethod(lambda: True)
        try:
            self.assertTrue(Cli.opens_text_screen([]))
            self.assertFalse(Cli.opens_text_screen(["model"]))
            self.assertFalse(Cli.opens_text_screen(["model", "photos"]))
            self.assertTrue(Cli.opens_text_screen(["about"]))
            self.assertFalse(Cli.opens_text_screen(["join"]))
            self.assertFalse(Cli.opens_text_screen(["list-videos"]))
        finally:
            Cli.stdout_is_tty = previous
        folder = tempfile.mkdtemp(prefix="tdmempty_", dir="/tmp")
        previous_dir = os.getcwd()
        os.chdir(folder)
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = app.run(["model"])
        finally:
            os.chdir(previous_dir)
        self.assertEqual(code, 0)
        self.assertIn("No supported images found in", buf.getvalue())
        self.assertIn(os.path.realpath(folder), buf.getvalue())
        self.assertNotIn("has been selected", buf.getvalue())

    def test_model_rejects_a_missing_folder_and_a_foreign_folder_flag(self):
        app = Cli()
        err = io.StringIO()
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = app.run(["model", "/tmp/three-dimension-modeller-missing-folder"])
        self.assertEqual(code, 1)
        self.assertIn("is not a folder", out.getvalue())
        self.assertNotIn("has been selected", out.getvalue())
        err = io.StringIO()
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = app.run(["version", "photos"])
        self.assertEqual(code, 1)
        self.assertIn("A folder is only for model", err.getvalue())

    def test_removed_video_verbs_are_unknown(self):
        app = Cli()
        for verb in ("join", "list-videos", "hello", "outline"):
            err = io.StringIO()
            with redirect_stderr(err):
                code = app.run([verb])
            self.assertEqual(code, 1, verb)
            self.assertIn("Unknown verb '{0}'".format(verb), err.getvalue())
        help_buf = io.StringIO()
        with redirect_stdout(help_buf):
            self.assertEqual(app.run(["help"]), 0)
        text = help_buf.getvalue()
        self.assertIn("model", text)
        self.assertIn("model.glb", text)
        self.assertNotIn("list-videos", text)
        self.assertNotIn("FFmpeg", text)
        self.assertNotIn("ffmpeg", text)
        self.assertNotIn("concatenate", text)

    def test_menu_row_1_lists_the_current_folder_and_subfolders(self):
        home = tempfile.mkdtemp(prefix="tdmhome_", dir="/tmp")
        folder = tempfile.mkdtemp(prefix="tdmclips_", dir="/tmp")
        os.mkdir(os.path.join(folder, "beta"))
        os.mkdir(os.path.join(folder, "alpha"))
        os.mkdir(os.path.join(folder, ".hidden"))
        saved = os.environ.get("THREEDIMENSIONMODELLER_LANG")
        os.environ.pop("THREEDIMENSIONMODELLER_LANG", None)
        previous = os.getcwd()
        os.chdir(folder)
        painter = MenuPainter(home=home)
        try:
            self.assertEqual(painter.language.code(), "en")
            rows = painter.display_rows("front")
            self.assertEqual(
                rows[0],
                (
                    1,
                    "model",
                    "build a 3D model from outline images in a chosen folder",
                    "model",
                ),
            )
            model = MenuModel(painter=painter)
            self.assertIsNone(model._activate(1, "model"))
            self.assertEqual(model.layer, "folders")
            picked = painter.display_rows("folders")
            self.assertEqual(picked[0][0], 1)
            self.assertEqual(picked[0][1], "current")
            self.assertEqual(picked[0][3], "pick:.")
            self.assertEqual(picked[1][1], "alpha")
            self.assertEqual(picked[1][3], "pick:alpha")
            self.assertEqual(picked[2][1], "beta")
            names = [row[1] for row in picked]
            self.assertNotIn(".hidden", names)
        finally:
            os.chdir(previous)
            os.environ.pop("THREEDIMENSIONMODELLER_LANG", None)
            if saved is not None:
                os.environ["THREEDIMENSIONMODELLER_LANG"] = saved

    def test_waiting_sentence_is_a_function(self):
        self.assertEqual(
            selected_choice_line("model", "Building the 3D model"),
            "model has been selected. Building the 3D model takes time to finish.",
        )

    def test_empty_folder_does_not_import_the_vision_stack(self):
        folder = tempfile.mkdtemp(prefix="tdmempty2_", dir="/tmp")
        with patch(
            "ThreeDimensionModeller.model._image_stack",
            side_effect=AssertionError("imported"),
        ):
            code, lines = convert_folder(folder)
        self.assertEqual(code, 0)
        self.assertIn("No supported images found in", "\n".join(lines))
        self.assertNotIn("has been selected", "\n".join(lines))

    def test_two_outlines_write_glb_and_html(self):
        cv2, np, _measure = _stack()
        folder = Path(tempfile.mkdtemp(prefix="tdmbuild_", dir="/tmp"))
        _write_outline(cv2, np, folder / "front.png", 0)
        _write_outline(cv2, np, folder / "side.png", 1)
        views = folder / "views.json"
        views.write_text(
            '{"views":['
            '{"file":"front.png","azimuth":0,"elevation":0},'
            '{"file":"side.png","azimuth":90,"elevation":0}'
            "]}",
            encoding="utf-8",
        )
        code, lines = convert_folder(folder, views_path=views, grid=24, choice="model")
        text = "\n".join(lines)
        self.assertEqual(code, 0, text)
        self.assertTrue(text.startswith(
            "model has been selected. Building the 3D model takes time to finish."
        ))
        glb = folder / "output" / "model.glb"
        html = folder / "output" / "viewer.html"
        self.assertTrue(glb.is_file(), text)
        self.assertTrue(html.is_file(), text)
        self.assertTrue(glb.read_bytes().startswith(b"glTF"))
        page = html.read_text(encoding="utf-8")
        self.assertIn("<canvas", page)
        self.assertNotIn("script src=", page)
        self.assertIn("Model saved in:", text)
        self.assertIn("Saved model -> model.glb", text)
        self.assertIn("Saved viewer -> viewer.html", text)

    def test_cli_model_flushes_the_sentence_before_the_stack(self):
        cv2, np, _measure = _stack()
        folder = Path(tempfile.mkdtemp(prefix="tdmcli_", dir="/tmp"))
        _write_outline(cv2, np, folder / "front.png", 0)
        previous = os.getcwd()
        os.chdir(folder)
        seen = []
        real_stack = __import__(
            "ThreeDimensionModeller.model", fromlist=["_image_stack"]
        )._image_stack

        def _watch():
            seen.append("import")
            return real_stack()

        try:
            buf = io.StringIO()
            with redirect_stdout(buf), patch(
                "ThreeDimensionModeller.model._image_stack", side_effect=_watch
            ):
                code = Cli().run(["model", "--grid", "24"])
        finally:
            os.chdir(previous)
        text = buf.getvalue()
        self.assertEqual(code, 0, text)
        sentence = "model has been selected. Building the 3D model takes time to finish."
        self.assertIn(sentence, text)
        self.assertEqual(seen, ["import"])
        self.assertLess(text.index(sentence), text.index("Saved model"))

    def test_list_images_skips_subfolders(self):
        folder = Path(tempfile.mkdtemp(prefix="tdmlist_", dir="/tmp"))
        (folder / "a.png").write_bytes(b"")
        (folder / "nested").mkdir()
        (folder / "nested" / "b.png").write_bytes(b"")
        (folder / "note.txt").write_text("x", encoding="utf-8")
        names = [item.name for item in list_images(folder)]
        self.assertEqual(names, ["a.png"])

    def test_convert_py_entry_uses_the_same_function(self):
        folder = tempfile.mkdtemp(prefix="tdmconv_", dir="/tmp")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = convert_main(["--input-dir", folder, "--grid", "24"])
        self.assertEqual(code, 0)
        self.assertIn("No supported images found in", buf.getvalue())


def _stack():
    import cv2
    import numpy as np
    from skimage import measure

    return cv2, np, measure


def _write_outline(cv2, np, path, which):
    canvas = np.zeros((80, 80), dtype=np.uint8)
    if which == 0:
        cv2.ellipse(canvas, (40, 40), (24, 18), 0, 0, 360, 255, 2)
    else:
        cv2.ellipse(canvas, (40, 40), (12, 18), 0, 0, 360, 255, 2)
    cv2.imwrite(str(path), canvas)


if __name__ == "__main__":
    unittest.main()
