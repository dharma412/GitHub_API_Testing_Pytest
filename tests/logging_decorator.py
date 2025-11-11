import logging
import os
import functools
import inspect
import json
from typing import Any

# Directory for logs
LOG_DIR = os.path.join(os.getcwd(), "logs")
LOG_FILE = os.path.join(LOG_DIR, "test_run.log")
SENSITIVE_KEYS = {"token", "authorization", "password", "access_token", "auth"}


def get_logger(name: str = "test_logger") -> logging.Logger:
    """Create or return a module-level logger writing to logs/test_run.log."""
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return logger


def _mask_value(k: str, v: Any) -> Any:
    if isinstance(v, dict):
        return mask_sensitive(v)
    if isinstance(v, (list, tuple)):
        return type(v)(_mask_value(k, x) for x in v)
    if k and k.lower() in SENSITIVE_KEYS:
        return "****REDACTED****"
    return v


def mask_sensitive(obj: Any) -> Any:
    """Recursively mask sensitive dict keys.

    Non-dict/list objects are returned as-is.
    """
    try:
        if isinstance(obj, dict):
            return {k: _mask_value(k, v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [mask_sensitive(x) for x in obj]
        return obj
    except Exception:
        return "<unserializable>"


def _safe_serialize_args(args, kwargs):
    try:
        masked_args = mask_sensitive(list(args))
        masked_kwargs = mask_sensitive(dict(kwargs))
        return json.dumps({"args": masked_args, "kwargs": masked_kwargs}, default=str)
    except Exception:
        return "unserializable-args"


def log_call(level: str = "info"):
    """A decorator factory that logs entry, exit, returns and exceptions.

    Supports generator functions (so it can be used on pytest fixtures that yield).
    """
    logger = get_logger()

    def decorator(func):
        if inspect.isgeneratorfunction(func):
            @functools.wraps(func)
            def gen_wrapper(*args, **kwargs):
                try:
                    logger.debug(f"ENTER generator {func.__name__}: {_safe_serialize_args(args, kwargs)}")
                except Exception:
                    logger.debug(f"ENTER generator {func.__name__}: <unserializable-args>")
                try:
                    for item in func(*args, **kwargs):
                        try:
                            snippet = repr(item)
                        except Exception:
                            snippet = "<unrepr>"
                        logger.debug(f"{func.__name__} yielded: {snippet[:1000]}")
                        yield item
                    logger.debug(f"EXIT generator {func.__name__}")
                except Exception as exc:
                    logger.exception(f"EXCEPTION in generator {func.__name__}: {exc}")
                    raise
            return gen_wrapper

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                entry = f"ENTER {func.__name__}: {_safe_serialize_args(args, kwargs)}"
                getattr(logger, level)(entry)
            except Exception:
                logger.log(logging.DEBUG, f"ENTER {func.__name__}: <unserializable-args>")
            try:
                result = func(*args, **kwargs)
                try:
                    summary = repr(result)
                except Exception:
                    summary = "<unrepr>"
                getattr(logger, level)(f"RETURN {func.__name__}: {summary[:2000]}")
                return result
            except Exception as exc:
                logger.exception(f"EXCEPTION in {func.__name__}: {exc}")
                raise
        return wrapper

    return decorator

