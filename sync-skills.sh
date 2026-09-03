#!/usr/bin/env bash
# Sync profile skills folders into the firm-skills hub and push to GitHub.
# Usage:
#   sync-skills.sh          -> Auto-discovers and syncs ALL profiles
#   sync-skills.sh all      -> Auto-discovers and syncs ALL profiles
#   sync-skills.sh <name>   -> Syncs a specific profile only
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HUB="$SCRIPT_DIR"

# Locate profiles directory (checks container $HOME/.hermes/profiles or workspace data/profiles)
PROFILES_DIR="${HOME}/.hermes/profiles"
if [ ! -d "$PROFILES_DIR" ]; then
  if [ -d "/workspace/data/profiles" ]; then
    PROFILES_DIR="/workspace/data/profiles"
  elif [ -d "${HUB}/../../data/profiles" ]; then
    PROFILES_DIR="$(cd "${HUB}/../../data/profiles" && pwd)"
  fi
fi

TARGET="${1:-all}"
SYNCED_PROFILES=()

sync_folder() {
  local src="$1"
  local dest="$2"
  mkdir -p "$dest"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete "$src/" "$dest/"
  else
    rm -rf "${dest:?}"/*
    if [ -d "$src" ] && [ "$(ls -A "$src" 2>/dev/null)" ]; then
      cp -a "$src"/. "$dest"/
    fi
  fi
}

if [ "$TARGET" = "all" ] || [ -z "$TARGET" ]; then
  echo "🔍 Auto-discovering all profile skill folders in: $PROFILES_DIR"
  if [ -d "$PROFILES_DIR" ]; then
    for p_dir in "$PROFILES_DIR"/*; do
      if [ -d "$p_dir" ]; then
        p_name="$(basename "$p_dir")"
        src_skills="$p_dir/skills"
        dest_skills="$HUB/firm/$p_name/skills"
        
        if [ -d "$src_skills" ]; then
          sync_folder "$src_skills" "$dest_skills"
          SYNCED_PROFILES+=("$p_name")
          echo "  ✓ Synced profile: $p_name"
        fi
      fi
    done
  fi
else
  # Single specified profile
  p_name="$TARGET"
  src_skills="$PROFILES_DIR/$p_name/skills"
  dest_skills="$HUB/firm/$p_name/skills"
  
  if [ ! -d "$src_skills" ]; then
    echo "⚠️ Warning: No skills directory found for profile '$p_name' at $src_skills"
  else
    sync_folder "$src_skills" "$dest_skills"
    SYNCED_PROFILES+=("$p_name")
    echo "  ✓ Synced single profile: $p_name"
  fi
fi

# Change to hub directory to check git status
cd "$HUB"

# Check if there are any git changes anywhere in the repo
if [ -n "$(git status --porcelain)" ]; then
  echo "📦 Changes detected. Preparing commit..."
  git add -A
  
  SUMMARY="${SYNCED_PROFILES[*]:-all}"
  COMMIT_MSG="skills(sync): auto-synced profiles [${SUMMARY}] $(date -u +%Y-%m-%dT%H:%MZ)"
  
  git -c user.name="Ehab" -c user.email="devalees@users.noreply.github.com" \
      commit -qm "$COMMIT_MSG"
  
  echo "✅ Committed: $COMMIT_MSG"
  
  # Auto-load GITHUB_TOKEN from .env if not already exported
  if [ -z "${GITHUB_TOKEN:-}" ]; then
    if [ -f "${HUB}/../../.env" ]; then
      export GITHUB_TOKEN="$(grep -E "^GITHUB_TOKEN=" "${HUB}/../../.env" | cut -d"=" -f2- | tr -d "\"" | tr -d "\047")"
    fi
  fi

  # Push if GITHUB_TOKEN is available
  if [ -n "${GITHUB_TOKEN:-}" ]; then
    echo "🚀 Pushing changes to remote GitHub repository..."
    git remote set-url origin "https://${GITHUB_TOKEN}@github.com/devalees/skills.git"
    git pull --rebase origin main || true
    git push origin main
    git remote set-url origin "https://github.com/devalees/skills.git"
    echo "🎉 Successfully pushed all profile skills to GitHub!"
  else
    echo "ℹ️ Committed locally. To push, ensure GITHUB_TOKEN is exported or present in .env"
  fi
else
  echo "✨ All profile skills are already up to date. No changes to push."
fi
