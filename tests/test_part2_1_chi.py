import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHI_SCRIPT = PROJECT_ROOT / "Part2.1分箱_Chi.py"


def test_chi_merge_calls_never_use_empty_target_column():
    tree = ast.parse(CHI_SCRIPT.read_text(encoding="utf-8"))

    empty_target_calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "ChiMerge":
            continue
        if len(node.args) < 3:
            continue
        target_arg = node.args[2]
        if isinstance(target_arg, ast.Constant) and target_arg.value == "":
            empty_target_calls.append(node.lineno)

    assert empty_target_calls == []
