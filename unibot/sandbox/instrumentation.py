import json, os, time, threading, pathlib
_lock = threading.Lock()
def jlog(event, **ctx):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
           "event": event, "mode": os.getenv("MODE","SANDBOX"), **ctx}
    line = json.dumps(rec, separators=(",",":"))
    print(line, flush=True)
    log_file = os.getenv("LOG_FILE")
    if log_file:
        pathlib.Path(os.path.dirname(log_file)).mkdir(parents=True, exist_ok=True)
        with _lock, open(log_file, "a", encoding="utf-8") as f: f.write(line+"\n")
