#!/usr/bin/env bash
set -euo pipefail
root=$(git rev-parse --show-toplevel)
cd "$root"
if [[ $# -ne 2 || ! $1 =~ ^[a-z0-9][a-z0-9-]*$ || ! $2 =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo 'Usage : bash scripts/start-work.sh compte-a sujet-en-minuscules' >&2
  exit 1
fi
remote_url=$(git remote get-url origin)
case "$remote_url" in
  https://github.com/milles9m/Site-|https://github.com/milles9m/Site-.git|git@github.com:milles9m/Site-.git) ;;
  *) echo 'origin ne désigne pas milles9m/Site-; arrêt sans modification.' >&2; exit 1 ;;
esac
if [[ -n $(git status --porcelain) ]]; then
  echo 'Sauvegardez vos modifications avant de démarrer une autre tâche.' >&2
  exit 1
fi
git fetch origin
if ! git cat-file -e origin/main:dist/index.html 2>/dev/null; then
  echo 'Le site n’est pas encore dans main. Faire examiner et fusionner la PR d’import initiale.' >&2
  exit 1
fi
branch="codex/$1/$2-$(date -u +%Y%m%d-%H%M%S)"
git switch -c "$branch" origin/main
printf 'Branche de travail : %s\n' "$branch"
