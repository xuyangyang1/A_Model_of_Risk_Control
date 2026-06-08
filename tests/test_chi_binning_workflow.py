import pickle
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ChiBinningWorkflowTest(unittest.TestCase):
    def test_chi_binning_script_completes_on_checked_in_data(self):
        repo_root = Path(__file__).resolve().parents[1]
        script_name = "Part2.1分箱_Chi.py"

        with tempfile.TemporaryDirectory() as tmpdir:
            workdir = Path(tmpdir)
            shutil.copy(repo_root / script_name, workdir / script_name)
            shutil.copy(repo_root / "test1.csv", workdir / "test1.csv")

            result = subprocess.run(
                [sys.executable, script_name],
                cwd=workdir,
                text=True,
                capture_output=True,
                timeout=300,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}",
            )

            output_path = workdir / "continous_merged_dict.pkl"
            self.assertTrue(output_path.exists())
            with output_path.open("rb") as output_file:
                continuous_bins = pickle.load(output_file)

            self.assertIn("V01", continuous_bins)
            self.assertIsInstance(continuous_bins["V01"], list)


if __name__ == "__main__":
    unittest.main()
