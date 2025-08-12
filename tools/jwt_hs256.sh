#!/usr/bin/env bash
set -euo pipefail
# usage: ./tools/jwt_hs256.sh <secret> <claims-json>
b64url(){ openssl base64 -A | tr '+/' '-_' | tr -d '='; }
s="$1"; claims="$2"
hdr='{"alg":"HS256","typ":"JWT"}'
h="$(printf '%s' "$hdr"   | b64url)"
p="$(printf '%s' "$claims"| b64url)"
sig="$(printf '%s' "$h.$p" | openssl dgst -sha256 -hmac "$s" -binary | b64url)"
printf '%s.%s.%s\n' "$h" "$p" "$sig"
