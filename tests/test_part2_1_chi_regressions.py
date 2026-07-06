import ast
import pathlib
import unittest


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "Part2.1分箱_Chi.py"


class ChiBinningRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))

    def test_non_monotone_retry_uses_result_target(self):
        bad_retry_calls = [
            node
            for node in ast.walk(self.tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "ChiMerge"
            and len(node.args) >= 3
            and isinstance(node.args[2], ast.Constant)
            and node.args[2].value == ""
        ]

        self.assertEqual(
            bad_retry_calls,
            [],
            "ChiMerge retries must pass the result target column, not an empty column name.",
        )

    def test_assign_group_uses_unbounded_top_bucket(self):
        assign_group = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "AssignGroup"
        )

        top_bucket_returns = [
            node.value
            for node in ast.walk(assign_group)
            if isinstance(node, ast.Return)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "float"
        ]

        self.assertTrue(
            any(
                len(call.args) == 1
                and isinstance(call.args[0], ast.Constant)
                and call.args[0].value == "inf"
                for call in top_bucket_returns
            ),
            "AssignGroup should use float('inf') so values above all split points sort last.",
        )


if __name__ == "__main__":
    unittest.main()
