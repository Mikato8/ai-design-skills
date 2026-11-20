#!/usr/bin/env bash
# Install these skills into DeepSeek Harness (~/.agents/skills).
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dest="${DSH_SKILLS_DIR:-$HOME/.agents/skills}"

mkdir -p "$dest"
for skill in "$root"/skills/*/; do
    name="$(basename "$skill")"
    mkdir -p "$dest/$name"
    cp "$skill/SKILL.md" "$dest/$name/SKILL.md"
    echo "installed $name -> $dest/$name"
done
