import os
import pickle
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_NAME = "Part2.1分箱_Chi.py"
OUTPUT_NAME = "continous_merged_dict.pkl"


class Part2ChiWorkflowTest(unittest.TestCase):
    def test_chi_binning_workflow_completes_and_writes_cutoffs(self):
        output_path = REPO_ROOT / OUTPUT_NAME
        if output_path.exists():
            output_path.unlink()

        try:
            result = subprocess.run(
                [sys.executable, SCRIPT_NAME],
                cwd=REPO_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=300,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}",
            )
            self.assertTrue(output_path.exists())

            with output_path.open("rb") as output_file:
                merged_dict = pickle.load(output_file)

            self.assertIn("V01", merged_dict)
            self.assertGreaterEqual(len(merged_dict["V01"]), 1)
        finally:
            if output_path.exists():
                output_path.unlink()


if __name__ == "__main__":
    unittest.main()
