#!/usr/bin/env bash
set -euo pipefail
root=$(git rev-parse --show-toplevel)
cd "$root"
branch=$(git branch --show-current)
case "$branch" in
  codex/*/*) ;;
  *) echo 'Publier depuis une branche codex/compte/sujet, jamais main.' >&2; exit 1 ;;
esac
remote_url=$(git remote get-url origin)
case "$remote_url" in
  https://github.com/milles9m/Site-|https://github.com/milles9m/Site-.git|git@github.com:milles9m/Site-.git) ;;
  *) echo 'Dépôt origin inattendu; arrêt sans envoi.' >&2; exit 1 ;;
esac
if [[ -n $(git status --porcelain) ]]; then
  echo 'Enregistrez et vérifiez vos changements avant de publier.' >&2
  exit 1
fi
python3 scripts/check-site.py
node --check dist/app.js
git fetch origin
if ! git merge-base --is-ancestor origin/main HEAD; then
  echo 'Intégrer origin/main dans cette branche, résoudre les conflits et revérifier avant l’envoi.' >&2
  exit 1
fi
git push -u origin "$branch"
if gh pr view "$branch" --repo milles9m/Site- --json url --jq .url; then
  exit 0
fi
gh pr create --repo milles9m/Site- --base main --head "$branch" --fill
