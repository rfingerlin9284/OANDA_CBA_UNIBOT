from .termsty import paint

def _u(u):
    u=int(u); 
    return f"{u//1000}k" if abs(u)>=1000 and u%1000==0 else (f"{u/1000:.1f}k" if abs(u)>=1000 else str(u))

def render_trade_line(tr):
    st=(tr.get("status","") or "").lower()
    side=(tr.get("side","") or "").upper()
    sym=tr.get("symbol","?"); u=_u(tr.get("units",0)); avg=tr.get("avg",0.0); cur=tr.get("current",0.0)
    pips=tr.get("pl_pips",0.0); ticket=tr.get("ticket","—")
    base=f"{ticket} {sym} {side:<5} x{u} @ {avg:.5f} | P/L {pips:+.1f}p | Px {cur:.5f}"

    if st in ("failed","rejected","potential","blocked"):
        line=paint(f"{st.upper():<9} {base}", color="red")
        if tr.get("commentary"): line+=" "+paint(f"— {tr['commentary']}", color="red", italic=True)
        return line

    if st in ("open","active"):
        line=paint(f"OPEN       {base}", color="green", bold=True)
        o=tr.get("oco") or {}
        if o:
            tp=o.get("tp"); sl=o.get("sl"); trailing=o.get("trailing"); tp_removed=o.get("tp_removed")
            if tp_removed: oco=f"OCO: TP removed; SL {sl:.5f}"
            else:          oco=f"OCO: TP {tp:.5f} SL {sl:.5f}"
            if trailing:   oco+=" | trailing SL active"
            line+="  "+paint(oco, color="magenta", italic=True)
        return line

    if st=="closed": return paint(f"CLOSED     {base}", color="yellow", bold=True)
    return f"{st.upper():<9} {base}"
