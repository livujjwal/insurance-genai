import logging
import re
import sys
from contextvars import ContextVar

# ContextVar for tracing request across async tasks
request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="")

# PII Patterns for masking
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_PATTERN = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
CARD_PATTERN = re.compile(r"\b(?:\d{4}[- ]?){3}\d{4}\b")


def mask_pii(text: str) -> str:
    """Mask sensitive PII patterns (emails, phone numbers, card numbers) from log messages."""
    if not isinstance(text, str):
        return text
    masked = EMAIL_PATTERN.sub("[EMAIL_MASKED]", text)
    masked = PHONE_PATTERN.sub("[PHONE_MASKED]", masked)
    masked = CARD_PATTERN.sub("[CARD_MASKED]", masked)
    return masked


class StructuredLogFormatter(logging.Formatter):
    """Custom log formatter that includes request_id and masks PII."""

    def format(self, record: logging.LogRecord) -> str:
        req_id = request_id_ctx_var.get()
        record.request_id = req_id if req_id else "-"
        # Format base message
        orig_msg = record.getMessage()
        record.msg = mask_pii(orig_msg)
        record.args = None  # prevent re-formatting in parent
        return super().format(record)


def setup_logging(level: str = "INFO") -> None:
    """Configure root logger with structured formatting."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Avoid duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = StructuredLogFormatter(
            fmt="%(asctime)s [%(levelname)s] [req_id=%(request_id)s] [%(name)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        for existing_h in logger.handlers:
            formatter = StructuredLogFormatter(
                fmt="%(asctime)s [%(levelname)s] [req_id=%(request_id)s] [%(name)s:%(lineno)d] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            existing_h.setFormatter(formatter)
