#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(path):
    spec = importlib.util.spec_from_file_location("consumer_closure", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


closure = load_module(ROOT / "scripts" / "check-consumer-closure.py")


class ConsumerClosureChecks(unittest.TestCase):
    def test_extracts_and_normalizes_english_and_locale_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            olp = workspace / "OpenLogic-Zh"
            consumer = workspace / "book"
            (olp / "content" / "part").mkdir(parents=True)
            (olp / "locale" / "zh" / "content" / "part").mkdir(parents=True)
            consumer.mkdir()
            fls = consumer / "book.fls"
            fls.write_text(
                "INPUT ../OpenLogic-Zh/content/part/one.tex\n"
                "INPUT ../OpenLogic-Zh/content/part/one.tex\n"
                "INPUT ../OpenLogic-Zh/locale/zh/content/part/two.tex\n"
                "INPUT ../OpenLogic-Zh/sty/open-logic.sty\n",
                encoding="utf-8",
            )
            self.assertEqual(
                closure.extract_paths(fls, olp), ["part/one.tex", "part/two.tex"]
            )

    def test_metadata_requires_sources_and_revisions(self):
        valid = {
            "driver": "book-screen.tex",
            "tag-config": "book-config.sty",
            "consumer-revision": "1" * 40,
            "openlogic-revision": "2" * 40,
        }
        self.assertEqual(
            closure.metadata_problems(valid, "book-screen.tex", "book-config.sty"), []
        )
        invalid = dict(valid, **{"consumer-revision": "main"})
        problems = closure.metadata_problems(
            invalid, "other.tex", "book-config.sty"
        )
        self.assertTrue(any("expected" in problem for problem in problems))
        self.assertTrue(any("invalid consumer-revision" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
