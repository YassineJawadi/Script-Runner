import os
import subprocess
from datetime import datetime
from app import db
from app.models import RobotTest, TestStatus
from app.services.analyzer import analyze_result


def run_robot_test(test: RobotTest):
    """Execute Robot Framework test and update DB status + stats"""
    test.status = TestStatus.RUNNING
    db.session.commit()

    # Results directory under app/test_results/test_<id>
    results_dir = os.path.join("app", "test_results", f"test_{test.id}")
    os.makedirs(results_dir, exist_ok=True)

    try:
        # ✅ Fix: test.file_path already includes "robot_tests/"
        if not os.path.isabs(test.file_path):
            test_file = test.file_path
        else:
            test_file = test.file_path

        # Normalize path (cross-platform safe)
        test_file = os.path.abspath(os.path.normpath(test_file))

        result = subprocess.run(
            ["robot", "--outputdir", results_dir, test_file],
            capture_output=True, text=True
        )

        # Update status
        test.status = TestStatus.SUCCESS if result.returncode == 0 else TestStatus.FAILED
        test.log_path = os.path.join(results_dir, "log.html")

        # Analyze results
        stats = analyze_result(results_dir)
        if stats:
            test.total = stats["total"]
            test.passed = stats["passed"]
            test.failed = stats["failed"]
            test.elapsed_ms = stats["elapsed_ms"]

        # Save raw stdout/stderr for debugging
        debug_file = os.path.join(results_dir, "debug_output.txt")
        with open(debug_file, "w", encoding="utf-8") as f:
            f.write("STDOUT:\n" + result.stdout + "\n")
            f.write("STDERR:\n" + result.stderr + "\n")

    except Exception as e:
        test.status = TestStatus.FAILED
        test.log_path = str(e)

    test.finished_at = datetime.utcnow()
    db.session.commit()

    return test
