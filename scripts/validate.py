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
for name in ('public-names.json', 'private-names.json'):
    if (root / name).exists():
        errors.append('Keep the maintainer name map outside this repository')
if not catalog.get('publicReleaseReady'):
    errors.append('The catalogue is not cleared for public release')
packages = [s['package'] for s in catalog['skills']]
if any(name.startswith('cad-') for name in packages):
    errors.append('Use independent repository package names')
if any('site' in skill or 'source_package' in skill for skill in catalog['skills']):
    errors.append('Do not publish the per-skill website/source crosswalk')
if len(packages) != len(set(packages)):
    errors.append('Duplicate skill package')
for relative, digest in catalog['files'].items():
    path = root / relative
    if not safe(Path(relative)) or path.is_symlink() or not path.is_file():
        errors.append(f'Unsafe or missing file: {relative}')
    elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        errors.append(f'Changed file: {relative}')
for skill in catalog['skills']:
    if not skill['original'] or skill.get('publication') != 'original-mit':
        errors.append(f'Uncleared package: {skill["package"]}')
    if skill['path'] != 'skills/' + skill['package'] or not re.fullmatch(r'[a-z0-9-]+', skill['package']):
        errors.append('Invalid skill path')
        continue
    path = root / skill['path'] / 'SKILL.md'
    body = path.read_text() if path.exists() else ''
    if not re.search(r'^name:\s*' + re.escape(skill['package']) + r'\s*$', body, re.M):
        errors.append(f'Entrypoint name mismatch: {skill["package"]}')
    heading = re.search(r'^# (.+)$', body, re.M)
    if not heading or heading.group(1) != skill['name']:
        errors.append(f'Heading mismatch: {skill["package"]}')
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
