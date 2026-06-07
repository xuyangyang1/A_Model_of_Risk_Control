import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ChiBinningWorkflowTest(unittest.TestCase):
    def test_chi_binning_script_completes_after_monotonic_retry(self):
        repo_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            script_name = "Part2.1分箱_Chi.py"
            shutil.copyfile(repo_root / script_name, tmp_path / script_name)
            shutil.copyfile(repo_root / "test1.csv", tmp_path / "test1.csv")

            result = subprocess.run(
                [sys.executable, script_name],
                cwd=tmp_path,
                text=True,
                capture_output=True,
                timeout=300,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((tmp_path / "continous_merged_dict.pkl").exists())


if __name__ == "__main__":
    unittest.main()
