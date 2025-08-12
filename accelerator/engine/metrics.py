import json, pathlib, pandas as pd
REP=pathlib.Path(__file__).resolve().parents[1]/"reports"; REP.mkdir(parents=True, exist_ok=True)

def write_report(meta:dict, strat_summary:pd.DataFrame, sys_summary:pd.DataFrame, trade_rows:list, events:list):
    (REP/"strat_metrics.json").write_text(strat_summary.to_json(orient="records",indent=2))
    (REP/"sys_metrics.json").write_text(sys_summary.to_json(orient="records",indent=2))
    if trade_rows:
        pd.DataFrame(trade_rows).to_csv(REP/"all_trades.csv", index=False)
    (REP/"events.jsonl").write_text("\n".join([json.dumps(e) for e in events]))
    # Quick MD
    md=[]
    md.append(f"# Accelerated Replay — Summary\n")
    md.append(f"**Universe:** {meta['universe']} — Bars: ~{meta['bars']} — Years: {meta['years']}\n")
    md.append("## Strategy Metrics (per symbol)\n")
    md.append(pd.DataFrame(strat_summary).to_markdown(index=False))
    md.append("\n## System Workflow Metrics\n")
    md.append(sys_summary.to_markdown(index=False))
    md.append("\n**Notes:** OCO drop faults were injected to test self-healing; trailing was armed on trend per config.")
    (REP/"ACCELERATED_BRIEF.md").write_text("\n".join(md))
