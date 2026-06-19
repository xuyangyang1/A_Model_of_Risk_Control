import ast
import math
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = next(REPO_ROOT.glob("Part2.1*.py"))


def load_function_namespace():
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    module_ast = ast.parse(source)
    definition_nodes = [
        node for node in module_ast.body
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef))
    ]
    definitions_ast = ast.Module(body=definition_nodes, type_ignores=[])
    ast.fix_missing_locations(definitions_ast)

    namespace = {}
    exec(compile(definitions_ast, str(SCRIPT_PATH), "exec"), namespace)
    return namespace


class Part2ChiRegressionTest(unittest.TestCase):
    def test_full_workflow_completes_on_checked_in_data(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            shutil.copy2(SCRIPT_PATH, tmp_path / SCRIPT_PATH.name)
            shutil.copy2(REPO_ROOT / "test1.csv", tmp_path / "test1.csv")

            result = subprocess.run(
                [sys.executable, SCRIPT_PATH.name],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                timeout=300,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=(
                    "Chi binning workflow failed.\n"
                    f"stdout:\n{result.stdout[-4000:]}\n"
                    f"stderr:\n{result.stderr[-4000:]}"
                ),
            )
            self.assertTrue((tmp_path / "continous_merged_dict.pkl").exists())

    def test_assign_group_top_bucket_sorts_after_large_values(self):
        namespace = load_function_namespace()
        assign_group = namespace["AssignGroup"]

        assigned = assign_group(
            1_700_000_000_000,
            [1_000_000_000_000, 1_600_000_000_000],
        )

        self.assertTrue(math.isinf(assigned))
        self.assertGreater(assigned, 1_600_000_000_000)


if __name__ == "__main__":
    unittest.main()
