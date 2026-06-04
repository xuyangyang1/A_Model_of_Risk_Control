import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ChiBinningWorkflowTest(unittest.TestCase):
    def test_checked_in_data_completes_continuous_binning(self):
        repo_root = Path(__file__).resolve().parent
        script_name = "Part2.1分箱_Chi.py"

        with tempfile.TemporaryDirectory() as tmp_dir:
            work_dir = Path(tmp_dir)
            shutil.copy2(repo_root / script_name, work_dir / script_name)
            shutil.copy2(repo_root / "test1.csv", work_dir / "test1.csv")

            result = subprocess.run(
                [sys.executable, script_name],
                cwd=work_dir,
                text=True,
                capture_output=True,
                timeout=120,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn("V01 is in processing", result.stdout)
            self.assertTrue((work_dir / "continous_merged_dict.pkl").exists())


if __name__ == "__main__":
    unittest.main()
