#!/usr/bin/env python3
"""
Build the browser version of CHROME DOGS.

Inlines web_curses.py (the in-browser curses shim), solvent.py's logic
slice (terminal.py only needs its CHASSIS/OUTFITS data tables, not its
own curses UI), and terminal.py itself (untouched) into template.html,
plus web_bridge.py to wire them together. Re-run after changing any of
those files:

    python3 -m py_compile terminal.py solvent.py web_curses.py web_bridge.py
    python3 build_web.py
"""

UI_MARKER = ("# ----------------------------------------------------------------------------\n"
             "# CURSES UI")


def main():
    solvent = open("solvent.py").read()
    logic = solvent.split(UI_MARKER)[0]
    curses_shim = open("web_curses.py").read()
    game = open("terminal.py").read()
    bridge = open("web_bridge.py").read()

    blobs = (
        (curses_shim, "web_curses.py"),
        (logic, "solvent.py"),
        (game, "terminal.py"),
        (bridge, "web_bridge.py"),
    )
    for blob, name in blobs:
        if "</script" in blob:
            raise SystemExit(f"{name} contains '</script', which would break inlining")

    html = open("template.html").read()
    html = (html
            .replace("__PY_CURSES__", curses_shim)
            .replace("__PY_SOLVENT__", logic)
            .replace("__PY_TERMINAL__", game)
            .replace("__PY_BRIDGE__", bridge))
    with open("index.html", "w") as f:
        f.write(html)
    sizes = ", ".join(f"{name} {len(blob):,}" for blob, name in blobs)
    print(f"index.html written ({len(html):,} bytes; {sizes})")


if __name__ == "__main__":
    main()
