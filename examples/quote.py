"""Run the Tencent quote implementation from SKILL.md without its tutorial calls."""

import argparse
import ast
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError


SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"


def load_quote_helpers():
    """Load only the three prerequisite blocks from the local, trusted Skill."""
    blocks = re.findall(r"```python\n(.*?)```", SKILL_PATH.read_text(encoding="utf-8"), re.S)
    namespace = {}
    for name in ("get_prefix", "norm_ticker", "tencent_quote"):
        matches = [block for block in blocks if re.search(rf"^def {name}\(", block, re.M)]
        if len(matches) != 1:
            raise RuntimeError(f"SKILL.md 中 {name} 的定义应恰好出现一次。")
        tree = ast.parse(matches[0])
        defined = {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
        kept = []
        for node in tree.body:
            if not isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef,
                                     ast.Assign, ast.AnnAssign)):
                continue
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                called = {call.func.id for call in ast.walk(node)
                          if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)}
                if called & defined:
                    continue
            kept.append(node)
        tree.body = kept
        exec(compile(tree, f"{SKILL_PATH}:{name}", "exec"), namespace)
    return namespace


def main():
    parser = argparse.ArgumentParser(description="调用 SKILL.md 的腾讯行情代码，输出 JSON。")
    parser.add_argument("codes", nargs="+", help="如 600519、sz000001、000001.SH、510300")
    args = parser.parse_args()
    try:
        helpers = load_quote_helpers()
        codes = list(dict.fromkeys(helpers["get_prefix"](code) + helpers["norm_ticker"](code)
                                   for code in args.codes))
        quotes = helpers["tencent_quote"](codes)
        missing = [code for code in codes if code not in quotes]
        if missing:
            raise RuntimeError("腾讯未返回这些代码的行情：" + ", ".join(missing))
    except (ValueError, RuntimeError, URLError, OSError) as error:
        print(f"行情读取失败：{error}", file=sys.stderr)
        return 1
    print(json.dumps({
        "source": "tencent",
        "source_url": "https://qt.gtimg.cn/q=" + ",".join(codes),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "quotes": quotes,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
