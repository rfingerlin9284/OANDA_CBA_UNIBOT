#!/usr/bin/env bash
set -euo pipefail
set -o errtrace
trap 'ret=$?; echo "❌ Error $ret on line $LINENO: $BASH_COMMAND" >&2' ERR

# ---- CONFIG ----
ACTIVE_ROOT="$(pwd)"
LEGACY_DIR="$ACTIVE_ROOT/legacy_bloat"
KEEP_DIRS=("config" "engines" "scripts" "tools" ".githooks" ".git")
KEEP_FILES=("LICENSE" ".gitignore" ".gitattributes" "make_swapper.sh" "secrets_replace.json" \
            "secrets_swap_manifest.json" "secrets_swap_report.txt" "WOLFPACK_PROTO_GUIDE.md")

# extra junk patterns
NUKE_PATTERNS=("nohup.out" "*.log" "*.tmp" "*.bak" "*.old" "*.swp" "*.swo" "*.zip" "*.tar" "*.tar.gz" "*.7z")
NUKE_DIRS=("legacy_logs" "__pycache__" ".pytest_cache" ".mypy_cache" ".venv" "venv" "node_modules" "logs")

say(){ printf "\n\033[1;36m%s\033[0m\n" "$*"; }
ok(){  printf "\033[1;32m%s\033[0m\n" "$*"; }
warn(){printf "\033[1;33m%s\033[0m\n" "$*"; }

say "1) Preparing legacy area: $LEGACY_DIR"
mkdir -p "$LEGACY_DIR"

say "2) Remove heavy/temporary dirs"
for d in "${NUKE_DIRS[@]}"; do
  if [ -d "$d" ]; then
    rm -rf -- "$d"
    ok "deleted dir: $d"
  fi
done

say "3) Remove runtime noise files"
for pat in "${NUKE_PATTERNS[@]}"; do
  find "$ACTIVE_ROOT" -maxdepth 1 -type f -name "$pat" -print0 | xargs -0 -r rm -f --
done
ok "surface runtime noise cleared"

say "4) Move stray top-level items to legacy_bloat (keeps the live core tidy)"
shopt -s dotglob nullglob
for item in *; do
  # skip kept dirs/files
  skip=false
  for k in "${KEEP_DIRS[@]}"; do [[ "$item" == "$k" ]] && { skip=true; break; }; done
  for kf in "${KEEP_FILES[@]}"; do [[ "$item" == "$kf" ]] && { skip=true; break; }; done
  [[ "$item" == "." || "$item" == ".." || "$item" == ".git" ]] && skip=true
  $skip && continue
  mv -f -- "$item" "$LEGACY_DIR"/
  ok "moved -> legacy_bloat: $item"
done
shopt -u dotglob nullglob

say "5) Normalize line endings + exec bits"
# fix CRLF in our shell/python files
find config engines scripts tools -type f \( -name "*.sh" -o -name "*.py" \) -print0 \
  | xargs -0 -r sed -i 's/\r$//'
# ensure our runners are executable
find scripts tools -type f -name "*.sh" -print0 | xargs -0 -r chmod +x

say "6) Harden .gitignore for live-only repo"
cat > .gitignore <<'IG'
# private artifacts (do NOT commit)
secrets_swap_manifest.json
secrets_replace.json
secrets_replace.json.current
secrets_swap_report.txt

# envs & venvs
.env*
.venv/
venv/

# caches
__pycache__/
.pytest_cache/
.mypy_cache/

# logs & dumps
logs/
*.log
nohup.out
*.tmp
*.bak
*.old
*.swp
*.swo
IG
ok "updated .gitignore"

say "7) Pre-commit hook to block secrets/JWTs"
mkdir -p .githooks
cat > .githooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail
# do not allow secrets bundles
if git diff --cached --name-only | grep -E 'secrets_(swap_manifest|replace|replace\.current|swap_report)\.json$' >/dev/null; then
  echo "Abort: secrets files are private; do not commit them."
  exit 1
fi
# block PEM or JWT-ish strings
if git diff --cached -U0 | grep -E 'BEGIN [^-]*PRIVATE KEY|[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+' >/dev/null; then
  echo "Abort: potential key/token in commit."
  exit 1
fi
HOOK
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks

say "8) Final tree"
find . -maxdepth 2 -mindepth 1 -printf "%y %p\n" | sort
ok "✅ Clean, live-only tree is ready."
