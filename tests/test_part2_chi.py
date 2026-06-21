import math
import pickle
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_NAME = "Part2.1分箱_Chi.py"
SCRIPT_PATH = REPO_ROOT / SCRIPT_NAME


def load_chi_helpers():
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    helper_source = source.split("#读取数据", 1)[0]
    namespace = {"__name__": "part2_chi_helpers"}
    exec(compile(helper_source, str(SCRIPT_PATH), "exec"), namespace)
    return namespace


class Part2ChiRegressionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.helpers = load_chi_helpers()

    def test_assign_group_tail_bucket_sorts_after_large_cut_points(self):
        assign_group = self.helpers["AssignGroup"]
        cut_points = [10**12, 2 * 10**12]

        tail_bucket = assign_group(3 * 10**12, cut_points)

        self.assertTrue(math.isinf(tail_bucket))
        self.assertGreater(tail_bucket, max(cut_points))

    def test_checked_in_workflow_completes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            shutil.copy2(SCRIPT_PATH, tmp_path / SCRIPT_NAME)
            shutil.copy2(REPO_ROOT / "test1.csv", tmp_path / "test1.csv")

            subprocess.run(
                [sys.executable, SCRIPT_NAME],
                cwd=tmp_path,
                check=True,
                capture_output=True,
                text=True,
                timeout=300,
            )

            output_path = tmp_path / "continous_merged_dict.pkl"
            self.assertTrue(output_path.exists())
            with output_path.open("rb") as output_file:
                merged_dict = pickle.load(output_file)
            self.assertIn("V01", merged_dict)


if __name__ == "__main__":
    unittest.main()
