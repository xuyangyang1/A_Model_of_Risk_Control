import ast
import pathlib
import unittest


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / "Part2.1分箱_Chi.py"


class ChiBinningRegressionTests(unittest.TestCase):
    def _script_text(self):
        return SCRIPT_PATH.read_text(encoding="utf-8")

    def test_chimerge_calls_never_use_empty_target_column(self):
        tree = ast.parse(self._script_text())

        empty_target_lines = []
        for node in ast.walk(tree):
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

    def test_assign_group_overflow_bucket_sorts_after_large_values(self):
        source = self._script_text()
        tree = ast.parse(source)
        assign_group_node = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "AssignGroup"
        )
        namespace = {}
        exec(ast.get_source_segment(source, assign_group_node), namespace)

        overflow_bucket = namespace["AssignGroup"](10**12, [100, 200, 300])

        self.assertEqual(overflow_bucket, float("inf"))
        self.assertGreater(overflow_bucket, 10**12)


if __name__ == "__main__":
    unittest.main()
