import ast
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ChiBinningScriptTest(unittest.TestCase):
    def test_chi_merge_calls_include_target_column(self):
        script_path = REPO_ROOT / "Part2.1分箱_Chi.py"
        tree = ast.parse(script_path.read_text(encoding="utf-8"))

        empty_target_lines = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "ChiMerge":
                continue
            if len(node.args) >= 3 and isinstance(node.args[2], ast.Constant):
                if node.args[2].value == "":
                    empty_target_lines.append(node.lineno)

        self.assertEqual(empty_target_lines, [])


if __name__ == "__main__":
    unittest.main()
