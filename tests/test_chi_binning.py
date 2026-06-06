import pickle
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "Part2.1分箱_Chi.py"


class ChiBinningWorkflowTest(unittest.TestCase):
    def test_continuous_retry_path_completes_and_writes_cutoffs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workdir = Path(tmpdir)
            shutil.copy2(ROOT / SCRIPT, workdir / SCRIPT)
            shutil.copy2(ROOT / "test1.csv", workdir / "test1.csv")

            result = subprocess.run(
                [sys.executable, SCRIPT],
                cwd=workdir,
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
            output = workdir / "continous_merged_dict.pkl"
            self.assertTrue(output.exists())

            with output.open("rb") as fh:
                cutoffs = pickle.load(fh)

            self.assertIn("V01", cutoffs)
            self.assertIsInstance(cutoffs["V01"], list)


if __name__ == "__main__":
    unittest.main()
