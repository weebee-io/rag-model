# model-service/app/core/logger.py

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

BASE_LOG_DIR = Path("/var/log/fastapi")
BASE_LOG_DIR.mkdir(parents=True, exist_ok=True)

# QA 전용 로그 설정
QA_LOG_DIR = BASE_LOG_DIR / "qa"
QA_LOG_DIR.mkdir(parents=True, exist_ok=True)
qa_logger = logging.getLogger("qa_logger")
qa_logger.setLevel(logging.INFO)
qa_handler = TimedRotatingFileHandler(
    filename=QA_LOG_DIR / "qa_request_response.log",
    when="midnight",
    interval=1,
    encoding="utf-8",
    backupCount=7,
)
qa_formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
qa_handler.setFormatter(qa_formatter)
qa_logger.addHandler(qa_handler)

# News 전용 로그 설정
NEWS_LOG_DIR = BASE_LOG_DIR / "news"
NEWS_LOG_DIR.mkdir(parents=True, exist_ok=True)
news_logger = logging.getLogger("news_logger")
news_logger.setLevel(logging.INFO)
news_handler = TimedRotatingFileHandler(
    filename=NEWS_LOG_DIR / "news_request_response.log",
    when="midnight",
    interval=1,
    encoding="utf-8",
    backupCount=7,
)
news_formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
news_handler.setFormatter(news_formatter)
news_logger.addHandler(news_handler)

# Hint 전용 로그 설정
HINT_LOG_DIR = BASE_LOG_DIR / "hint"
HINT_LOG_DIR.mkdir(parents=True, exist_ok=True)
hint_logger = logging.getLogger("hint_logger")
hint_logger.setLevel(logging.INFO)
hint_handler = TimedRotatingFileHandler(
    filename=HINT_LOG_DIR / "hint_request_response.log",
    when="midnight",
    interval=1,
    encoding="utf-8",
    backupCount=7,
)
hint_formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
hint_handler.setFormatter(hint_formatter)
hint_logger.addHandler(hint_handler)

# 기타(General) 로그 설정
GENERAL_LOG_DIR = BASE_LOG_DIR / "general"
GENERAL_LOG_DIR.mkdir(parents=True, exist_ok=True)
general_logger = logging.getLogger("general_logger")
general_logger.setLevel(logging.INFO)
general_handler = TimedRotatingFileHandler(
    filename=GENERAL_LOG_DIR / "general_request_response.log",
    when="midnight",
    interval=1,
    encoding="utf-8",
    backupCount=7,
)
general_formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
general_handler.setFormatter(general_formatter)
general_logger.addHandler(general_handler)
