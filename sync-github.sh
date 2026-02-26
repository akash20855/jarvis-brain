#!/bin/bash
cd /Volumes/Akash\ SSD/repos/jarvis-brain

# Set git to not use an editor
export GIT_EDITOR=true
export GIT_MERGE_VERBOSITY=1

# Try to reset and clean
echo "🔄 Resetting local changes..."
git reset --hard HEAD 2>/dev/null || true
git clean -fd 2>/dev/null || true

# Try simple merge instead of rebase
echo "📥 Pulling from remote (using merge strategy)..."
git config pull.rebase false
git pull origin main --no-edit 2>&1

# If pull succeeded, push
if [ $? -eq 0 ]; then
    echo "🚀 Pushing to GitHub..."
    git push -u origin main
    echo "✅ Done!"
else
    echo "❌ Pull failed. Trying alternative approach..."
    # Alternative: Take remote version completely
    git fetch origin
    git reset --hard origin/main
    git push -u origin main --force
fi
