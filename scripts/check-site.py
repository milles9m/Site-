#!/usr/bin/env python3
"""Vérifie les fichiers du site et les secrets suivis, sans afficher leur contenu."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
errors = []

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.refs = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('img', 'script', 'iframe', 'source') and attrs.get('src'):
            self.refs.append(attrs['src'])
        if tag in ('a', 'link', 'image') and attrs.get('href'):
            self.refs.append(attrs['href'])

pages = {}
for filename in ('index.html', 'en.html'):
    path = DIST / filename
    if not path.is_file():
        errors.append(f'Page absente : {filename}')
        continue
    page = Page()
    page.feed(path.read_text(encoding='utf-8'))
    pages[filename] = page
    if len(page.ids) != len(set(page.ids)):
        errors.append(f'Identifiants HTML dupliqués : {filename}')

for filename, page in pages.items():
    for ref in page.refs:
        parsed = urlsplit(ref)
        if parsed.scheme or parsed.netloc:
            continue
        relative = unquote(parsed.path)
        target = (DIST / relative.lstrip('/')).resolve() if relative else DIST / filename
        if not target.is_relative_to(DIST.resolve()):
            errors.append(f'Référence hors de dist : {filename}')
            continue
        if not target.is_file():
            errors.append(f'Fichier référencé absent : {filename} -> {relative}')
        elif parsed.fragment and target.suffix == '.html':
            target_page = pages.get(target.name)
            if target_page and unquote(parsed.fragment) not in target_page.ids:
                errors.append(f'Ancre absente : {filename} -> {ref}')

patterns = {
    'clé privée': rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'jeton GitHub': rb'(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,})',
    'clé AWS': rb'AKIA[A-Z0-9]{16}',
    'clé API': rb'sk-(?:proj-)?[A-Za-z0-9_-]{30,}',
    'identifiant temporaire Sites': rb'art_v2_[A-Za-z0-9_]{20,}',
}
tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
for name in filter(None, tracked):
    path = ROOT / name
    lower = path.name.lower()
    sensitive = (lower == '.env' or lower.startswith('.env.') and lower != '.env.example'
                 or path.suffix.lower() in ('.pem', '.key', '.p12', '.pfx')
                 or any(part in ('.ssh', '.aws', 'secrets') for part in path.parts)
                 or lower in ('credentials.json', 'id_rsa', 'id_ed25519', '.netrc', '.npmrc', '.git-credentials'))
    if sensitive:
        errors.append(f'Fichier sensible suivi : {name}')
    if not path.is_file() or path.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.ico'):
        continue
    data = path.read_bytes()
    for label, pattern in patterns.items():
        if re.search(pattern, data):
            errors.append(f'Secret potentiel ({label}) : {name}; valeur non affichée')
if errors:
    for error in errors:
        print(error, file=sys.stderr)
    sys.exit(1)
print('OK : pages FR/EN, fichiers et ancres locales; aucun secret détecté dans les fichiers suivis.')
