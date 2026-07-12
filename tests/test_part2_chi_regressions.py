import ast
import math
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
CHI_SCRIPT = ROOT / "Part2.1分箱_Chi.py"


def _parse_chi_script():
    return ast.parse(CHI_SCRIPT.read_text(encoding="utf-8"), filename=str(CHI_SCRIPT))


def _load_function(function_name):
    tree = _parse_chi_script()
    functions = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == function_name
    ]
    if len(functions) != 1:
        raise AssertionError(f"Expected one {function_name} definition, found {len(functions)}")

    module = ast.Module(body=functions, type_ignores=[])
    ast.fix_missing_locations(module)
    namespace = {}
    exec(compile(module, str(CHI_SCRIPT), "exec"), namespace)
    return namespace[function_name]


class ChiBinningRegressionTests(unittest.TestCase):
    def test_continuous_monotone_retry_keeps_target_column(self):
        tree = _parse_chi_script()
        empty_target_lines = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "ChiMerge":
                continue
            if len(node.args) < 3:
                continue
            target_arg = node.args[2]
            if isinstance(target_arg, ast.Constant) and target_arg.value == "":
                empty_target_lines.append(node.lineno)

        self.assertEqual([], empty_target_lines)

    def test_assign_group_overflow_is_above_large_split_points(self):
        assign_group = _load_function("AssignGroup")
        split_points = [10**12, 2 * 10**12, 3 * 10**12]

        overflow_group = assign_group(4 * 10**12, split_points)

        self.assertTrue(math.isinf(overflow_group))
        self.assertGreater(overflow_group, max(split_points))


if __name__ == "__main__":
    unittest.main()
