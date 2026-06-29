import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_NAME = "Part2.1分箱_Chi.py"


def load_chi_helpers():
    script = (REPO_ROOT / SCRIPT_NAME).read_text(encoding="utf-8")
    helper_source = script.split("#读取数据", 1)[0]
    namespace = {}
    exec(compile(helper_source, SCRIPT_NAME, "exec"), namespace)
    return namespace


class ChiBinningRegressionTests(unittest.TestCase):
    def test_assign_group_preserves_order_for_large_values(self):
        helpers = load_chi_helpers()
        assign_group = helpers["AssignGroup"]

        split_points = [1_700_000_000_000, 1_700_000_000_100]

        self.assertEqual(assign_group(1_700_000_000_050, split_points), split_points[1])
        self.assertEqual(assign_group(1_700_000_000_150, split_points), float("inf"))
        self.assertGreater(assign_group(1_700_000_000_150, split_points), split_points[-1])

    def test_full_chi_workflow_completes_on_checked_in_data(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            shutil.copy(REPO_ROOT / SCRIPT_NAME, tmpdir_path / SCRIPT_NAME)
            shutil.copy(REPO_ROOT / "test1.csv", tmpdir_path / "test1.csv")

            result = subprocess.run(
                [sys.executable, SCRIPT_NAME],
                cwd=tmpdir_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300,
            )

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
