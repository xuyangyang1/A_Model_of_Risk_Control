import ast
from pathlib import Path
import unittest


class ChiBinningScriptTests(unittest.TestCase):
    def test_chimerge_calls_do_not_use_empty_target(self):
        source_path = Path(__file__).resolve().parents[1] / "Part2.1分箱_Chi.py"
        tree = ast.parse(source_path.read_text(encoding="utf-8"))

        empty_target_calls = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "ChiMerge":
                continue
            if len(node.args) >= 3 and isinstance(node.args[2], ast.Constant) and node.args[2].value == "":
                empty_target_calls.append(node.lineno)

        self.assertEqual([], empty_target_calls)


if __name__ == "__main__":
    unittest.main()
