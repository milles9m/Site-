#!/usr/bin/env bash
set -euo pipefail
root=$(git rev-parse --show-toplevel)
cd "$root"
branch=$(git branch --show-current)
if [[ "$branch" != export/site-complet-2026-10-31 ]]; then
  echo 'Ce script termine uniquement la branche d’import préparée.' >&2
  exit 1
fi
case "$(git remote get-url origin)" in
  https://github.com/milles9m/Site-.git|git@github.com:milles9m/Site-.git) ;;
  *) echo 'origin inattendu; aucun envoi effectué.' >&2; exit 1 ;;
esac
if [[ -n $(git status --porcelain) ]]; then
  echo 'La branche doit être propre et les changements enregistrés.' >&2
  exit 1
fi
python3 scripts/check-site.py
node --check dist/app.js
git fetch origin
if ! git merge-base --is-ancestor origin/main HEAD; then
  echo 'main a changé : intégrer origin/main et revérifier avant de relancer.' >&2
  exit 1
fi
git -c 'credential.helper=!gh auth git-credential' push -u origin "$branch"
python3 scripts/verify-github.py
url=$(gh pr list --repo milles9m/Site- --head "$branch" --base main --state open --json url --jq '.[0].url // empty')
if [[ -n "$url" ]]; then
  printf '%s\n' "$url"
else
  gh pr create --repo milles9m/Site- --base main --head "$branch" --title 'Importer le site complet et préparer la collaboration Codex' --body-file docs/PULL_REQUEST.md
fi
printf 'Fichiers : https://github.com/milles9m/Site-/tree/%s/dist\n' "$branch"
