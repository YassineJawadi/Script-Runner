from datetime import datetime
from . import db
import enum
from sqlalchemy.dialects.mysql import LONGTEXT

class TestStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class RobotTest(db.Model):
    __tablename__ = "robot_tests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(TestStatus), default=TestStatus.PENDING, nullable=False)
    log_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)

    # --- analyzer fields ---
    total = db.Column(db.Integer, default=0)       # total test cases
    passed = db.Column(db.Integer, default=0)      # passed cases
    failed = db.Column(db.Integer, default=0)      # failed cases
    elapsed_ms = db.Column(db.Integer, default=0)  # execution time in ms

    # --- NEW fields to store artifacts as text ---
    output_xml = db.Column(LONGTEXT)
    report_html = db.Column(LONGTEXT)
    debug_text = db.Column(LONGTEXT)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "file_path": self.file_path,
            "status": self.status.value,
            "log_path": self.log_path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "elapsed_ms": self.elapsed_ms,
            # don’t dump huge HTML/XML directly
            "has_output_xml": bool(self.output_xml),
            "has_report_html": bool(self.report_html),
            "has_debug_text": bool(self.debug_text),
        }
