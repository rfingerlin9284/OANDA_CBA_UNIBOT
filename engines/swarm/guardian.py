import os, time, math, threading
from dataclasses import dataclass

@dataclass
class TradeState:
    id: str
    side_sign: int
    entry: float
    tp: float
    sl: float

class Guardian:
    def __init__(self, broker, state: TradeState, pip: float):
        self.broker = broker
        self.s = state
        self.pip = pip
        self.cfg = {
            "trail_on": float(os.getenv("SWARM_TRAIL_ON_PROFIT_PIPS","10")),
            "trail_step": float(os.getenv("SWARM_TRAIL_STEP_PIPS","2")),
            "giveback": float(os.getenv("SWARM_MAX_GIVEBACK_PIPS","6")),
            "stale_min": int(os.getenv("SWARM_KILL_IF_STALE_MIN","45")),
            "escalate": str(os.getenv("SWARM_ESCALATE_ON_MOMENTUM","true")).lower() in {"1","true","yes"},
        }
        self._stop = threading.Event()

    def start(self): threading.Thread(target=self._run, daemon=True).start()
    def stop(self): self._stop.set()

    def _run(self):
        hb = max(1, int(os.getenv("SWARM_HEARTBEAT_SEC","1")))
        last_progress_ts = time.time()
        peak_unreal = 0.0

        while not self._stop.is_set():
            px = self.broker.get_last_price()
            pnl_pips = self.s.side_sign * (px - self.s.entry) / self.pip
            peak_unreal = max(peak_unreal, pnl_pips)

            # trailing activation
            if pnl_pips >= self.cfg["trail_on"]:
                trail_base = px - self.s.side_sign * self.cfg["giveback"]*self.pip
                new_sl = max(self.s.sl, trail_base) if self.s.side_sign>0 else min(self.s.sl, trail_base)
                if (self.s.side_sign>0 and new_sl>self.s.sl+self.cfg["trail_step"]*self.pip) or \
                   (self.s.side_sign<0 and new_sl<self.s.sl-self.cfg["trail_step"]*self.pip):
                    self.broker.modify_stop(self.s.id, new_sl)
                    self.s.sl = new_sl

            # stagnation check (and simple momentum flip via EMAs)
            if abs(pnl_pips) < 2:
                if time.time()-last_progress_ts > self.cfg["stale_min"]*60:
                    self.broker.close(self.s.id, reason="stale")
                    return
            else:
                last_progress_ts = time.time()

            # momentum escalation (pseudo):
            if self.cfg["escalate"] and self.broker.momentum_flip_detected():
                # tighten stop slightly
                bump = 1.0 * self.pip
                new_sl = self.s.sl + self.s.side_sign*bump
                self.broker.modify_stop(self.s.id, new_sl)
                self.s.sl = new_sl

            time.sleep(hb)
