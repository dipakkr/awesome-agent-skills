#!/usr/bin/env python3
"""Deterministic radial vessels, STL/3MF and an offline exact-mesh preview."""
import argparse
from collections import defaultdict
import html
import json
import math
from pathlib import Path
import re
import struct
import zipfile


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def validate_config(c):
    limits = {'height': (20, 180), 'diameter': (30, 160), 'wall': (2, 8),
              'base': (2, 10), 'flutes': (3, 24), 'amplitude': (0, 4),
              'twist': (-90, 90), 'taper': (-0.15, 0.15)}
    if set(c) != set(limits) | {'name', 'color'}:
        raise ValueError('Config keys must match the bundled example schema')
    for key, (lo, hi) in limits.items():
        if type(c[key]) not in (int, float) or not math.isfinite(c[key]) or not lo <= c[key] <= hi:
            raise ValueError(f'{key} must be a finite number in [{lo}, {hi}]')
    if type(c['flutes']) is not int:
        raise ValueError('flutes must be an integer')
    if not isinstance(c['name'], str) or not 1 <= len(c['name']) <= 80:
        raise ValueError('name must contain 1 to 80 characters')
    if not isinstance(c['color'], str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', c['color']):
        raise ValueError('color must be a six-digit hex color')
    if c['diameter']/2*(1-abs(c['taper']))-c['amplitude']-c['wall'] < 5:
        raise ValueError('Inner radius must remain at least 5 mm')
    if c['base'] >= c['height']/2:
        raise ValueError('Base must be less than half of the height')


def mesh(c):
    n, steps = 192, 60
    v, f = [], []
    def ring(z, inner=False):
        ids = []
        t = z/c['height']
        for i in range(n):
            a = i*2*math.pi/n
            r = c['diameter']/2*(1+c['taper']*t)
            r += c['amplitude']*math.cos(c['flutes']*(a-math.radians(c['twist'])*t))
            if inner:
                r -= c['wall']
            ids.append(len(v))
            v.append((r*math.cos(a), r*math.sin(a), z))
        return ids
    def join(a, b, reverse=False):
        for i in range(n):
            j = (i+1) % n
            faces = [(a[i], a[j], b[j]), (a[i], b[j], b[i])]
            f.extend(tuple(reversed(x)) if reverse else x for x in faces)
    outer = [ring(c['height']*j/steps) for j in range(steps+1)]
    inner = [ring(c['base']+(c['height']-c['base'])*j/steps, True) for j in range(steps+1)]
    for j in range(steps):
        join(outer[j], outer[j+1])
        join(inner[j], inner[j+1], True)
    join(outer[-1], inner[-1])
    bottom, floor = len(v), len(v)+1
    v.extend([(0, 0, 0), (0, 0, c['base'])])
    for i in range(n):
        j = (i+1) % n
        f.extend([(bottom, outer[0][j], outer[0][i]), (floor, inner[0][i], inner[0][j])])
    return v, f


def check(v, f):
    edges = defaultdict(list)
    adjacency = defaultdict(set)
    volume = 0
    for face in f:
        a, b, c = (v[i] for i in face)
        normal = cross(sub(b, a), sub(c, a))
        if dot(normal, normal) <= 1e-16:
            raise ValueError('Degenerate triangle')
        volume += dot(a, cross(b, c))/6
        for x, y in zip(face, face[1:]+face[:1]):
            edges[tuple(sorted((x, y)))].append((x, y))
            adjacency[x].add(y)
            adjacency[y].add(x)
    if any(len(e) != 2 or e[0] != e[1][::-1] for e in edges.values()):
        raise ValueError('Surface is not closed with consistent winding')
    visited, pending = set(), [0]
    while pending:
        i = pending.pop()
        if i not in visited:
            visited.add(i)
            pending.extend(adjacency[i]-visited)
    if len(visited) != len(v) or volume <= 0 or not all(math.isfinite(x) for p in v for x in p):
        raise ValueError('Disconnected, nonfinite or inverted mesh')
    bounds = [[min(p[i] for p in v), max(p[i] for p in v)] for i in range(3)]
    return {'vertices': len(v), 'triangles': len(f), 'closed_edge_manifold': True,
            'consistent_winding': True, 'connected_components': 1,
            'bounds_mm': bounds, 'size_mm': [round(b-a, 3) for a, b in bounds],
            'enclosed_material_volume_mm3': round(volume, 3),
            'status': 'Mesh checked; not slicer-tested or physically printed',
            'limits': ['No general self-intersection or minimum-wall-distance test',
                       'Wall input is radial thickness, not minimum normal thickness',
                       'No printer profile, toolpath, time or material estimate']}


def stl(v, f):
    result = bytearray(b'Parametric vessel; coordinates in millimeters'.ljust(80, b' '))
    result.extend(struct.pack('<I', len(f)))
    for face in f:
        a, b, c = (v[i] for i in face)
        normal = cross(sub(b, a), sub(c, a))
        length = math.sqrt(dot(normal, normal))
        result.extend(struct.pack('<12fH', *(x/length for x in normal), *a, *b, *c, 0))
    return result


def write_3mf(path, v, f):
    vertices = ''.join(f'<vertex x="{x:.9f}" y="{y:.9f}" z="{z:.9f}"/>' for x, y, z in v)
    triangles = ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in f)
    model = f'<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources><object id="1" type="model"><mesh><vertices>{vertices}</vertices><triangles>{triangles}</triangles></mesh></object></resources><build><item objectid="1"/></build></model>'
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels', '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel" Target="/3D/3dmodel.model"/></Relationships>')
        z.writestr('3D/3dmodel.model', model)


def preview(c, v, f, report):
    template = (Path(__file__).parent.parent/'assets/preview.html').read_text()
    data = json.dumps({'config': c, 'vertices': v, 'faces': f, 'report': report}, separators=(',', ':')).replace('<', '\\u003c')
    return template.replace('__TITLE__', html.escape(c['name'])).replace('__MESH_DATA__', data)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    try:
        c = json.loads(args.config.read_text())
        validate_config(c)
        if args.out.exists():
            raise ValueError('Output path exists; choose a new directory')
        v, f = mesh(c)
        report = check(v, f)
        page = preview(c, v, f, report)
        args.out.mkdir(parents=True)
        for name, data in [('parameters', c), ('mesh', {'vertices': v, 'faces': f}), ('checks', report)]:
            (args.out/f'{name}.json').write_text(json.dumps(data, indent=2)+'\n')
        (args.out/'model.stl').write_bytes(stl(v, f))
        write_3mf(args.out/'model.3mf', v, f)
        (args.out/'preview.html').write_text(page)
        print(json.dumps({'output': str(args.out), **report}, indent=2))
    except (ValueError, OSError) as error:
        p.error(str(error))


if __name__ == '__main__':
    main()
