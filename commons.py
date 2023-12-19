import os

import psutil


def get_memory_usage() -> int:
    """in MiB"""
    return round(psutil.Process(os.getpid()).memory_info().rss / 1024**2)
