import pickle
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_NAME = "Part2.1分箱_Chi.py"
DATA_NAME = "test1.csv"
OUTPUT_NAME = "continous_merged_dict.pkl"


class Part2ChiWorkflowTest(unittest.TestCase):
    def test_chi_binning_workflow_completes_on_checked_in_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            shutil.copy(REPO_ROOT / SCRIPT_NAME, workdir / SCRIPT_NAME)
            shutil.copy(REPO_ROOT / DATA_NAME, workdir / DATA_NAME)

            result = subprocess.run(
                [sys.executable, SCRIPT_NAME],
                cwd=workdir,
                text=True,
                capture_output=True,
                timeout=300,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg="stdout:\n{}\nstderr:\n{}".format(result.stdout, result.stderr),
            )
            output_path = workdir / OUTPUT_NAME
            self.assertTrue(output_path.exists())
            with output_path.open("rb") as output_file:
                merged_bins = pickle.load(output_file)
            self.assertIn("V01", merged_bins)


if __name__ == "__main__":
    unittest.main()
