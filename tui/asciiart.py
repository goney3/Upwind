"""tui/asciiart.py - Upwind roundel logo in ASCII/Unicode art."""

from tui.widgets import u, seg

LOGO = u(r"""
          .-~~~~~-.
       ,~    ▲    ~,
      /  ╲   █   ╱  \
     |    ╲  █  ╱    |
     |=====( █ )=====|
     |    ╱  █  ╲    |
      \  ╱   █   ╲  /
       '~    ▼    ~'
          '-.....-'
""").rstrip("\n").split("\n")

# Compact single-line mark for the header bar
MARK = u("▲(█)▲")


def logo_lines(theme):
    """Logo as styled lines (compass ring muted, prop/hub/arrow accented)."""
    out = []
    for i, ln in enumerate(LOGO):
        if i == 1:
            out.append(seg(ln.rstrip(), "muted") + [seg("▲", "amber") if u("▲") in ln else seg("", "muted")])
        elif i == 4:
            out.append(seg(ln, "accent"))
        else:
            out.append(seg(ln, "accent"))
    return out
