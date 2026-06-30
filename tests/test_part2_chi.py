import ast
import math
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / 'Part2.1分箱_Chi.py'


def load_function(name):
    tree = ast.parse(SCRIPT_PATH.read_text(encoding='utf-8'))
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if not functions:
        raise AssertionError(f'{name} not found in {SCRIPT_PATH.name}')

    namespace = {}
    module = ast.Module(body=functions, type_ignores=[])
    ast.fix_missing_locations(module)
    exec(compile(module, str(SCRIPT_PATH), 'exec'), namespace)
    return namespace[name]


class Part2ChiRegressionTests(unittest.TestCase):
    def test_assign_group_uses_unbounded_top_bucket(self):
        assign_group = load_function('AssignGroup')

        top_bucket = assign_group(200_000_000_000, [1, 2, 3])

        self.assertTrue(math.isinf(top_bucket))
        self.assertGreater(top_bucket, 200_000_000_000)

    def test_chimerge_calls_never_use_empty_target(self):
        tree = ast.parse(SCRIPT_PATH.read_text(encoding='utf-8'))
        empty_target_calls = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != 'ChiMerge':
                continue
            if len(node.args) >= 3 and isinstance(node.args[2], ast.Constant) and node.args[2].value == '':
                empty_target_calls.append(node.lineno)

        self.assertEqual([], empty_target_calls)


if __name__ == '__main__':
    unittest.main()
