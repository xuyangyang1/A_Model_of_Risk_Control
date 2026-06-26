import ast
import math
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_NAME = 'Part2.1分箱_Chi.py'
SCRIPT_PATH = REPO_ROOT / SCRIPT_NAME


def load_script_functions():
    source = SCRIPT_PATH.read_text(encoding='utf-8')
    tree = ast.parse(source, filename=str(SCRIPT_PATH))
    tree.body = [
        node for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef))
    ]
    namespace = {}
    exec(compile(tree, str(SCRIPT_PATH), 'exec'), namespace)
    return namespace


class Part2ChiRegressionTests(unittest.TestCase):
    def test_assign_group_uses_unbounded_top_bucket(self):
        namespace = load_script_functions()
        assign_group = namespace['AssignGroup']

        self.assertEqual(assign_group(2, [1, 3, 5]), 3)
        self.assertTrue(math.isinf(assign_group(10**12, [1, 3, 5])))

    def test_bundled_workflow_completes_monotonic_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            shutil.copy(SCRIPT_PATH, tmp_path / SCRIPT_NAME)
            shutil.copy(REPO_ROOT / 'test1.csv', tmp_path / 'test1.csv')

            proc = subprocess.run(
                [sys.executable, SCRIPT_NAME],
                cwd=tmp_path,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=300,
            )

            self.assertEqual(
                proc.returncode,
                0,
                msg='stdout:\n{}\nstderr:\n{}'.format(proc.stdout, proc.stderr),
            )
            self.assertTrue((tmp_path / 'continous_merged_dict.pkl').exists())


if __name__ == '__main__':
    unittest.main()
