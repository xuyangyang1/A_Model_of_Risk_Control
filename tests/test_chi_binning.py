import subprocess
import sys
from pathlib import Path


def test_chi_binning_script_completes():
    repo_root = Path(__file__).resolve().parents[1]
    output_file = repo_root / "continous_merged_dict.pkl"
    if output_file.exists():
        output_file.unlink()

    try:
        result = subprocess.run(
            [sys.executable, "Part2.1分箱_Chi.py"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=60,
        )

        assert result.returncode == 0, result.stdout + result.stderr
        assert output_file.exists()
    finally:
        if output_file.exists():
            output_file.unlink()
