import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent
SCRIPT = next(ROOT.glob("Part2.1*_Chi.py"))
DATA = ROOT / "test1.csv"


class ChiBinningScriptTest(unittest.TestCase):
    @unittest.skipIf(
        importlib.util.find_spec("pandas") is None
        or importlib.util.find_spec("numpy") is None,
        "pandas and numpy are required to run the binning script",
    )
    def test_chi_binning_script_runs_on_checked_in_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            shutil.copy2(SCRIPT, temp_path / SCRIPT.name)
            shutil.copy2(DATA, temp_path / DATA.name)

            result = subprocess.run(
                [sys.executable, SCRIPT.name],
                cwd=temp_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=120,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertTrue((temp_path / "continous_merged_dict.pkl").exists())


if __name__ == "__main__":
    unittest.main()
