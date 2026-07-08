import ast
import math
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHI_SCRIPT = next(ROOT.glob("Part2.1*_Chi.py"))


def load_chi_definitions():
    source = CHI_SCRIPT.read_text(encoding="utf-8")
    parsed = ast.parse(source, filename=str(CHI_SCRIPT))
    definition_nodes = [
        node
        for node in parsed.body
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef))
    ]
    module = ast.Module(body=definition_nodes, type_ignores=[])
    ast.fix_missing_locations(module)

    namespace = {"__name__": "chi_definitions_under_test"}
    exec(compile(module, str(CHI_SCRIPT), "exec"), namespace)
    return namespace, parsed


class ChiBinningRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.namespace, cls.parsed_script = load_chi_definitions()

    def test_assign_group_keeps_values_above_last_split_in_top_bucket(self):
        assign_group = self.namespace["AssignGroup"]
        split_points = [10**12, 2 * 10**12]

        self.assertEqual(assign_group(5 * 10**11, split_points), 10**12)
        self.assertEqual(assign_group(15 * 10**11, split_points), 2 * 10**12)

        top_bucket = assign_group(3 * 10**12, split_points)
        self.assertTrue(math.isinf(top_bucket))
        self.assertGreater(top_bucket, max(split_points))

    def test_chimerge_calls_never_use_empty_target_column(self):
        empty_target_lines = []
        for node in ast.walk(self.parsed_script):
            if not isinstance(node, ast.Call):
                continue
            if getattr(node.func, "id", None) != "ChiMerge":
                continue
            if len(node.args) < 3:
                continue
            target_arg = node.args[2]
            if isinstance(target_arg, ast.Constant) and target_arg.value == "":
                empty_target_lines.append(node.lineno)

        self.assertEqual(
            empty_target_lines,
            [],
            "ChiMerge needs a real target column on every path",
        )


if __name__ == "__main__":
    unittest.main()
