import ast
import pathlib
import unittest


class ChiMergeRetryTargetTest(unittest.TestCase):
    def test_chimerge_calls_never_use_empty_target(self):
        script = pathlib.Path(__file__).resolve().parents[1] / "Part2.1分箱_Chi.py"
        tree = ast.parse(script.read_text(encoding="utf-8"))

        empty_target_lines = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "ChiMerge":
                continue
            if len(node.args) >= 3 and isinstance(node.args[2], ast.Constant) and node.args[2].value == "":
                empty_target_lines.append(node.lineno)
            for keyword in node.keywords:
                if (
                    keyword.arg == "target"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value == ""
                ):
                    empty_target_lines.append(node.lineno)

        self.assertEqual([], empty_target_lines)


if __name__ == "__main__":
    unittest.main()
