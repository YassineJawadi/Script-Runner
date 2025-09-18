import os
from robot.api import ExecutionResult

def analyze_result(results_dir):
    """
    Parse Robot Framework's output.xml and extract useful stats.
    """
    output_file = os.path.join(results_dir, "output.xml")
    if not os.path.exists(output_file):
        return None

    result = ExecutionResult(output_file)

    # Correct way: use suite/statistics attributes directly
    stats = {
        "total": result.suite.statistics.total,
        "passed": result.suite.statistics.passed,
        "failed": result.suite.statistics.failed,
        "elapsed_ms": result.suite.elapsedtime
    }
    return stats
