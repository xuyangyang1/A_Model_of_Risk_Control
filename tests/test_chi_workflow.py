import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ChiWorkflowTest(unittest.TestCase):
    def test_full_workflow_completes_when_monotonic_retry_is_needed(self):
        repo_root = Path(__file__).resolve().parents[1]
        script_name = "Part2.1分箱_Chi.py"

        with tempfile.TemporaryDirectory() as tmpdir:
            workdir = Path(tmpdir)
            shutil.copy(repo_root / script_name, workdir / script_name)
            shutil.copy(repo_root / "test1.csv", workdir / "test1.csv")

            result = subprocess.run(
                [sys.executable, script_name],
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}",
            )
            self.assertTrue((workdir / "continous_merged_dict.pkl").exists())


if __name__ == "__main__":
    unittest.main()
