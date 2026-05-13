import os
import subprocess
import sys
import unittest
from pathlib import Path


class ChiBinningScriptTest(unittest.TestCase):
    def test_script_completes_when_monotonic_retry_is_needed(self):
        repo_root = Path(__file__).resolve().parents[1]
        script_path = repo_root / "Part2.1\u5206\u7bb1_Chi.py"
        output_path = repo_root / "continous_merged_dict.pkl"
        env = os.environ.copy()
        env.setdefault("PYTHONIOENCODING", "utf-8")

        if output_path.exists():
            output_path.unlink()

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=repo_root,
                env=env,
                text=True,
                capture_output=True,
                timeout=180,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=result.stdout + result.stderr,
            )
            self.assertTrue(output_path.exists())
        finally:
            output_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
