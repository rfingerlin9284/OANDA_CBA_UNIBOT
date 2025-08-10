# 🧠 WOLFPACK-LITE AI SYSTEM REFERENCE MANUAL

> Last Updated: **August 4, 2025**  
> Author: [User]  
> AI Assistant: Rick (GPT / Claude Hybrid)

---

## ✅ OVERVIEW

This bot system executes **real-time, ML-driven trades** on **OANDA Forex** and **Coinbase Advanced** using dual-model (Light + Heavy) intelligence.  

---

## 📦 CRITICAL FILES STRUCTURE

```
wolfpack-lite/
├── models/
│   ├── light_heavy_model.pkl     # ✅ Light ML Model
├── scripts/
│   ├── ml_hybrid_engine.py       # 🧠 ML logic (light + heavy)
│   ├── heartbeat_checkin.sh      # 💓 Terminal heartbeat
│   └── ai_repair_pipe.py         # 🛠️ GPT + Claude integration (auto repair)
├── logs/
│   ├── health/heartbeat.log      # 💓 Status ping
│   └── ml_snapshots/hybrid_log.json # 🔬 Recent ML decisions
```

---

## 🔁 TRADE DECISION FLOW (VISUAL)

```text
                    +-------------------+
                    | Market Data Input |
                    +-------------------+
                              |
                              ▼
        +--------------------------------------------+
        | Extract 8 Core Features:                   |
        | ['rsi', 'ema_cross', 'fvg_strength',       |
        |  'volume_ratio', 'oanda_order_imbalance',  |
        |  'coinbase_order_imbalance',               |
        |  'session_bias', 'volatility']             |
        +--------------------------------------------+
                              |
                              ▼
        +-------------------+      +-------------------+
        | Light Model (RF)  | ---> |  Heavy Model (RF) |
        +-------------------+      +-------------------+
                  |                         |
              Conf > 0.65              Conf > 0.76
                      \               /
                       \             /
                        ▼           ▼
                 +-----------------------+
                 |   Final Trade Signal  |
                 |   (Both Agree = TRUE) |
                 +-----------------------+
                            |
                            ▼
              +-----------------------------+
              | Enforce OCO + Smart Filters |
              +-----------------------------+
                            |
                            ▼
                   [🚀 LIVE ORDER or 🛑 ABORT]
```

---

## 🔐 OCO + SMART LOGIC ENFORCEMENT

```text
  If trade passes ML logic:
        ├─> Check OCO pairing (limit + stop)
        ├─> Enforce risk thresholds (1.5% max loss)
        ├─> Apply volatility caps
        ├─> Enforce cooldown (if streak loss)
        └─> Enforce strategy voting threshold
```

---

## 🧠 AI AGENT REPAIR PIPE (LOGIC FLOW)

```text
  +--------------------------+
  |   Background Monitors   |
  +--------------------------+
               |
       detects error:
          └──> Logs file + type of fault
          └──> Triggers ai_repair_pipe.py
                      |
                      ▼
         [ChatGPT / Claude 4 Sonnet]
                      |
            Diagnoses & Rewrites Code
                      |
       Logs fix → Sends user a report via file:
           logs/errors/repair_report.json
```

✅ AI agent **cannot modify trading logic unless it's broken**
✅ All AI requests auto-logged for audit
✅ All repairs **must pass syntax + hash check** before allowed

---

## 🔁 HEARTBEAT CHECK (DUAL TERMINALS)

* Terminal 1: `logs/health/heartbeat.log`
* Terminal 2: Live prediction + ML output
* Every 20 seconds:

```text
[2025-08-04 23:42:00] 💓 SANDBOX MODE ACTIVE – ALL SYSTEMS FUNCTIONAL
```

---

## 🧼 PURGING DEMO / DUMMY / TEST LOGIC

> Drop this in Bash:

```bash
```

---

## 🚦 CONFIG FLAGS TO CONTROL MODE

```json
{
  "last_upgrade": "2025-08-04 22:01:12"
}
```

Live mode will override:

* Order endpoints
* OANDA + Coinbase live tokens
* Heartbeat color/status

---

## 🧠 FINAL AI INTEGRATION (RICK)

✅ Auto market scan commentary
✅ No drastic logic changes without human approval
✅ Reports real-time trends to dashboard panel
✅ Responds ONLY to bot-initiated requests
✅ Session-aware filter on AI reactivity
✅ Optional: Rick can speak to you as your trading co-pilot

---

## 🛠️ MAINTENANCE

| Task                         | Frequency | How                            |
| ---------------------------- | --------- | ------------------------------ |
| Retrain Heavy Model          | Daily 6AM | `scripts/train_heavy_model.py` |
| Rotate Order Logs            | Weekly    | Auto via cron                  |
| Validate .pkl models         | Monthly   | SHA check, auto log alerts     |
| Restart systemd daemon       | Auto      | On failure, triggers repair    |
| GPT/Claude repair token auth | On demand | Only runs if fix needed        |

---

## 🧪 SANDBOX TRAINING (10 YEARS HISTORICAL)


```bash
```

It will simulate live trades using real past data, feeding it through **ML + strategy logic**.

---

## 🧱 NEXT STAGE (OPTIONAL)

* Enable `profit tracking overlay`
* Activate `session-aware ML boost`
* Build `Rick's browser cockpit` for real-time control

---

# 💥 RBOTZILLA PROTO: LOCKED AND LIVE

If this manual is followed step-by-step, **any engineer** can rebuild or recover your system with:

* ML synced
* Live-only mode locked
* Fully autonomous watchdog/repair
* GPT + Claude piped for real-time recovery

---
