import csv
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = next(ROOT.glob("Part2.1*_Chi.py"))


def load_chi_definitions():
    source = SCRIPT.read_text(encoding="utf-8")
    definitions, _ = source.split("#读取数据", 1)
    namespace = {}
    exec(definitions, namespace)
    return namespace


class ChiBinningRegressionTests(unittest.TestCase):
    def test_assign_group_large_values_stay_above_all_cut_points(self):
        namespace = load_chi_definitions()

        group = namespace["AssignGroup"](10**12, [10, 20, 30])

        self.assertEqual(float("inf"), group)

    def test_non_monotone_retry_uses_result_target_column(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            shutil.copy2(SCRIPT, temp_path / SCRIPT.name)
            with (temp_path / "test1.csv").open("w", newline="") as handle:
                writer = csv.DictWriter(handle, ["Unnamed: 0", "V01", "result"])
                writer.writeheader()
                for idx in range(150):
                    writer.writerow(
                        {
                            "Unnamed: 0": idx,
                            "V01": idx,
                            "result": int(50 <= idx < 100 or idx % 10 == 0),
                        }
                    )

            completed = subprocess.run(
                [sys.executable, SCRIPT.name],
                cwd=temp_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

        self.assertEqual(
            0,
            completed.returncode,
            completed.stdout + completed.stderr,
        )


if __name__ == "__main__":
    unittest.main()
