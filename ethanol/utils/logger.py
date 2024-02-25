__all__ = ["debug", "info", "warn", "error"]


def debug(*args, **kwargs):
    print("[DEBUG]:", *args, **kwargs)


def info(*args, **kwargs):
    print("[INFO]:", *args, **kwargs)


def warn(*args, **kwargs):
    print("[WARNING]:", *args, **kwargs)


def error(*args, **kwargs):
    print("[ERROR]:", *args, **kwargs)
