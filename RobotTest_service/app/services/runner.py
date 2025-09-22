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

    results_dir = os.path.join("app", "test_results", f"test_{test.id}")
    os.makedirs(results_dir, exist_ok=True)

    try:
        # Normalize test file path
        test_file = os.path.abspath(os.path.normpath(test.file_path))

        result = subprocess.run(
            ["robot", "--outputdir", results_dir, test_file],
            capture_output=True, text=True
        )

        test.status = TestStatus.SUCCESS if result.returncode == 0 else TestStatus.FAILED
        test.log_path = os.path.join(results_dir, "log.html")

        # Analyze stats
        stats = analyze_result(results_dir)
        if stats:
            test.total = stats["total"]
            test.passed = stats["passed"]
            test.failed = stats["failed"]
            test.elapsed_ms = stats["elapsed_ms"]

        # --- Save artifacts into DB ---
        try:
            with open(os.path.join(results_dir, "output.xml"), "r", encoding="utf-8") as f:
                test.output_xml = f.read()
        except FileNotFoundError:
            test.output_xml = None

        try:
            with open(os.path.join(results_dir, "report.html"), "r", encoding="utf-8") as f:
                test.report_html = f.read()
        except FileNotFoundError:
            test.report_html = None

        debug_file = os.path.join(results_dir, "debug_output.txt")
        with open(debug_file, "w", encoding="utf-8") as f:
            f.write("STDOUT:\n" + result.stdout + "\n")
            f.write("STDERR:\n" + result.stderr + "\n")

        with open(debug_file, "r", encoding="utf-8") as f:
            test.debug_text = f.read()

    except Exception as e:
        test.status = TestStatus.FAILED
        test.log_path = str(e)

    test.finished_at = datetime.utcnow()
    db.session.commit()
    return test
