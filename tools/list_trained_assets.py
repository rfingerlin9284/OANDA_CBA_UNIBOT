import os, re, json, ast, sys, argparse, pathlib

KEY_HINTS = [
    "assets","coins","symbols","pairs","tickers","universe",
    "train_assets","train_pairs","train_symbols","instruments"
]
STR_RE = re.compile(r"[A-Z0-9]{2,}([-_/][A-Z0-9]{2,}){0,3}")  # BTC-USD, ETH_USD, BTC, SOL-PERP, etc.

def classify(sym:str):
    s = sym.strip()
    U = s.upper()
    # forex
    if re.fullmatch(r"[A-Z]{3}[_/][A-Z]{3}", U):
        return "forex_pairs"
    # futures / perps
    if any(x in U for x in ["-PERP","/PERP","_PERP","-F0","-USD-PERP","-USDT-PERP","-PERPETUAL","-FUT","/FUT"]):
        return "futures"
    # dated futures like BTC-USD-240927
    if re.fullmatch(r"[A-Z0-9]+[-_/][A-Z0-9]+[-_/]\d{6}", U):
        return "futures"
    # spot pairs (crypto)
    if re.fullmatch(r"[A-Z0-9]+[-_/][A-Z0-9]+", U):
        return "pairs_spot"
    # single-asset symbols -> spot coin tickers
    if re.fullmatch(r"[A-Z0-9]{2,10}", U):
        return "coins_spot"
    return "unknown"

def add_hit(store, kind, sym, file):
    sym = sym.upper()
    if sym not in store[kind]["values"]:
        store[kind]["values"].append(sym)
    store[kind]["files"].setdefault(sym, set()).add(file)

def scan_json(path, store):
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return
    stack = [data]
    while stack:
        v = stack.pop()
        if isinstance(v, dict):
            for k, val in v.items():
                if any(h in str(k).lower() for h in KEY_HINTS):
                    # prefer arrays of strings
                    if isinstance(val, (list,tuple)):
                        for item in val:
                            if isinstance(item, str):
                                knd = classify(item)
                                if knd != "unknown":
                                    add_hit(store, knd, item, str(path))
                    elif isinstance(val,str):
                        # split on commas / whitespace if someone stuffed a CSV string
                        for token in re.split(r"[,\s]+", val):
                            if STR_RE.fullmatch(token):
                                knd = classify(token)
                                if knd!="unknown":
                                    add_hit(store,knd,token,str(path))
                if isinstance(val,(dict,list,tuple)):
                    stack.append(val)
        elif isinstance(v, (list,tuple)):
            for x in v:
                if isinstance(x,(dict,list,tuple)): stack.append(x)

def scan_yaml_toml_text(text, path, store):
    # cheap parse via regex fallback: grab quoted or bare tokens after keys we care about
    lines = text.splitlines()
    for ln in lines:
        low = ln.lower()
        if any(h in low for h in KEY_HINTS):
            for token in re.findall(r"[A-Za-z0-9\-_/.]+", ln):
                if STR_RE.fullmatch(token):
                    knd = classify(token)
                    if knd!="unknown":
                        add_hit(store,knd,token,str(path))

def scan_py_ast(path, store):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                name = getattr(t, "id", "") or ""
                if any(h in name.lower() for h in KEY_HINTS):
                    # list/tuple of strings
                    if isinstance(node.value, (ast.List, ast.Tuple, ast.Set)):
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Str):
                                knd = classify(elt.s)
                                if knd!="unknown":
                                    add_hit(store,knd,elt.s,str(path))
                    # dict with arrays
                    if isinstance(node.value, ast.Dict):
                        for val in node.value.values:
                            if isinstance(val, (ast.List, ast.Tuple, ast.Set)):
                                for elt in val.elts:
                                    if isinstance(elt, ast.Str):
                                        knd = classify(elt.s)
                                        if knd!="unknown":
                                            add_hit(store,knd,elt.s,str(path))

def build_store():
    kinds = ["coins_spot","pairs_spot","futures","forex_pairs"]
    return {k: {"values": [], "files": {}} for k in kinds}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="repo root to scan")
    ap.add_argument("--save", default="envs/asset_manifest.json", help="where to write the summary JSON")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    store = build_store()

    for p in root.rglob("*"):
        if not p.is_file(): continue
        low = p.name.lower()
        try:
            if low.endswith(".json"):
                scan_json(p, store)
            elif low.endswith((".yml",".yaml",".toml",".ini",".conf",".cfg",".md",".txt")):
                scan_yaml_toml_text(p.read_text(encoding="utf-8", errors="ignore"), p, store)
            elif low.endswith(".py"):
                scan_py_ast(p, store)
            else:
                # last resort: skim for obvious tickers in data files
                if low.endswith((".csv",".parquet",".pkl",".pt",".bin",".npz",".npy")):
                    # infer from filename
                    for token in STR_RE.findall(p.name.upper()):
                        knd = classify(token)
                        if knd!="unknown":
                            add_hit(store,knd,token,str(p))
        except Exception:
            pass

    # dedupe + sort
    for k in store:
        store[k]["values"] = sorted(set(store[k]["values"]))
        store[k]["files"] = {sym: sorted(list(paths)) for sym,paths in store[k]["files"].items()}

    out = {
        "root": str(root.resolve()),
        "summary": {k: store[k]["values"] for k in store},
        "where_defined": store[k]["files"]  # last k from loop scope? fix:
    }
    # fix where_defined properly:
    out["where_defined"] = {k: store[k]["files"] for k in store}

    pathlib.Path(args.save).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.save).write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out["summary"], indent=2))
    print(f"\nWrote full manifest -> {args.save}")
