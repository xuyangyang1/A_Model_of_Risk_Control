import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class Part2ChiRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parents[1]
        cls.script = next(cls.repo_root.glob("Part2.1*_Chi.py"))

    def _load_function_namespace(self):
        script_text = self.script.read_text(encoding="utf-8")
        setup_boundary = script_text.index("trainData = pd.read_csv")
        namespace = {}
        exec(compile(script_text[:setup_boundary], str(self.script), "exec"), namespace)
        return namespace

    def test_assign_group_keeps_large_values_in_top_bucket(self):
        namespace = self._load_function_namespace()
        assign_group = namespace["AssignGroup"]
        split_points = [1_600_000_000_000, 1_650_000_000_000]

        grouped_value = assign_group(1_700_000_000_000, split_points)

        self.assertEqual(float("inf"), grouped_value)
        self.assertGreater(grouped_value, max(split_points))

    def test_checked_in_dataset_chi_workflow_completes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            script_copy = tmp_path / self.script.name
            shutil.copy2(self.script, script_copy)
            shutil.copy2(self.repo_root / "test1.csv", tmp_path / "test1.csv")

            result = subprocess.run(
                [sys.executable, script_copy.name],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                timeout=300,
            )

            self.assertEqual(
                0,
                result.returncode,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertTrue((tmp_path / "continous_merged_dict.pkl").exists())


if __name__ == "__main__":
    unittest.main()
