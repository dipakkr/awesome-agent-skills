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


def public_bytes(data, relative, mapping, originals):
    # Keep historical evidence and third-party attribution byte-for-byte.
    lower = relative.name.lower()
    if any(word in lower for word in ('license', 'licence', 'copyright', 'ofl', 'provenance', 'receipt', 'manifest')):
        return data
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return data
    for source, identity in sorted(mapping.items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(source, identity['package'])
    for source, record in sorted(originals.items(), key=lambda item: len(item[1]['name']), reverse=True):
        text = text.replace(record['name'], mapping[source]['name'])
    # Generic publisher references are fine; remove direct product/demo routing.
    text = re.sub(r'https?://(?:www\.)?claudeai\.directory/(?:skills|studio)/[^\s\)\]\"<>]+',
                  'https://claudeai.directory/skills', text)
    return text.encode('utf-8')


def plan(workspace, selected, mapping):
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
    records = [record for record in records if record['original']]
    original_records = {record['package']: dict(record) for record in records}
    for record in records:
        identity = mapping[record['package']]
        record['source_package'] = record['package']
        record['package'] = identity['package']
        record['name'] = identity['name']
        record['description'] = record['description'].replace(original_records[record['source_package']]['name'], identity['name'])
        record.pop('site', None)
    eligible = {record['package'] for record in records}
    if selected - eligible:
        raise ValueError(f'Not an eligible original site skill: {sorted(selected - eligible)}')
    records = [record for record in records if record['package'] in selected]
    files, omitted = {}, []
    for record in sorted(records, key=lambda s: s['package']):
        name = record['package']
        if not re.fullmatch(r'[a-z0-9-]+', name):
            raise ValueError('Invalid package name')
        source_name = record.pop('source_package')
        source = workspace / '.agents/skills' / source_name
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
                    files[target] = public_bytes(path.read_bytes(), relative, mapping, original_records)
        if record['original']:
            # The owner's open-source direction applies to our original packages.
            # Preserve all nested third-party notices; change only our root licence.
            files[f'skills/{name}/LICENSE.txt'] = (REPO / 'LICENSE').read_bytes()
    records.sort(key=lambda s: s['package'])
    manifest = {
        'schemaVersion': 1,
        'source': 'Full reusable source, with repository-specific package names',
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
    parser.add_argument('--skill', help='Add one original skill; existing packages remain included')
    parser.add_argument('--mapping', type=Path, help='Private maintainer name map; never commit this mapping')
    parser.add_argument('--migrate-names', action='store_true', help='Rename existing imported packages using the private map')
    args = parser.parse_args()
    mapping_path = args.mapping or args.workspace / 'docs/products/skills-repository/public-names.json'
    mapping = json.loads(mapping_path.read_text())
    public_ids = [entry['package'] for entry in mapping.values()]
    if len(public_ids) != len(set(public_ids)) or any(not re.fullmatch(r'[a-z0-9-]+', name) for name in public_ids):
        raise ValueError('Invalid or duplicate public package names')
    manifest_path = REPO / 'catalog.json'
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {'skills': [], 'files': {}}
    selected = {skill['package'] for skill in previous['skills']}
    if args.migrate_names:
        selected = {mapping[name]['package'] if name in mapping else name for name in selected}
        for relative, digest in previous['files'].items():
            path = REPO / relative
            if not path.is_file() or sha(path.read_bytes()) != digest:
                raise ValueError(f'Changed source cannot be renamed: {relative}')
    if args.skill:
        selected.add(args.skill)
    files, manifest = plan(args.workspace.resolve(), selected, mapping)
    # Check every conflict before writing anything. Local edits must be reconciled
    # back to the authoring sources explicitly, not discarded by a bulk sync.
    for relative, data in files.items():
        target = REPO / relative
        if target.exists() and target.read_bytes() != data:
            if sha(target.read_bytes()) != previous['files'].get(relative):
                raise ValueError(f'Locally modified export: {relative}; reconcile before syncing')
    removed = set(previous['files']) - set(files)
    if removed and not args.migrate_names:
        raise ValueError(f'Source removals need explicit review: {sorted(removed)}')
    catalog_bytes = (json.dumps(manifest, indent=2, ensure_ascii=False) + '\n').encode()
    files['catalog.json'] = catalog_bytes
    rows = ['# Skill source index', '',
            'Choose a workflow, then open its instructions and supporting source files.', '',
            '| Skill | What it helps you do |',
            '| --- | --- |']
    for skill in manifest['skills']:
        description = skill['description'].replace('|', '/').replace('\n', ' ')
        rows.append(f'| [{skill["name"]}]({skill["path"]}/SKILL.md) | {description} |')
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
        for relative in removed:
            (REPO / relative).unlink()
        for folder in sorted((REPO / 'skills').rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()
    print(json.dumps({'skills': len(manifest['skills']), 'files': len(manifest['files']),
                      'changed': 0 if args.check else len(drift),
                      'publicReleaseReady': manifest['publicReleaseReady']}))


if __name__ == '__main__':
    main()
