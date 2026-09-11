#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_module(path):
    spec = importlib.util.spec_from_file_location("plan_dispatch", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = load_module(ROOT / ".github" / "scripts" / "plan-dispatch.py")


class DispatchPlanChecks(unittest.TestCase):
    def test_routes_body_changes_by_consumer_closure(self):
        bd = {"shared.tex", "bd-only.tex"}
        slc = {"shared.tex", "slc-only.tex"}
        self.assertEqual(dispatch.plan(["content/bd-only.tex"], bd, slc), {"bd"})
        self.assertEqual(
            dispatch.plan(["locale/zh/content/slc-only.tex"], bd, slc), {"slc"}
        )
        self.assertEqual(
            dispatch.plan(["content/shared.tex"], bd, slc), {"bd", "slc"}
        )

    def test_shared_and_closure_metadata_changes_dispatch_all(self):
        bd = {"bd.tex"}
        slc = {"slc.tex"}
        for changed in (
            "sty/open-logic.sty",
            "locale/zh/open-logic-config.sty",
            "locale/zh/consumers/sets-logic-computation-zh.txt",
        ):
            with self.subTest(changed=changed):
                self.assertEqual(
                    dispatch.plan([changed], bd, slc), {"bd", "slc"}
                )

    def test_both_closure_files_are_required(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.txt"
            with self.assertRaises(FileNotFoundError):
                dispatch.read_closure(missing)


if __name__ == "__main__":
    unittest.main()
