#!/usr/bin/env python3
"""Compare les chemins et les SHA Git locaux à l'arbre réellement stocké sur GitHub."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
def run(args):
    return subprocess.check_output(args, cwd=ROOT, text=True)
sha = run(['git', 'rev-parse', 'HEAD']).strip()
local = {}
for entry in run(['git', 'ls-tree', '-r', '-z', 'HEAD']).split('\0'):
    if entry:
        metadata, path = entry.split('\t', 1)
        _, kind, digest = metadata.split()
        if kind == 'blob':
            local[path] = digest
remote = json.loads(run(['gh', 'api', f'repos/milles9m/Site-/git/trees/{sha}?recursive=1']))
if remote.get('truncated'):
    sys.exit('Arbre GitHub tronqué; comparaison incomplète.')
actual = {entry['path']: entry['sha'] for entry in remote['tree'] if entry['type'] == 'blob'}
if actual != local:
    sys.exit('Les fichiers GitHub ne correspondent pas intégralement au commit local.')
print(f'Vérifié sur GitHub : {len(local)} fichiers identiques au commit {sha}.')
