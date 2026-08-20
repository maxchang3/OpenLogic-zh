#!/usr/bin/env python3
import contextlib
import io
import json
import subprocess
import sys


sys.dont_write_bytecode = True

from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(path):
    import importlib.util

    spec = importlib.util.spec_from_file_location("translation_state", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


state = load_module(ROOT / "scripts" / "translation-state.py")


class TemporaryTranslationRepository:
    def __init__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "content").mkdir()
        (self.root / "locale" / "zh" / "content").mkdir(parents=True)
        (self.root / ".agents" / "translation" / "terminology").mkdir(
            parents=True
        )
        (self.root / "content" / "one.tex").write_text(
            "alpha appears.\n", encoding="utf-8"
        )
        (self.root / "locale" / "zh" / "content" / "one.tex").write_text(
            "阿尔法出现。\n", encoding="utf-8"
        )
        (self.root / "locale" / "zh" / "manifest.txt").write_text(
            "one.tex\n", encoding="utf-8"
        )
        (self.root / ".agents" / "translation" / "state.json").write_text(
            '{"schema": 1, "pairs": {}}\n', encoding="utf-8"
        )
        (
            self.root
            / ".agents"
            / "translation"
            / "terminology"
            / "terms.json"
        ).write_text(
            json.dumps(
                {
                    "terms": [
                        {"en": "alpha", "zh": "阿尔法", "module": "core"},
                        {"en": "beta", "zh": "贝塔", "module": "core"},
                        {"en": "gamma", "zh": "伽马", "module": "core"},
                    ]
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Translation Test")
        self.git("config", "commit.gpgsign", "false")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "fixture")

    def close(self):
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.root, check=True, stdout=subprocess.PIPE
        )

    def confirm(self):
        problems, confirmed = state.confirm_paths(
            self.root, ["one.tex"], write=True, run_static=False
        )
        if problems or confirmed != ["one.tex"]:
            raise AssertionError(f"confirm failed: {problems}, {confirmed}")

    def statuses(self):
        entries, problems = state.status_entries(self.root)
        if problems:
            raise AssertionError(f"status failed: {problems}")
        return {entry["path"]: entry["status"] for entry in entries}


class TranslationStateChecks(unittest.TestCase):
    def test_empty_state_covers_every_manifest_entry(self):
        fixture = TemporaryTranslationRepository()
        self.addCleanup(fixture.close)
        (fixture.root / "content" / "two.tex").write_text(
            "second\n", encoding="utf-8"
        )
        (fixture.root / "locale" / "zh" / "content" / "two.tex").write_text(
            "第二个\n", encoding="utf-8"
        )
        (fixture.root / "locale" / "zh" / "manifest.txt").write_text(
            "one.tex\ntwo.tex\n", encoding="utf-8"
        )
        entries, problems = state.status_entries(fixture.root)
        self.assertEqual(problems, [])
        self.assertEqual(
            {entry["path"] for entry in entries}, {"one.tex", "two.tex"}
        )
        self.assertEqual({entry["status"] for entry in entries}, {"unconfirmed"})

    def test_confirm_records_blobs_and_derives_all_change_states(self):
        fixture = TemporaryTranslationRepository()
        self.addCleanup(fixture.close)

        self.assertEqual(fixture.statuses(), {"one.tex": "unconfirmed"})
        fixture.confirm()
        self.assertEqual(fixture.statuses(), {"one.tex": "confirmed"})

        source = fixture.root / "content" / "one.tex"
        translation = fixture.root / "locale" / "zh" / "content" / "one.tex"
        source.write_text("alpha changed.\n", encoding="utf-8")
        self.assertEqual(fixture.statuses(), {"one.tex": "source-changed"})
        source.write_text("alpha appears.\n", encoding="utf-8")
        translation.write_text("阿尔法已改。\n", encoding="utf-8")
        self.assertEqual(fixture.statuses(), {"one.tex": "translation-changed"})
        source.write_text("alpha changed too.\n", encoding="utf-8")
        self.assertEqual(fixture.statuses(), {"one.tex": "both-changed"})

    def test_check_rejects_stale_unknown_and_non_blob_state(self):
        fixture = TemporaryTranslationRepository()
        self.addCleanup(fixture.close)
        fixture.confirm()

        source = fixture.root / "content" / "one.tex"
        source.write_text("alpha changed.\n", encoding="utf-8")
        problems = state.check_state(fixture.root)
        self.assertTrue(any("source changed" in problem for problem in problems))

        document = {
            "schema": 1,
            "pairs": {
                "unknown.tex": {"source": "0" * 40, "translation": "0" * 40}
            },
        }
        (fixture.root / ".agents" / "translation" / "state.json").write_text(
            json.dumps(document) + "\n", encoding="utf-8"
        )
        problems = state.check_state(fixture.root)
        self.assertTrue(any("not in manifest" in problem for problem in problems))

        document = {
            "schema": 1,
            "pairs": {
                "one.tex": {"source": "0" * 40, "translation": "0" * 40}
            },
        }
        (fixture.root / ".agents" / "translation" / "state.json").write_text(
            json.dumps(document) + "\n", encoding="utf-8"
        )
        problems = state.check_state(fixture.root)
        self.assertTrue(any("not a readable Git blob" in problem for problem in problems))

    def test_brief_uses_stored_source_diff_and_only_matching_terms(self):
        fixture = TemporaryTranslationRepository()
        self.addCleanup(fixture.close)
        fixture.confirm()
        (fixture.root / "content" / "one.tex").write_text(
            "alpha appears.\n% gamma in comment\nbeta changed.\n",
            encoding="utf-8",
        )

        output, problems = state.brief(fixture.root, "one.tex")
        self.assertEqual(problems, [])
        self.assertIn("--- confirmed/content/one.tex", output)
        self.assertIn("+++ content/one.tex", output)
        self.assertIn("beta → 贝塔", output)
        self.assertNotIn("alpha → 阿尔法", output)
        self.assertNotIn("gamma → 伽马", output)

        (fixture.root / ".agents" / "translation" / "state.json").write_text(
            '{"schema": 1, "pairs": {}}\n', encoding="utf-8"
        )
        output, problems = state.brief(fixture.root, "one.tex")
        self.assertEqual(problems, [])
        self.assertIn("[unconfirmed", output)
        self.assertNotIn("alpha appears.", output)
        self.assertNotIn("gamma → 伽马", output)

    def test_confirm_static_failure_does_not_write_state(self):
        fixture = TemporaryTranslationRepository()
        self.addCleanup(fixture.close)
        state_file = fixture.root / ".agents" / "translation" / "state.json"
        before = state_file.read_text(encoding="utf-8")
        original_gate = state.run_static_gate
        state.run_static_gate = lambda root: 1
        try:
            problems, confirmed = state.confirm_paths(
                fixture.root, ["one.tex"], write=True
            )
        finally:
            state.run_static_gate = original_gate
        self.assertEqual(confirmed, [])
        self.assertTrue(any("check-zh-static failed" in problem for problem in problems))
        self.assertEqual(state_file.read_text(encoding="utf-8"), before)

    def test_confirm_deduplicates_paths(self):
        fixture = TemporaryTranslationRepository()
        self.addCleanup(fixture.close)
        problems, confirmed = state.confirm_paths(
            fixture.root, ["one.tex", "one.tex"], write=True, run_static=False
        )
        self.assertEqual(problems, [])
        self.assertEqual(confirmed, ["one.tex"])

    def test_confirm_without_write_is_rejected(self):
        fixture = TemporaryTranslationRepository()
        self.addCleanup(fixture.close)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = state.main(["confirm", "one.tex"], root=fixture.root)
        self.assertEqual(code, 2)
        self.assertIn("--write", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
