import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class Part2ChiWorkflowTest(unittest.TestCase):
    def test_chi_binning_workflow_completes(self):
        repo_root = Path(__file__).resolve().parents[1]
        script_path = next(repo_root.glob("Part2.1*_Chi.py"))

        with tempfile.TemporaryDirectory() as temp_dir:
            work_dir = Path(temp_dir)
            shutil.copy2(script_path, work_dir / script_path.name)
            shutil.copy2(repo_root / "test1.csv", work_dir / "test1.csv")

            result = subprocess.run(
                [sys.executable, script_path.name],
                cwd=work_dir,
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
            self.assertTrue((work_dir / "continous_merged_dict.pkl").exists())


if __name__ == "__main__":
    unittest.main()
