import ast
import pathlib
import unittest


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / "Part2.1分箱_Chi.py"


class ChiBinningRegressionTests(unittest.TestCase):
    def _script_text(self):
        return SCRIPT_PATH.read_text(encoding="utf-8")

    def _assign_group(self):
        source = self._script_text()
        tree = ast.parse(source)
        assign_group_node = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "AssignGroup"
        )
        namespace = {}
        exec(ast.get_source_segment(source, assign_group_node), namespace)
        return namespace["AssignGroup"]

    def test_chimerge_calls_never_use_empty_target_column(self):
        tree = ast.parse(self._script_text())

        empty_target_lines = []
        result_target_calls = 0
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
            if isinstance(target_arg, ast.Constant) and target_arg.value == "result":
                result_target_calls += 1

        self.assertEqual(
            empty_target_lines,
            [],
            "ChiMerge must receive the real target column on retry paths.",
        )
        self.assertGreaterEqual(
            result_target_calls,
            4,
            "ChiMerge retry paths must keep using the result target column.",
        )

    def test_assign_group_overflow_bucket_sorts_after_large_values(self):
        assign_group = self._assign_group()
        overflow_bucket = assign_group(10**12, [100, 200, 300])

        self.assertEqual(overflow_bucket, float("inf"))
        self.assertGreater(overflow_bucket, 10**12)

    def test_assign_group_timestamp_overflow_does_not_reorder_bins(self):
        assign_group = self._assign_group()
        split_points = [1.0e12, 1.5e12, 1.7e12]
        mapped = [
            assign_group(0.5e12, split_points),
            assign_group(1.2e12, split_points),
            assign_group(1.6e12, split_points),
            assign_group(2.0e12, split_points),
        ]

        self.assertEqual(mapped[-1], float("inf"))
        self.assertEqual(
            sorted(set(mapped)),
            [1.0e12, 1.5e12, 1.7e12, float("inf")],
        )


if __name__ == "__main__":
    unittest.main()
