from __future__ import annotations

import random
import string
import sys
from io import StringIO
from pathlib import Path
from types import ModuleType
from typing import Any
from urllib.parse import urlparse
from urllib.request import urlopen


def loadmod(path: Path | str | StringIO, variables: dict[str, Any] | None = None, name: str = "") -> ModuleType:
    random_name = "".join(random.choices(string.ascii_lowercase, k=5))
    random_name = f"loadmod.{random_name}"

    txt = None
    if isinstance(path, Path):
        txt = path.read_text()
    elif isinstance(path, StringIO):
        txt = path.getvalue()
        path = "<string>"
    elif (parsed := urlparse(str(path))).scheme in {"http", "https"}:
        txt = str(urlopen(str(path)).read(), encoding="utf-8")
        path = f"<string {path}>"
    elif parsed.scheme in {"file"}:
        txt = Path(parsed.path).read_text()
        path = parsed.netloc
    else:
        raise ValueError(f"unsupported path type: {path}")

    mod = ModuleType(name)
    mod.__dict__.update(variables or {})
    mod.__dict__["__name__"] = name or random_name
    mod.__file__ = str(path)
    code_obj = compile(txt, filename=str(path), mode="exec")
    sys.modules[name] = mod
    exec(code_obj, mod.__dict__)  # noqa: S102
    return mod
