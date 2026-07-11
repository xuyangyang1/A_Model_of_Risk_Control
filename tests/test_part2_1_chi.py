import ast
import math
import pathlib
import unittest


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / "Part2.1分箱_Chi.py"


def _parse_script():
    return ast.parse(SCRIPT_PATH.read_text(encoding="utf-8"))


def _load_function(name):
    tree = _parse_script()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            module = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(module)
            namespace = {}
            exec(compile(module, str(SCRIPT_PATH), "exec"), namespace)
            return namespace[name]
    raise AssertionError(f"{name} not found in {SCRIPT_PATH}")


class ChiBinningRegressionTests(unittest.TestCase):
    def test_assign_group_uses_unbounded_upper_bucket(self):
        assign_group = _load_function("AssignGroup")

        upper_bucket = assign_group(10**12, [1, 2, 3])

        self.assertTrue(math.isinf(upper_bucket))

    def test_chi_merge_calls_never_use_empty_target_column(self):
        tree = _parse_script()

        empty_target_calls = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "ChiMerge":
                continue
            if len(node.args) >= 3 and isinstance(node.args[2], ast.Constant) and node.args[2].value == "":
                empty_target_calls.append(node.lineno)

        self.assertEqual(empty_target_calls, [])


if __name__ == "__main__":
    unittest.main()
