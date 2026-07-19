import ast
import pathlib
import unittest


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / "Part2.1分箱_Chi.py"


class ChiBinningRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SCRIPT_PATH.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)

    def test_assign_group_keeps_large_values_in_the_top_bucket(self):
        assign_group_node = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "AssignGroup"
        )
        namespace = {}
        exec(ast.get_source_segment(self.source, assign_group_node), namespace)
        assign_group = namespace["AssignGroup"]

        split_points = [10**12, 2 * 10**12]
        self.assertEqual(assign_group(5 * 10**11, split_points), 10**12)
        self.assertEqual(assign_group(15 * 10**11, split_points), 2 * 10**12)

        top_bucket = assign_group(3 * 10**12, split_points)
        self.assertEqual(top_bucket, float("inf"))
        self.assertGreater(top_bucket, max(split_points))

    def test_chimerge_calls_never_use_an_empty_target_column(self):
        empty_target_lines = []
        for node in ast.walk(self.tree):
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
            "ChiMerge must receive the real target column on retry paths.",
        )


if __name__ == "__main__":
    unittest.main()
