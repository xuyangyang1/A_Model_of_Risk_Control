import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "Part2.1分箱_Chi.py"
DATA = ROOT / "test1.csv"


class Part2ChiWorkflowTest(unittest.TestCase):
    def test_full_workflow_writes_continuous_bin_dictionary(self):
        try:
            import pandas  # noqa: F401
        except ModuleNotFoundError:
            self.skipTest("pandas is required to run Part2.1分箱_Chi.py")

        with tempfile.TemporaryDirectory() as tmpdir:
            workdir = Path(tmpdir)
            shutil.copy2(SCRIPT, workdir / SCRIPT.name)
            shutil.copy2(DATA, workdir / DATA.name)

            result = subprocess.run(
                [sys.executable, SCRIPT.name],
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=300,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}",
            )
            self.assertTrue((workdir / "continous_merged_dict.pkl").is_file())


if __name__ == "__main__":
    unittest.main()
