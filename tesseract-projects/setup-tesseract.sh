#!/bin/bash
# Reinstall the pinned Tesseract CLI (plus Linux render deps) in a fresh cloud container.
# Follows .claude/skills/tesseract-video/references/installation.md.
set -euo pipefail
repo="$(cd -- "$(dirname -- "$0")/.." && pwd)"
version="$(cat "$repo/.claude/skills/tesseract-video/references/cli-version.txt")"
tsrct="${XDG_DATA_HOME:-$HOME/.local/share}/Tesseract/bin/tsrct"
if [ -x "$tsrct" ] && "$tsrct" --version | grep -q "tsrct $version "; then
  echo "tsrct $version already installed: $tsrct"
else
  asset="tesseract-$version-linux-x86_64.zip"
  dl="$(mktemp -d)"
  base="https://github.com/mirage-hq/tesseract/releases/download/v$version"
  curl -fsSL -o "$dl/$asset" "$base/$asset"
  curl -fsSL -o "$dl/$asset.sha256" "$base/$asset.sha256"
  (cd "$dl" && sha256sum -c "$asset.sha256")
  unzip -q "$dl/$asset" -d "$dl/x"
  bash "$dl/x/tesseract-$version-linux-x86_64/install.sh"
fi
# Headless rendering needs a Vulkan driver (Mesa lavapipe); H.264 export needs FFmpeg with libx264.
if ! ls /usr/share/vulkan/icd.d/lvp_icd*.json >/dev/null 2>&1 || ! command -v ffmpeg >/dev/null; then
  apt-get update -qq || true
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq mesa-vulkan-drivers ffmpeg
fi
"$tsrct" --version
