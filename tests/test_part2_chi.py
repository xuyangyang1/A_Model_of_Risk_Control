import ast
import math
import pathlib
import unittest


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / "Part2.1分箱_Chi.py"


def _script_tree():
    return ast.parse(SCRIPT_PATH.read_text(encoding="utf-8"))


def _load_function(function_name):
    tree = _script_tree()
    function_defs = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == function_name
    ]
    if len(function_defs) != 1:
        raise AssertionError(f"Expected exactly one {function_name} definition")

    module = ast.Module(body=function_defs, type_ignores=[])
    ast.fix_missing_locations(module)
    namespace = {}
    exec(compile(module, str(SCRIPT_PATH), "exec"), namespace)
    return namespace[function_name]


class Part2ChiRegressionTests(unittest.TestCase):
    def test_assign_group_uses_unbounded_top_bucket(self):
        assign_group = _load_function("AssignGroup")

        self.assertEqual(assign_group(5, [10, 20]), 10)
        self.assertEqual(assign_group(15, [10, 20]), 20)
        self.assertTrue(math.isinf(assign_group(30, [10, 20])))

    def test_chi_merge_calls_never_use_empty_target(self):
        for node in ast.walk(_script_tree()):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "ChiMerge":
                continue
            if len(node.args) >= 3 and isinstance(node.args[2], ast.Constant):
                self.assertNotEqual(
                    node.args[2].value,
                    "",
                    "ChiMerge must receive the result target column during retries",
                )


if __name__ == "__main__":
    unittest.main()
