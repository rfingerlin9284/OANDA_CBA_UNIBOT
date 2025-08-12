RESET="\x1b[0m"; BOLD="\x1b[1m"; ITALIC="\x1b[3m"
C={"red":"\x1b[31m","green":"\x1b[32m","yellow":"\x1b[33m","blue":"\x1b[34m","magenta":"\x1b[35m","cyan":"\x1b[36m","white":"\x1b[37m"}
def paint(t,color=None,bold=False,italic=False):
    s=[]
    if color in C: s.append(C[color])
    if bold: s.append(BOLD)
    if italic: s.append(ITALIC)
    s.append(str(t)); s.append(RESET); return "".join(s)
