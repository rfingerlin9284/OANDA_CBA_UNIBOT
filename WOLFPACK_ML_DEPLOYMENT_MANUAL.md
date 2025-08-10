# 🧠 WOLFPACK-LITE: Full ML Hybrid Deployment Manual (OANDA + Coinbase)

This markdown document serves as a complete rebuild and troubleshooting reference for engineers and AI agents managing the **WOLFPACK-LITE** hybrid trading bot system. It outlines exactly how the system is wired, which models are used, what features are active, and how to verify, retrain, or repair any part of the stack.

---

## ✅ ACTIVE COMPONENTS

| Module                | Description                                                             | Location                    |
|-----------------------|-------------------------------------------------------------------------|-----------------------------|
| light_heavy_model.pkl | Lightweight ML model (quick patterns, fast entries)                     | `models/`                   |
| ml_hybrid_engine.py   | Executes dual-model prediction logic                                    | `scripts/ml_hybrid_engine.py` |
| train_light_model.py  | Retrains lightweight model using cleaned + historical data              | `scripts/`                  |
| train_heavy_model.py  | Retrains heavyweight model                                              | `scripts/`                  |
| hybrid_log.json       | Log of the last 20 decisions with timestamp + confidence                | `logs/ml_snapshots/`        |

---

## 🔗 HOW EVERYTHING CONNECTS

1. `main.py` or your trading router calls:
   ```python
   from scripts.ml_hybrid_engine import HybridMLDecisionEngine
   engine = HybridMLDecisionEngine()
   decision = engine.predict(features)
   if decision:
       execute_trade()
   ```

2. `features` is a dictionary with **live pre-processed indicators** like:
   - `fvg_signal`
   - `ema_distance`
   - `orderbook_depth_ratio`
   - `volume_spike`
   - `rsi_shift`
   - `previous_confluence_score`

3. Both models must give minimum confidence:
   - `light_conf` ≥ 0.65
   - `heavy_conf` ≥ 0.76
   - Decision = True ONLY if both are satisfied

4. All trades are automatically:
   - Evaluated with ML overlay
   - Enforced with **OCO order logic**
   - Protected with **Cobra Strike filter** (tight SL on reversal)

---

## 🧪 DAILY RETRAINING PIPELINE (CRON SCHEDULED)

At **7:50 AM daily**, two things happen:

   ```bash
   find data/ -type f -name "*.csv" | while read file; do
   done
   ```

2. Then ML retraining script is triggered:
   ```bash
   python3 scripts/train_light_model.py
   python3 scripts/train_heavy_model.py
   ```

Cron entry (verify with `crontab -l`):
```bash
45 7 * * * bash /home/ing/FOUR_horsemen/ALPHA_FOUR/proto_oanda/wolfpack-lite/scripts/purge_fake_data.sh
50 7 * * * bash /home/ing/FOUR_horsemen/ALPHA_FOUR/proto_oanda/wolfpack-lite/setup_daily_retrainer.sh
```

---

## 🔍 TROUBLESHOOTING CHECKLIST

| Task                                | Command or Check                                             |
|-------------------------------------|--------------------------------------------------------------|
| Confirm models exist                | `ls models/`                                                 |
| Confirm hybrid engine works         | `python3 scripts/ml_hybrid_engine.py`                        |
| Manually trigger retrain            | `bash setup_daily_retrainer.sh`                             |
| Confirm cron jobs installed         | `crontab -l`                                                 |
| Inspect purge operation             | `bash scripts/purge_fake_data.sh && git diff` (optional)    |

---

## 🧠 STRATEGY NOTES FOR ML ENGINE

The ML system is trained on:
- Real-time and historical **price action**
- FVG zone success probability
- Live orderbook metrics from both OANDA and Coinbase
- Session-aware behavior (NY open, London close, etc)
- Prior trade outcomes (via `logs/`)

The system **auto-relearns daily**, adapts to volatility, and avoids stale strategies.

---

## 🔒 SECURITY & INTEGRITY

- `.pkl` models are locked to live-only signals
- All `.env` API values are hardcoded for deployment
- OCO and SL/TP logic enforced in trade layer

---

## 👨‍🔧 MAINTENANCE FOR HUMAN ENGINEER OR AI AGENT

| Task                      | Frequency       | Action                                                           |
|---------------------------|------------------|------------------------------------------------------------------|
| Check retrain logs        | Daily            | Open `logs/ml_snapshots/hybrid_log.json`                         |
| Validate strategy results | Weekly           | Sample from last 20 decisions + match with P/L logs              |
| Backup models             | Monthly          | Copy `.pkl` files to archive directory                           |
| Refresh training data     | Quarterly        | Pull updated CSVs into `data/` folder                            |

---

## 🚀 QUICK DEPLOYMENT VERIFICATION

Run this sequence to verify the entire ML hybrid stack is operational:

```bash
# 1. Check all components exist
ls models/ scripts/ logs/ml_snapshots/

# 2. Test hybrid engine standalone
python3 -c "from scripts.ml_hybrid_engine import HybridMLDecisionEngine; print('✅ ML Engine loaded successfully')"

# 3. Verify cron jobs
crontab -l | grep wolfpack

# 4. Check recent ML decisions
cat logs/ml_snapshots/hybrid_log.json | tail -5

# 5. Test full integration
```

---

## 🔧 AI AGENT COMMAND PROMPTS

### For rebuilding the entire ML stack:
```
"Run the inject_ml_hybrid_stack.sh script to install models, create training scripts, and set up daily retraining cron jobs for the WOLFPACK-LITE system."
```

### For manual retraining:
```
```

### For troubleshooting ML decisions:
```
"Check logs/ml_snapshots/hybrid_log.json for the last 20 ML decisions and their confidence scores. Verify both light_conf and heavy_conf meet minimum thresholds."
```

---

This file is your final **AI Agent Instruction + Developer Reference** for maintaining, repairing, and validating the WOLFPACK-LITE ML Trading Engine.
