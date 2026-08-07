#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""flow-walkthrough 自检脚本：环境检查 + golden 走查构建断言。

用法： python3 scripts/selftest.py
退出码： 0 = 全部通过；1 = 存在失败项。
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(HERE, "build.py")
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, ("  [%s]" % detail) if detail and not ok else ""))


def run(args):
    return subprocess.run([sys.executable, BUILD] + args, capture_output=True, text=True, encoding="utf-8")


def main():
    check("python 版本 >= 3.8", sys.version_info >= (3, 8), sys.version.split()[0])
    tmp = tempfile.mkdtemp(prefix="flowwalk-selftest-")
    out = os.path.join(tmp, "walkthrough.html")

    p = run([os.path.join(ROOT, "examples", "walkmap.json"), "-o", out])
    check("golden 走查构建成功", p.returncode == 0, (p.stderr or p.stdout).strip()[:120])
    if p.returncode == 0:
        rep = json.loads(p.stdout.splitlines()[0])
        check("页面数 = 8", rep["pages"] == 8, str(rep["pages"]))
        check("映射节点数 = 15", rep["nodes"] == 15, str(rep["nodes"]))
        check("SVG 节点与映射一致（无警告）", not rep["warnings"], "; ".join(rep["warnings"])[:100])
        html = open(out, encoding="utf-8").read()
        check("单文件产物含嵌入 SVG", 'data-flowspec="1"' in html)
        check("联动脚本存在", "setViewByNode" in html and "goNode" in html)
        check("画布拖拽/缩放存在", "pointerdown" in html and "setZoom" in html)
        check("选中框定位逻辑存在", "sel-ring" in html and "getBBox" in html)
        check("全部页面均已内联", all(('id="p-%s"' % x) in html for x in
                                    ["login", "home", "external", "form", "review", "rejected", "active", "admin"]))
        emoji = [ch for ch in html if 0x1F000 <= ord(ch) <= 0x1FAFF or 0x2600 <= ord(ch) <= 0x27BF]
        check("产物无 emoji", not emoji, "".join(emoji[:5]))

    # 错误场景：引用不存在页面必须明确报错
    badmap = os.path.join(tmp, "bad.json")
    with open(badmap, "w", encoding="utf-8") as f:
        json.dump({"spec": "walkmap/1", "svg": "../examples/member-onboarding.svg",
                   "pages": [], "nodes": {"A": {"page": "p-nope"}}}, f)
    p = run([badmap, "--check"])
    ok = p.returncode != 0 and "未定义页面" in (p.stdout + p.stderr)
    check("坏映射明确报错", ok, (p.stdout + p.stderr).strip()[:100])

    fails = [r for r in results if not r[1]]
    print("\n%d/%d 通过" % (len(results) - len(fails), len(results)))
    if fails:
        print("失败项：" + "; ".join(r[0] for r in fails))
        sys.exit(1)
    print("flow-walkthrough 自检全部通过")


if __name__ == "__main__":
    main()
