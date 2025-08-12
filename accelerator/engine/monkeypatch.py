import os, types, sys
def patch_if_needed():
    if os.getenv("BROKER_BACKEND","SIM").upper()!="SIM": return
    from accelerator.engine import broker_sim as sim
    m = types.ModuleType("unibot.adapters.oanda")
    m.Oanda = sim.Oanda
    sys.modules["unibot.adapters.oanda"] = m
