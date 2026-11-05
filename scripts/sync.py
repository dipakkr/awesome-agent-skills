#!/usr/bin/env python3
"""Import the site's skill sources without overwriting locally edited exports."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', '.pytest_cache', '.next'}
RENDER_EXTENSIONS = {'.mp4', '.webm', '.mov', '.wav', '.mp3', '.gif', '.pptx', '.pdf', '.html', '.stl', '.3mf'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def excluded(relative):
    parts = relative.parts
    if any(p in SKIP_DIRS for p in parts) or relative.name in {'.DS_Store', 'validation.json'}:
        return 'runtime/cache'
    if 'examples' in parts and ('recorded' in parts or relative.suffix.lower() in RENDER_EXTENSIONS):
        return 'rendered example; see website'
    return None


def safe(relative):
    return not (relative.is_absolute() or '..' in relative.parts or
                any(p.startswith('.env') for p in relative.parts) or
                relative.name in {'credentials.json', 'secrets.json', 'id_rsa', 'id_ed25519'} or
                relative.suffix.lower() in {'.pem', '.key', '.p12', '.pfx'})


def plan(workspace):
    catalog = json.loads((workspace / 'fe/src/data/studio/edition-catalog.json').read_text())['skills']
    records = [{
        'package': s['package'], 'name': s['name'], 'description': s['description'],
        'site': 'https://claudeai.directory/skills/' + s['slug'],
        'kind': 'catalogue', 'original': s.get('original') is True,
    } for s in catalog]
    for path in sorted((workspace / 'fe/src/data/studio/profiles').glob('*-downloads.json')):
        for item in json.loads(path.read_text()):
            if item['skill'] not in {s['package'] for s in records}:
                name = item['skill']
                body = (workspace / '.agents/skills' / name / 'SKILL.md').read_text()
                records.append({
                    'package': name, 'name': re.search(r'^# (.+)$', body, re.M).group(1),
                    'description': re.search(r'^description: (.+)$', body, re.M).group(1),
                    'site': 'https://claudeai.directory/skills/for/' + path.stem.replace('-downloads', '-founders'),
                    'kind': 'profile', 'original': 'ownership: original-workflow' in body,
                })
    files, omitted = {}, []
    for record in sorted(records, key=lambda s: s['package']):
        name = record['package']
        if not re.fullmatch(r'[a-z0-9-]+', name):
            raise ValueError('Invalid package name')
        source = workspace / '.agents/skills' / name
        if not (source / 'SKILL.md').is_file():
            raise ValueError(f'Missing skill: {name}')
        record['path'] = 'skills/' + name
        record['publication'] = 'original-mit' if record['original'] else 'third-party-review-required'
        for folder, directories, names in os.walk(source, followlinks=False):
            for directory in directories:
                if (Path(folder) / directory).is_symlink():
                    raise ValueError(f'Symlink in {name}')
            directories[:] = sorted(d for d in directories if d not in SKIP_DIRS)
            for filename in sorted(names):
                path = Path(folder) / filename
                relative = path.relative_to(source)
                if path.is_symlink() or not safe(relative):
                    raise ValueError(f'Unexpected private file or symlink: {name}/{relative}')
                reason = excluded(relative)
                target = f'skills/{name}/{relative.as_posix()}'
                if reason:
                    omitted.append({'path': target, 'reason': reason})
                else:
                    files[target] = path.read_bytes()
        if record['original']:
            # The owner's open-source direction applies to our original packages.
            # Preserve all nested third-party notices; change only our root licence.
            files[f'skills/{name}/LICENSE.txt'] = (REPO / 'LICENSE').read_bytes()
    records.sort(key=lambda s: s['package'])
    manifest = {
        'schemaVersion': 1,
        'source': 'Site catalogue and profile downloads; authoring sources in .agents/skills',
        'publicReleaseReady': not any(not s['original'] for s in records),
        'skills': records,
        'files': {p: sha(data) for p, data in sorted(files.items())},
        'omitted': sorted(omitted, key=lambda x: x['path']),
    }
    return files, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, default=REPO.parent)
    parser.add_argument('--check', action='store_true', help='Check source coverage and byte parity without writing')
    args = parser.parse_args()
    files, manifest = plan(args.workspace.resolve())
    manifest_path = REPO / 'catalog.json'
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {'files': {}}
    # Check every conflict before writing anything. Local edits must be reconciled
    # back to the authoring sources explicitly, not discarded by a bulk sync.
    for relative, data in files.items():
        target = REPO / relative
        if target.exists() and target.read_bytes() != data:
            if sha(target.read_bytes()) != previous['files'].get(relative):
                raise ValueError(f'Locally modified export: {relative}; reconcile before syncing')
    removed = set(previous['files']) - set(files)
    if removed:
        raise ValueError(f'Source removals need explicit review: {sorted(removed)}')
    catalog_bytes = (json.dumps(manifest, indent=2, ensure_ascii=False) + '\n').encode()
    files['catalog.json'] = catalog_bytes
    rows = ['# Skill source index', '',
            'Preview outputs, download a packaged skill and find usage examples on its website page.', '',
            '| Skill | Source | Website | Source status |',
            '| --- | --- | --- | --- |']
    for skill in manifest['skills']:
        status = 'Original / MIT' if skill['original'] else 'Third-party review required'
        rows.append(f'| {skill["name"]} | [Files]({skill["path"]}/SKILL.md) | [Preview and download]({skill["site"]}) | {status} |')
    files['CATALOG.md'] = ('\n'.join(rows) + '\n').encode()
    drift = [p for p, data in files.items() if not (REPO / p).is_file() or (REPO / p).read_bytes() != data]
    if args.check:
        if drift:
            raise ValueError(f'{len(drift)} files need sync; first: {drift[0]}')
    else:
        for relative in drift:
            target = REPO / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(files[relative])
    print(json.dumps({'skills': len(manifest['skills']), 'files': len(manifest['files']),
                      'changed': 0 if args.check else len(drift),
                      'publicReleaseReady': manifest['publicReleaseReady']}))


if __name__ == '__main__':
    main()
