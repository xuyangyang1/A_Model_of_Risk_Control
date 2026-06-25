import ast
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHI_SCRIPT = next(REPO_ROOT.glob("Part2.1*_Chi.py"))


def load_function(function_name):
    source = CHI_SCRIPT.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(CHI_SCRIPT))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            module = ast.Module(body=[node], type_ignores=[])
            namespace = {}
            exec(compile(ast.fix_missing_locations(module), str(CHI_SCRIPT), "exec"), namespace)
            return namespace[function_name]
    raise AssertionError("{} was not found".format(function_name))


class Part2ChiRegressionTest(unittest.TestCase):
    def test_assign_group_top_bucket_sorts_after_large_split_points(self):
        assign_group = load_function("AssignGroup")

        split_points = [1_600_000_000_000, 1_700_000_000_000]
        top_bucket = assign_group(1_800_000_000_000, split_points)

        self.assertGreater(top_bucket, max(split_points))

    def test_checked_in_workflow_completes_and_writes_bin_dictionary(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            shutil.copy(REPO_ROOT / "test1.csv", tmp_path / "test1.csv")

            completed = subprocess.run(
                [sys.executable, str(CHI_SCRIPT)],
                cwd=tmp_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300,
            )

            if completed.returncode != 0:
                self.fail(
                    "Part2.1 Chi workflow failed with exit code {}.\nSTDOUT:\n{}\nSTDERR:\n{}".format(
                        completed.returncode, completed.stdout, completed.stderr
                    )
                )
            self.assertTrue((tmp_path / "continous_merged_dict.pkl").exists())


if __name__ == "__main__":
    unittest.main()
