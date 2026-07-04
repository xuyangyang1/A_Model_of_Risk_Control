import math
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHI_SCRIPT = REPO_ROOT / "Part2.1分箱_Chi.py"


def load_chi_helpers():
    source = CHI_SCRIPT.read_text(encoding="utf-8")
    helper_source = source.split("#读取数据", 1)[0]
    namespace = {}
    exec(compile(helper_source, str(CHI_SCRIPT), "exec"), namespace)
    return namespace


class ChiBinningRegressionTests(unittest.TestCase):
    def test_assign_group_uses_unbounded_tail_bucket(self):
        helpers = load_chi_helpers()

        result = helpers["AssignGroup"](10**12, [10, 20, 30])

        self.assertTrue(math.isinf(result))

    def test_full_chi_workflow_completes_on_checked_in_dataset(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            shutil.copy(CHI_SCRIPT, tmp_path / CHI_SCRIPT.name)
            shutil.copy(REPO_ROOT / "test1.csv", tmp_path / "test1.csv")

            proc = subprocess.run(
                [sys.executable, CHI_SCRIPT.name],
                cwd=tmp_path,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=300,
            )

            self.assertEqual(proc.returncode, 0, proc.stdout)
            self.assertTrue((tmp_path / "continous_merged_dict.pkl").exists())


if __name__ == "__main__":
    unittest.main()
