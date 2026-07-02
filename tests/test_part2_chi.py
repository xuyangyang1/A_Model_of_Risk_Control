import math
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHI_SCRIPT = REPO_ROOT / "Part2.1分箱_Chi.py"


def load_chi_functions():
    source = CHI_SCRIPT.read_text(encoding="utf-8")
    function_source = source.split("#读取数据", 1)[0]
    namespace = {}
    exec(compile(function_source, str(CHI_SCRIPT), "exec"), namespace)
    return namespace


class ChiBinningRegressionTests(unittest.TestCase):
    def test_assign_group_overflow_bucket_sorts_after_large_values(self):
        assign_group = load_chi_functions()["AssignGroup"]
        split_points = [1_600_000_000_000, 1_700_000_000_000]

        grouped_values = [
            assign_group(1_500_000_000_000, split_points),
            assign_group(1_650_000_000_000, split_points),
            assign_group(1_800_000_000_000, split_points),
        ]

        self.assertEqual(grouped_values[:2], split_points)
        self.assertTrue(math.isinf(grouped_values[-1]))
        self.assertEqual(grouped_values, sorted(grouped_values))

    def test_monotonic_retry_uses_result_target(self):
        source = CHI_SCRIPT.read_text(encoding="utf-8")

        self.assertNotIn("ChiMerge(trainData, col, '',", source)
        self.assertIn("ChiMerge(trainData, col, 'result',", source)


if __name__ == "__main__":
    unittest.main()
