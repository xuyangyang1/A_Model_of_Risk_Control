import subprocess
import sys
import unittest
from pathlib import Path


class ChiBinningScriptTest(unittest.TestCase):
    def test_chi_binning_script_completes(self):
        repo_root = Path(__file__).resolve().parents[1]
        output_file = repo_root / "continous_merged_dict.pkl"
        if output_file.exists():
            output_file.unlink()

        try:
            result = subprocess.run(
                [sys.executable, "Part2.1分箱_Chi.py"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=240,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue(output_file.exists())
        finally:
            if output_file.exists():
                output_file.unlink()


if __name__ == "__main__":
    unittest.main()
