#!/usr/bin/env bash
set -euo pipefail

ISO_URL="https://github.com/ExploitEducation/Protostar/releases/download/v2.0.0/exploit-exercises-protostar-2.iso"
ISO_NAME="exploit-exercises-protostar-2.iso"

mkdir -p "$(dirname "$0")/iso"
cd "$(dirname "$0")/iso"

if [[ -f "$ISO_NAME" ]]; then
  echo "[+] ISO already exists: $PWD/$ISO_NAME"
  exit 0
fi

echo "[+] Downloading Protostar ISO..."
if command -v curl >/dev/null 2>&1; then
  curl -L --fail -o "$ISO_NAME" "$ISO_URL"
elif command -v wget >/dev/null 2>&1; then
  wget -O "$ISO_NAME" "$ISO_URL"
else
  echo "[-] Need curl or wget" >&2
  exit 2
fi

echo "[+] Downloaded: $PWD/$ISO_NAME"

