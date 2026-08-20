#!/usr/bin/env python3
import sys


sys.dont_write_bytecode = True

import json
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


manifest_checks = load_module(
    "check_zh_manifest", ROOT / "scripts" / "check-zh-manifest.py"
)
term_checks = load_module("check_terms", ROOT / "scripts" / "check-terms.py")


class ManifestChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        content = self.root / "content"
        locale_content = self.root / "locale" / "zh" / "content"
        content.mkdir()
        locale_content.mkdir(parents=True)
        (content / "one.tex").write_text("source\n", encoding="utf-8")
        (locale_content / "one.tex").write_text("translation\n", encoding="utf-8")
        (self.root / "locale" / "zh" / "manifest.txt").write_text(
            "# path list\none.tex\n", encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_scope_reports_unlisted_and_missing_source_paths(self):
        extra = self.root / "locale" / "zh" / "content" / "extra.tex"
        extra.write_text("extra\n", encoding="utf-8")
        problems, _ = manifest_checks.validate(self.root)
        report = "\n".join(problems)
        self.assertIn("not listed in manifest", report)
        self.assertIn("without an English counterpart", report)

        extra.unlink()
        (self.root / "locale" / "zh" / "manifest.txt").write_text(
            "# path list\nmissing.tex\none.tex\n", encoding="utf-8"
        )
        problems, _ = manifest_checks.validate(self.root)
        report = "\n".join(problems)
        self.assertIn("manifest entries missing", report)
        self.assertIn("without an English counterpart", report)

    def test_manifest_rejects_noncanonical_paths(self):
        manifest = self.root / "locale" / "zh" / "manifest.txt"
        manifest.write_text(
            "# path list\na//b.tex\na/./b.tex\n", encoding="utf-8"
        )
        paths, problems = manifest_checks.manifest_paths(manifest)
        self.assertEqual(paths, [])
        report = "\n".join(problems)
        self.assertIn("a//b.tex", report)
        self.assertIn("a/./b.tex", report)


class TokenChecks(unittest.TestCase):
    def test_parser_ignores_comments_and_definitions(self):
        sty = (
            "% \\zhToken[comment]{ignored}{伪调用}\n"
            "\\newcommand{\\zhToken}[3][]{#1#2#3}\n"
            "\\zhToken[formula]{formula}{公式} % trailing comment\n"
        )
        tokens, problems = term_checks.parse_sty_tokens(sty, "fixture.sty")
        self.assertEqual(tokens, {"!!{formula}": "公式"})
        self.assertEqual(problems, [])

    def test_parser_rejects_duplicate_and_trailing_text(self):
        sty = "\\zhToken[formula]{formula}{公式}\n\\zhToken[formula]{formula}{公式}\n"
        _, problems = term_checks.parse_sty_tokens(sty, "fixture.sty")
        self.assertTrue(any("duplicate" in problem for problem in problems))

        _, problems = term_checks.parse_sty_tokens(
            "\\zhToken[formula]{formula}{公式} trailing\n", "fixture.sty"
        )
        self.assertTrue(any("malformed" in problem for problem in problems))

    def test_mapping_difference_is_reported(self):
        problems = term_checks.compare_token_maps(
            {"!!{formula}": "公式"}, {"!!{formula}": "公式X"}
        )
        self.assertTrue(any("mapping mismatch" in problem for problem in problems))

    def test_structural_types_are_failures(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            terms = root / "terms.json"
            index = root / "index.json"
            terms.write_text('{"terms":[1],"context":{}}', encoding="utf-8")
            index.write_text('{"entries":[1]}', encoding="utf-8")
            term_problems, _ = term_checks.validate_terms(terms)
            index_problems, _ = term_checks.validate_index(index)
            self.assertIn("terms[0]: entry must be an object", term_problems)
            self.assertIn("index[0]: entry must be an object", index_problems)

            terms.write_text("[]", encoding="utf-8")
            index.write_text("[]", encoding="utf-8")
            term_problems, _ = term_checks.validate_terms(terms)
            index_problems, _ = term_checks.validate_index(index)
            self.assertIn("root must be an object", term_problems[0])
            self.assertIn("root must be an object", index_problems[0])

            index.write_text("{}", encoding="utf-8")
            index_problems, _ = term_checks.validate_index(index)
            self.assertIn('"entries" missing', index_problems[0])

    def test_index_allows_empty_english_and_checks_line_type(self):
        with tempfile.TemporaryDirectory() as directory:
            index = Path(directory) / "index.json"
            entry = {"line": 1, "zh": "", "en": "", "pages": "", "sub": False}
            index.write_text('{"entries": [' + json.dumps(entry) + "]}", encoding="utf-8")
            problems, _ = term_checks.validate_index(index)
            self.assertEqual(problems, [])

            entry["line"] = "1"
            index.write_text('{"entries": [' + json.dumps(entry) + "]}", encoding="utf-8")
            problems, _ = term_checks.validate_index(index)
            self.assertIn("line must be a positive integer", problems[0])


if __name__ == "__main__":
    unittest.main()
