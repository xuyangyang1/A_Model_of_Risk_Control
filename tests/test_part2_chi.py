import pickle
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_NAME = "Part2.1分箱_Chi.py"
DATA_NAME = "test1.csv"


class ChiBinningWorkflowTest(unittest.TestCase):
    def test_continuous_retry_uses_result_target_column(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            shutil.copy2(ROOT / SCRIPT_NAME, tmp_path / SCRIPT_NAME)
            shutil.copy2(ROOT / DATA_NAME, tmp_path / DATA_NAME)

            completed = subprocess.run(
                [sys.executable, SCRIPT_NAME],
                cwd=tmp_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300,
            )

            self.assertEqual(
                completed.returncode,
                0,
                msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            output_path = tmp_path / "continous_merged_dict.pkl"
            self.assertTrue(output_path.exists())
            with output_path.open("rb") as output_file:
                merged_bins = pickle.load(output_file)
            self.assertIn("V01", merged_bins)


if __name__ == "__main__":
    unittest.main()
