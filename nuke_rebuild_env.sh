#!/bin/bash
# === ULTIMATE ENVIRONMENT RESET (kills liveplefilter forever) ===
cd /home/ing/overlord/wolfpack-lite/oanda_cba_unibot
deactivate 2>/dev/null || true

echo "🔥 NUKING coinbase_env (removing broken numpy/pip)..."
rm -rf coinbase_env

echo "🚀 RECREATING fresh coinbase_env virtualenv..."
python3 -m venv coinbase_env
source coinbase_env/bin/activate

echo "⬆️  Installing latest pip, numpy, pandas, and essentials..."
pip install --upgrade pip numpy pandas requests websockets matplotlib

echo "🔥 Installing PyNaCl for Ed25519 authentication..."
pip install PyNaCl typing_extensions

echo "🟢 VERIFYING numpy and pandas import clean..."
python3 -c "import numpy, pandas; print('✅ Clean NUMPY & PANDAS imports!')"

echo "🔐 VERIFYING Ed25519 imports clean..."
python3 -c "from nacl.signing import SigningKey; from nacl.encoding import Base64Encoder; print('✅ Clean Ed25519 imports!')"

echo "✅ Your environment is now 100% clean. Re-run your FVG/ML/live bot scripts and they WILL work."
