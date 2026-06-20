import ast
import importlib.util
import math
import pickle
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "Part2.1分箱_Chi.py"
DATA = REPO_ROOT / "test1.csv"


def load_function(function_name):
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == function_name
    ]
    if len(functions) != 1:
        raise AssertionError(f"Expected exactly one {function_name} function")

    namespace = {}
    module = ast.Module(body=functions, type_ignores=[])
    ast.fix_missing_locations(module)
    exec(compile(module, str(SCRIPT), "exec"), namespace)
    return namespace[function_name]


class Part2ChiRegressionTests(unittest.TestCase):
    def test_assign_group_keeps_values_above_large_split_points_last(self):
        assign_group = load_function("AssignGroup")

        split_points = [1_700_000_000_000, 1_800_000_000_000]
        assigned_group = assign_group(1_900_000_000_000, split_points)

        self.assertTrue(math.isinf(assigned_group))
        self.assertGreater(assigned_group, split_points[-1])

    def test_chi_merge_retry_never_uses_empty_target(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))
        empty_target_calls = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "ChiMerge":
                continue
            if len(node.args) >= 3 and isinstance(node.args[2], ast.Constant):
                if node.args[2].value == "":
                    empty_target_calls.append(node.lineno)

        self.assertEqual([], empty_target_calls)

    @unittest.skipUnless(
        importlib.util.find_spec("pandas"),
        "pandas is required to run the checked-in Chi workflow",
    )
    def test_checked_in_dataset_completes_chi_binning_workflow(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            shutil.copy2(SCRIPT, temp_path / SCRIPT.name)
            shutil.copy2(DATA, temp_path / DATA.name)

            result = subprocess.run(
                [sys.executable, SCRIPT.name],
                cwd=temp_path,
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode != 0:
                self.fail(
                    "Chi binning workflow failed\n"
                    f"stdout:\n{result.stdout}\n"
                    f"stderr:\n{result.stderr}"
                )

            output_path = temp_path / "continous_merged_dict.pkl"
            self.assertTrue(output_path.exists())
            with output_path.open("rb") as output_file:
                self.assertTrue(pickle.load(output_file))


if __name__ == "__main__":
    unittest.main()
