import importlib.util
import pickle
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import TestCase


class Part2ChiWorkflowTest(TestCase):
    def test_script_completes_and_writes_continuous_bin_config(self):
        if importlib.util.find_spec("pandas") is None:
            self.skipTest("pandas is required to run Part2.1 Chi binning workflow")

        repo_root = Path(__file__).resolve().parents[1]
        script_name = "Part2.1分箱_Chi.py"

        with tempfile.TemporaryDirectory() as temp_dir:
            work_dir = Path(temp_dir)
            shutil.copy(repo_root / script_name, work_dir / script_name)
            shutil.copy(repo_root / "test1.csv", work_dir / "test1.csv")

            result = subprocess.run(
                [sys.executable, script_name],
                cwd=work_dir,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=300,
            )

            self.assertEqual(
                0,
                result.returncode,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )

            output_path = work_dir / "continous_merged_dict.pkl"
            self.assertTrue(output_path.exists())
            with output_path.open("rb") as output_file:
                continuous_bins = pickle.load(output_file)

            self.assertIn("V01", continuous_bins)
            self.assertTrue(continuous_bins["V01"])
