import ast
import unittest
from pathlib import Path


class ChiBinningRegressionTest(unittest.TestCase):
    def test_chimerge_calls_do_not_use_empty_target(self):
        script_path = next(Path(__file__).resolve().parents[1].glob("Part2.1*_Chi.py"))
        tree = ast.parse(script_path.read_text(encoding="utf-8"))
        empty_target_lines = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "ChiMerge":
                continue
            if len(node.args) >= 3 and _is_empty_string(node.args[2]):
                empty_target_lines.append(node.lineno)
            for keyword in node.keywords:
                if keyword.arg == "target" and _is_empty_string(keyword.value):
                    empty_target_lines.append(node.lineno)

        self.assertEqual([], empty_target_lines)


def _is_empty_string(node):
    return isinstance(node, ast.Constant) and node.value == ""


if __name__ == "__main__":
    unittest.main()
