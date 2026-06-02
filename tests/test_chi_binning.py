import subprocess
import sys
import unittest
from pathlib import Path


class ChiBinningScriptTest(unittest.TestCase):
    def test_script_completes_monotonic_retry_path(self):
        repo_root = Path(__file__).resolve().parents[1]
        output_file = repo_root / "continous_merged_dict.pkl"
        output_file.unlink(missing_ok=True)

        try:
            result = subprocess.run(
                [sys.executable, "Part2.1分箱_Chi.py"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=30,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertTrue(output_file.exists())
        finally:
            output_file.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
