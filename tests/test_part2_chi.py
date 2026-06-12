import pickle
import subprocess
import sys
import unittest
from pathlib import Path


class Part2ChiWorkflowTest(unittest.TestCase):
    def test_chi_binning_script_completes_and_writes_bins(self):
        repo_root = Path(__file__).resolve().parents[1]
        output_path = repo_root / "continous_merged_dict.pkl"
        script_path = next(
            path
            for path in repo_root.iterdir()
            if path.name.startswith("Part2.1") and path.name.endswith("_Chi.py")
        )

        output_path.unlink(missing_ok=True)
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=repo_root,
                text=True,
                capture_output=True,
                timeout=300,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertTrue(output_path.exists())
            with output_path.open("rb") as output_file:
                merged_bins = pickle.load(output_file)
            self.assertIn("V01", merged_bins)
            self.assertIsInstance(merged_bins["V01"], list)
        finally:
            output_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
