import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "Part2.1分箱_Chi.py"
OUTPUT = ROOT / "continous_merged_dict.pkl"


class Part2ChiWorkflowTest(unittest.TestCase):
    def tearDown(self):
        OUTPUT.unlink(missing_ok=True)

    def test_chi_binning_workflow_completes(self):
        OUTPUT.unlink(missing_ok=True)

        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,
        )

        self.assertEqual(
            completed.returncode,
            0,
            msg=(
                "Part2.1 Chi binning script failed.\n"
                f"stdout:\n{completed.stdout}\n"
                f"stderr:\n{completed.stderr}"
            ),
        )
        self.assertTrue(OUTPUT.exists(), "expected Chi binning output pickle to be written")


if __name__ == "__main__":
    unittest.main()
