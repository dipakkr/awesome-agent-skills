#!/usr/bin/env python3
"""Render an offline decision workbook. Python standard library only."""
import argparse
import csv
import html
import json
import re
from pathlib import Path


def validate(data):
    for key in ('title', 'brand', 'purpose', 'disclosure'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f'Missing text: {key}')
    if data.get('accent') not in ('lime', 'coral', 'blue', 'lavender'):
        raise ValueError('Choose a supported accent')
    if not isinstance(data.get('sources'), list) or not isinstance(data.get('cards'), list) or not data['cards']:
        raise ValueError('Supply sources and at least one card')
    ids = set()
    for source in data['sources']:
        for key in ('id', 'label', 'text', 'locator'):
            if not isinstance(source.get(key), str) or not source[key].strip():
                raise ValueError(f'Missing source {key}')
        if source['id'] in ids:
            raise ValueError('Duplicate source ID')
        ids.add(source['id'])
    card_ids = set()
    for card in data['cards']:
        if not re.fullmatch(r'[A-Za-z0-9-]+', card.get('id', '')) or card['id'] in card_ids:
            raise ValueError('Invalid or duplicate card ID')
        card_ids.add(card['id'])
        for key in ('title', 'decision', 'next'):
            if not isinstance(card.get(key), str) or not card[key].strip():
                raise ValueError(f'Missing card {key}')
        if card.get('status') not in ('Ready', 'Explore', 'Hold'):
            raise ValueError('Invalid card status')
        if not isinstance(card.get('evidence'), list) or not set(card['evidence']) <= ids:
            raise ValueError('Unknown evidence reference')
        if card['status'] == 'Ready' and not card['evidence']:
            raise ValueError('Ready cards need evidence; use Explore for unsupported hypotheses')
        if not isinstance(card.get('fields'), dict) or not card['fields'] or not all(isinstance(k, str) and isinstance(v, str) for k, v in card['fields'].items()):
            raise ValueError('Supply text fields')
        if not isinstance(card.get('note', ''), str):
            raise ValueError('Notes must be text')
    return data


def csv_cell(value):
    value = str(value)
    return "'" + value if value.lstrip().startswith(('=', '+', '-', '@')) else value


def render(data):
    validate(data)
    esc = html.escape
    cards = []
    for index, card in enumerate(data['cards'], 1):
        fields = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in card['fields'].items())
        refs = ' '.join(f'<a href="#source-{esc(ref, quote=True)}">{esc(ref)}</a>' for ref in card['evidence']) or 'No evidence yet'
        cards.append(f'''<article data-status="{card['status']}" data-id="{card['id']}">
<div class="card-top"><span class="index">{index:02}</span><span class="status {card['status'].lower()}">{card['status']}</span></div>
<h2>{esc(card['title'])}</h2><p class="decision">{esc(card['decision'])}</p><dl>{fields}</dl>
<div class="next"><strong>Next action</strong><p>{esc(card['next'])}</p></div>
<div class="refs">Evidence {refs}</div><label for="note-{card['id']}">Working notes</label>
<textarea id="note-{card['id']}" placeholder="Add a decision or owner. Export JSON to keep edits.">{esc(card.get('note', ''))}</textarea></article>''')
    sources = ''.join(f'<details id="source-{esc(s["id"], quote=True)}"><summary>{esc(s["id"])} · {esc(s["label"])}</summary><p>{esc(s["text"])}</p><small>{esc(s["locator"])}</small></details>' for s in data['sources'])
    payload = json.dumps(data, ensure_ascii=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return TEMPLATE.replace('@@TITLE@@', esc(data['title'])).replace('@@BRAND@@', esc(data['brand'])).replace('@@PURPOSE@@', esc(data['purpose'])).replace('@@DISCLOSURE@@', esc(data['disclosure'])).replace('@@ACCENT@@', data['accent']).replace('@@COUNT@@', str(len(cards))).replace('@@CARDS@@', ''.join(cards)).replace('@@SOURCES@@', sources).replace('@@DATA@@', payload)


TEMPLATE = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>@@TITLE@@ · @@BRAND@@</title>
<style>
:root{--ink:#172d32;--paper:#f5f3eb;--accent:#d7ed86}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,sans-serif}body[data-accent=coral]{--accent:#ffb59c}body[data-accent=blue]{--accent:#a8d9f2}body[data-accent=lavender]{--accent:#d3bff3}button,textarea,select{font:inherit}button,select{padding:10px 16px;border:1px solid #b7c3bc;border-radius:6px;background:transparent;color:inherit;cursor:pointer}button:hover{background:var(--accent)}button:focus-visible,a:focus-visible,textarea:focus-visible,select:focus-visible{outline:3px solid #4475d5;outline-offset:3px}aside{width:235px;background:var(--ink);color:#eff2e9;padding:36px 28px;position:fixed;inset:0 auto 0 0;display:flex;flex-direction:column;gap:32px}aside .brand{font-weight:750;font-size:24px;letter-spacing:-1px}aside small{color:#b9cec6}aside nav{display:grid;gap:20px}aside a{color:inherit;text-decoration:none}aside .stamp{margin-top:auto;padding-top:25px;border-top:1px solid #647471}aside .mark{width:46px;height:46px;border-radius:50%;background:var(--accent);color:var(--ink);display:grid;place-items:center;font-size:23px;font-weight:800}main{margin-left:235px;padding:44px 42px;max-width:1800px}.eyebrow{text-transform:uppercase;font-size:12px;letter-spacing:2px;font-weight:750}header{padding-bottom:28px;border-bottom:1px solid #bcc5ba}h1{font-size:clamp(32px,4vw,58px);line-height:1.05;letter-spacing:-2px;max-width:850px;margin:16px 0}header p{max-width:830px;font-size:18px;color:#52665f}.disclosure{font-size:12px;background:#e8eade;border-left:3px solid var(--ink);padding:9px 12px}.toolbar{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin:24px 0}.toolbar label{font-size:13px}.toolbar .count{margin-right:auto;font-size:13px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}article{background:#fffef8;border:1px solid #d8ded1;border-radius:10px;padding:25px;overflow-wrap:anywhere}article[hidden]{display:none}.card-top{display:flex;justify-content:space-between;align-items:center}.index{font-size:28px;font-weight:750;color:#788d80}.status{padding:4px 11px;border-radius:20px;font-size:12px;font-weight:700}.ready{background:#deedba}.explore{background:#dcebf4}.hold{background:#f6d8cc}h2{font-size:23px;line-height:1.2;letter-spacing:-.5px;margin:18px 0 12px}.decision{font-size:16px;font-weight:600}dl{margin:22px 0}dl div{border-top:1px solid #e4e7dc;padding:11px 0}dt{font-size:11px;letter-spacing:1px;text-transform:uppercase;font-weight:700;color:#60746a}dd{margin:5px 0 0;font-size:14px}.next{padding:14px;background:var(--accent);border-radius:5px}.next strong{font-size:11px;text-transform:uppercase;letter-spacing:1px}.next p{margin:5px 0;font-size:14px}.refs{font-size:12px;margin:18px 0}.refs a{color:inherit;border-bottom:1px solid;margin-left:8px;text-decoration:none}article label{font-size:12px;display:block;margin:8px 0}textarea{display:block;width:100%;min-height:62px;resize:vertical;border:1px solid #c8d0c2;border-radius:5px;background:transparent;padding:9px;color:inherit;font-size:13px}#sources{margin-top:38px}#sources details{padding:15px 0;border-bottom:1px solid #c5cfc1}summary{cursor:pointer;font-weight:600}details p{max-width:850px}details small{color:#52665f;overflow-wrap:anywhere}footer{margin:28px 0;font-size:12px;color:#52665f}#message{min-height:22px;font-size:13px}#empty{padding:35px} @media(max-width:800px){aside{position:static;width:auto;padding:18px 22px;display:flex;flex-direction:row;align-items:center;gap:16px}aside nav,aside .stamp,aside small{display:none}aside .brand{font-size:20px}aside .mark{width:32px;height:32px;font-size:18px}main{margin:0;padding:26px 18px}.grid{grid-template-columns:1fr}h1{letter-spacing:-1px}.toolbar .count{flex-basis:100%}article{padding:20px}}@media print{aside,.toolbar,textarea,article label,#message{display:none}main{margin:0;padding:0}.grid{display:block}article{break-inside:avoid;margin:15px 0}details{display:block}details p{display:block}}
</style></head><body data-accent="@@ACCENT@@"><aside><div class="mark">C</div><div class="brand">Creative<br>fieldwork.</div><small>@@BRAND@@</small><nav><a href="#board">01 / Decision board</a><a href="#sources">02 / Evidence ledger</a></nav><div class="stamp"><small>CLAUDE DIRECTORY<br>Original strategy workbooks</small></div></aside><main id="board"><header><div class="eyebrow">@@BRAND@@ / Strategy workbook</div><h1>@@TITLE@@</h1><p>@@PURPOSE@@</p><div class="disclosure">@@DISCLOSURE@@</div></header><div class="toolbar"><span class="count" id="count">@@COUNT@@ decisions</span><label for="filter">Show</label><select id="filter"><option>All</option><option>Ready</option><option>Explore</option><option>Hold</option></select><button id="export">Export edited JSON</button><button id="csv">Export decision CSV</button></div><p id="message" role="status">Notes stay in this tab until you export. Reloading discards unsaved edits.</p><div class="grid">@@CARDS@@</div><p id="empty" hidden>No decisions have this status.</p><section id="sources"><div class="eyebrow">Trace the reasoning</div><h2>Evidence ledger</h2>@@SOURCES@@</section><footer>Ready means supported enough for the stated next action. It is not a prediction of advertising results.</footer></main><script type="application/json" id="data">@@DATA@@</script><script>
const data=JSON.parse(document.getElementById('data').textContent);
document.getElementById('filter').addEventListener('change',event=>{let count=0;document.querySelectorAll('article').forEach(card=>{card.hidden=event.target.value!=='All'&&card.dataset.status!==event.target.value;if(!card.hidden)count++});document.getElementById('count').textContent=count+' decisions';document.getElementById('empty').hidden=count!==0});
document.querySelectorAll('.refs a').forEach(link=>link.addEventListener('click',()=>{document.getElementById(link.hash.slice(1)).open=true}));
function current(){data.cards.forEach(card=>{card.note=document.getElementById('note-'+card.id).value});return data}
function save(content,type,name){const url=URL.createObjectURL(new Blob([content],{type}));const link=document.createElement('a');link.href=url;link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);document.getElementById('message').textContent='Exported '+name+'. Your current notes are included.'}
document.getElementById('export').addEventListener('click',()=>save(JSON.stringify(current(),null,2),'application/json','workbook.json'));
const cell=value=>{let text=String(value);if(/^[\\s]*[=+@-]/.test(text))text="'"+text;return '"'+text.replaceAll('"','""')+'"'};
document.getElementById('csv').addEventListener('click',()=>{const rows=[['id','status','title','decision','fields','next','evidence','note'],...current().cards.map(c=>[c.id,c.status,c.title,c.decision,JSON.stringify(c.fields),c.next,c.evidence.join(' | '),c.note])];save(rows.map(r=>r.map(cell).join(',')).join('\\r\\n'),'text/csv;charset=utf-8','decisions.csv')});
</script></body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    data = validate(json.loads(args.source.read_text()))
    if args.output.exists():
        raise SystemExit('Use a new output directory to preserve previous work')
    args.output.mkdir(parents=True)
    (args.output / 'index.html').write_text(render(data))
    (args.output / 'workbook.json').write_text(json.dumps(data, indent=2) + '\n')
    with (args.output / 'decisions.csv').open('w', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['id', 'status', 'title', 'decision', 'fields', 'next', 'evidence', 'note'])
        for c in data['cards']:
            writer.writerow(map(csv_cell, [c['id'], c['status'], c['title'], c['decision'], json.dumps(c['fields']), c['next'], ' | '.join(c['evidence']), c.get('note', '')]))
    print(args.output / 'index.html')


if __name__ == '__main__':
    main()
