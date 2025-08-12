#!/usr/bin/env bash
set -euo pipefail

cd /home/ing/overlord/wolfpack-lite/oanda_cba_unibot/OANDA_CBA_UNIBOT

echo "== repo =="
git remote -v | sed 's/^/  /'

# 1) make sure secret artifacts are ignored
if ! grep -qE '^\.(env|env\.live|env\.practice)$' .gitignore 2>/dev/null; then
  printf "%s\n" ".env" ".env.live" ".env.practice" >> .gitignore
fi
if ! grep -q '^secrets_' .gitignore 2>/dev/null; then
  printf "%s\n" "secrets_*" >> .gitignore
fi

# 2) show staged files
echo "== staged files (before) =="
git diff --cached --name-only | sed 's/^/  /' || true

# 3) unstage anything that looks secret-like to satisfy the pre-commit guard
SECRET_RE='(^|/)\.env($|\.|/)|^secrets_|(_|-)token|(_|-)secret|jwt|\.pem$|\.p12$|\.key$'
mapfile -t staged < <(git diff --cached --name-only || true)
for f in "${staged[@]}"; do
  if [[ "$f" =~ $SECRET_RE ]]; then
    echo ">> Unstaging secret-like file: $f"
    git restore --staged -- "$f" || true
  fi
done

echo "== staged files (after) =="
git diff --cached --name-only | sed 's/^/  /' || true

# 4) commit only if something remains staged
if [[ -n "$(git diff --cached)" ]]; then
  git commit -m "Safe commit: code updates (no secrets)"
else
  echo ">> Nothing staged to commit (or only secrets were staged)."
fi

# 5) sync with remote to fix 'fetch first'
echo "== fetch & rebase =="
git fetch origin
# Rebase on top of remote main to avoid merge commits
git rebase origin/main || { echo "!! Rebase conflict. Aborting."; git rebase --abort; exit 2; }

# 6) push
echo "== push =="
git push origin main && { echo '✔ Pushed cleanly.'; exit 0; }
