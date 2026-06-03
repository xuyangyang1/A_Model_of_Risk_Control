import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ChiBinningScriptTest(unittest.TestCase):
    def test_script_runs_and_writes_continuous_merge_dict(self):
        repo_root = Path(__file__).resolve().parent
        script_name = "Part2.1分箱_Chi.py"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            shutil.copy2(repo_root / script_name, tmp_path / script_name)
            shutil.copy2(repo_root / "test1.csv", tmp_path / "test1.csv")

            result = subprocess.run(
                [sys.executable, script_name],
                cwd=tmp_path,
                text=True,
                capture_output=True,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertTrue((tmp_path / "continous_merged_dict.pkl").exists())


if __name__ == "__main__":
    unittest.main()
