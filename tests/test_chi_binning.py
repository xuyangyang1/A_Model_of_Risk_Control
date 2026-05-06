import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


class ChiBinningScriptTest(unittest.TestCase):
    def test_monotonic_retry_uses_result_target(self):
        repo_root = Path(__file__).resolve().parents[1]
        script_name = "Part2.1分箱_Chi.py"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            shutil.copy(repo_root / script_name, tmp_path / script_name)

            rows = []
            for value in range(30):
                for repeat in range(2):
                    rows.append(
                        {
                            "Unnamed: 0": value * 2 + repeat,
                            "x": value,
                            "result": value % 2,
                        }
                    )
            pd.DataFrame(rows).to_csv(tmp_path / "test1.csv", index=False)

            completed = subprocess.run(
                [sys.executable, script_name],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                timeout=20,
            )

        self.assertEqual(
            completed.returncode,
            0,
            msg=completed.stdout + completed.stderr,
        )


if __name__ == "__main__":
    unittest.main()
