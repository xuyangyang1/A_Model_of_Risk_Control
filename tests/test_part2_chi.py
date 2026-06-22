import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "Part2.1分箱_Chi.py"


def load_chi_definitions():
    source = SCRIPT.read_text(encoding="utf-8")
    definitions = source.split("#读取数据", 1)[0]
    namespace = {}
    exec(compile(definitions, str(SCRIPT), "exec"), namespace)
    return namespace


class Part2ChiRegressionTest(unittest.TestCase):
    def test_assign_group_top_bucket_preserves_large_numeric_ordering(self):
        assign_group = load_chi_definitions()["AssignGroup"]
        split_points = [10**12, 2 * 10**12]

        top_bucket = assign_group(3 * 10**12, split_points)

        self.assertGreater(top_bucket, max(split_points))

    def test_non_monotone_retry_uses_result_target_column(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            shutil.copy2(SCRIPT, tmp_path / SCRIPT.name)
            pd.read_csv(
                REPO_ROOT / "test1.csv",
                usecols=["Unnamed: 0", "V01", "result"],
            ).to_csv(tmp_path / "test1.csv", index=False)

            completed = subprocess.run(
                [sys.executable, SCRIPT.name],
                cwd=tmp_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=60,
            )

            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertTrue((tmp_path / "continous_merged_dict.pkl").exists())


if __name__ == "__main__":
    unittest.main()
