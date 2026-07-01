import ast
import pathlib
import unittest


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / "Part2.1分箱_Chi.py"


def _parse_script():
    return ast.parse(SCRIPT_PATH.read_text(encoding="utf-8"), filename=str(SCRIPT_PATH))


class Part2ChiRegressionTests(unittest.TestCase):
    def test_chimerge_calls_do_not_use_empty_target(self):
        tree = _parse_script()
        literal_targets = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "ChiMerge":
                continue
            if len(node.args) >= 3 and isinstance(node.args[2], ast.Constant):
                literal_targets.append((node.lineno, node.args[2].value))

        self.assertNotIn(
            "",
            [target for _, target in literal_targets],
            "ChiMerge must receive the real target column when retrying bins",
        )

    def test_assign_group_upper_bucket_sorts_after_large_split_points(self):
        tree = _parse_script()
        assign_group_defs = [
            node for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "AssignGroup"
        ]
        self.assertEqual(len(assign_group_defs), 1)

        module = ast.Module(body=assign_group_defs, type_ignores=[])
        ast.fix_missing_locations(module)
        namespace = {}
        exec(compile(module, str(SCRIPT_PATH), "exec"), namespace)

        split_points = [1_500_000_000_000, 1_600_000_000_000]
        upper_group = namespace["AssignGroup"](2_000_000_000_000, split_points)

        self.assertGreater(upper_group, max(split_points))
        self.assertEqual(upper_group, float("inf"))


if __name__ == "__main__":
    unittest.main()
