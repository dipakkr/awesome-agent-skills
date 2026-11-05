#!/usr/bin/env python3
"""Validate the standalone collection, with no access to the website workspace."""
import hashlib
import json
import re
from pathlib import Path
from sync import safe, SKIP_DIRS

root = Path(__file__).resolve().parents[1]
catalog = json.loads((root / 'catalog.json').read_text())
errors = []
packages = [s['package'] for s in catalog['skills']]
if len(packages) != len(set(packages)):
    errors.append('Duplicate skill package')
for relative, digest in catalog['files'].items():
    path = root / relative
    if not safe(Path(relative)) or path.is_symlink() or not path.is_file():
        errors.append(f'Unsafe or missing file: {relative}')
    elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        errors.append(f'Changed file: {relative}')
for skill in catalog['skills']:
    path = root / skill['path'] / 'SKILL.md'
    body = path.read_text() if path.exists() else ''
    if not re.search(r'^name:\s*' + re.escape(skill['package']) + r'\s*$', body, re.M):
        errors.append(f'Entrypoint name mismatch: {skill["package"]}')
    if not re.search(r'^description:\s*\S', body, re.M):
        errors.append(f'Missing description: {skill["package"]}')
    if skill['original'] and not (root / skill['path'] / 'LICENSE.txt').is_file():
        errors.append(f'Missing original licence: {skill["package"]}')
for path in (root / 'skills').rglob('*'):
    if path.is_symlink():
        errors.append(f'Symlink: {path.relative_to(root)}')
    if path.is_file() and not set(path.parts) & SKIP_DIRS:
        if path.relative_to(root).as_posix() not in catalog['files']:
            errors.append(f'Unrecorded file: {path.relative_to(root)}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Validated {len(packages)} skills and {len(catalog["files"])} source files.')
print('Public release ready:', catalog['publicReleaseReady'])
