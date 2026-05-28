import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


REPO_ROOT = Path(__file__).resolve().parents[1]


class ChiBinningScriptTest(unittest.TestCase):
    def test_script_completes_on_checked_in_dataset(self):
        script_name = "Part2.1分箱_Chi.py"

        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            shutil.copy(REPO_ROOT / script_name, tmp_path / script_name)
            shutil.copy(REPO_ROOT / "test1.csv", tmp_path / "test1.csv")

            result = subprocess.run(
                [sys.executable, script_name],
                cwd=tmp_path,
                text=True,
                capture_output=True,
                timeout=60,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertGreater(
                (tmp_path / "continous_merged_dict.pkl").stat().st_size,
                0,
            )


if __name__ == "__main__":
    unittest.main()
