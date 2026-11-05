#!/usr/bin/env python3
"""Export evidence-linked copy and variants as new Shopify draft products. No network."""
import argparse
import csv
import hashlib
import html
import io
import json
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), f'{label} must be nonempty text')
    require(not any(ord(c) < 32 and c not in '\n\r\t' for c in value), f'{label} contains control characters')
    require(not value.lstrip().startswith(('=', '+', '-', '@')) and not value.startswith(('\t','\r','\n')), f'{label} has an unsafe spreadsheet prefix; revise it before export')
    return value


def unique(rows, key, label):
    require(isinstance(rows, list), f'{label} must be a list')
    require(all(isinstance(row, dict) and isinstance(row.get(key), str) and row[key].strip() for row in rows), f'{label} needs {key} values')
    result = {row[key]: row for row in rows}
    require(len(result) == len(rows), f'Duplicate {label} {key}')
    return result


def csv_bytes(headers, rows):
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=headers, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode('utf-8')


def build(context_bytes, copy_bytes):
    context, copy = json.loads(context_bytes), json.loads(copy_bytes)
    require(isinstance(context, dict) and isinstance(copy, dict), 'Inputs must be JSON objects')
    require(context.get('schema_version') == 1, 'Unsupported context schema')
    digest = hashlib.sha256(context_bytes).hexdigest()
    require(copy.get('context_sha256') == digest, 'Context changed: review and regenerate listing copy')
    business = context.get('business', {})
    require(isinstance(business, dict), 'Missing business context')
    require(str(business.get('platform', '')).casefold() == 'shopify', 'This export supports Shopify only')
    currency = business.get('currency')
    require(isinstance(currency, str) and re.fullmatch('[A-Z]{3}', currency), 'Confirm the store currency before CSV export')
    sources = unique(context.get('sources'), 'id', 'sources')
    for source in sources.values():
        text(source.get('label'), 'Source label')
        text(source.get('excerpt'), 'Source excerpt')
    products = unique(context.get('products'), 'id', 'products')
    drafts = unique(copy.get('products'), 'id', 'listing products')
    require(bool(drafts), 'Select at least one product')
    require(set(drafts) <= set(products), 'Copy refers to an unknown product')
    require(isinstance(context.get('questions'), list) and all(isinstance(q, str) for q in context['questions']), 'Questions must be a list of strings')
    seen_handles, seen_skus, max_options = set(), set(), 1
    prepared = []
    ledger = []
    for product_id, draft in drafts.items():
        product = products[product_id]
        handle = product.get('handle')
        require(isinstance(handle, str) and re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', handle), 'Invalid product handle')
        require(handle not in seen_handles, 'Duplicate product handle')
        seen_handles.add(handle)
        title = text(draft.get('title'), 'Listing title')
        facts = unique(product.get('facts'), 'id', f'{product_id} facts')
        bullets = draft.get('bullets')
        require(isinstance(bullets, list), 'Bullets must be a list')
        claims = [draft.get('summary')] + bullets
        for claim in claims:
            require(isinstance(claim, dict), 'Each claim must have text and fact_ids')
            wording = text(claim.get('text'), 'Claim')
            refs = claim.get('fact_ids')
            require(isinstance(refs, list) and refs and all(isinstance(ref,str) for ref in refs), 'Each claim needs fact IDs')
            for ref in dict.fromkeys(refs):
                require(ref in facts and facts[ref].get('status') == 'confirmed', f'{product_id}: claim uses unknown or unconfirmed fact {ref}')
                fact = facts[ref]
                require(isinstance(fact.get('source'),str) and fact['source'] in sources, 'Fact source is missing')
                source = sources[fact['source']]
                ledger.append({'Product ID':product_id,'Claim':wording,'Fact ID':ref,'Fact':text(fact.get('text'),'Fact'),'Source':source['label'],'Source excerpt':source['excerpt']})
        variants = product.get('variants')
        require(isinstance(variants,list) and variants, 'Each product needs at least one variant')
        names = None
        combinations = set()
        for variant in variants:
            require(isinstance(variant,dict), 'Variant must be an object')
            sku = text(variant.get('sku'), 'SKU')
            require(sku not in seen_skus, 'Duplicate SKU')
            seen_skus.add(sku)
            require(isinstance(variant.get('source'),str) and variant['source'] in sources, 'Variant source missing')
            price = variant.get('price')
            require(isinstance(price,str) and re.fullmatch(r'(?:0|[1-9][0-9]*)(?:\.[0-9]{1,2})?', price), f'{sku}: confirm a nonnegative price with at most two decimals')
            options = variant.get('options')
            require(isinstance(options,list) and len(options)<=3, 'Provide zero to three variant options')
            require(all(isinstance(o,dict) for o in options), 'Invalid variant option')
            current_names = tuple(text(o.get('name'),'Option name') for o in options)
            values = tuple(text(o.get('value'),'Option value') for o in options)
            require(len(set(current_names)) == len(current_names), 'Duplicate option names')
            if names is None:
                names = current_names
            require(current_names == names, 'All variants must preserve the same option names and order')
            require(values not in combinations, 'Duplicate variant option combination')
            combinations.add(values)
            max_options = max(max_options, len(options))
        body = '<p>'+html.escape(claims[0]['text'])+'</p>'
        if bullets:
            body += '<ul>'+''.join('<li>'+html.escape(item['text'])+'</li>' for item in bullets)+'</ul>'
        prepared.append((product_id,handle,title,body,variants,claims))
    headers = ['Title','URL handle','Description','Published on online store','Status','SKU']
    for i in range(1,max_options+1):
        headers.extend([f'Option{i} name',f'Option{i} value'])
    headers.append('Price')
    rows, lines = [], ['# Product listing drafts','',f'Store currency: {currency}. New draft products only.','']
    for product_id,handle,title,body,variants,claims in prepared:
        lines.extend([f'## {title}','',claims[0]['text'],''])
        lines.extend('- '+item['text'] for item in claims[1:])
        lines.extend(['',f'Product ID: {product_id}. Handle: {handle}.',''])
        for index,variant in enumerate(variants):
            row = {'Title':title if index==0 else '', 'URL handle':handle,'Description':body if index==0 else '', 'Published on online store':'false' if index==0 else '', 'Status':'draft' if index==0 else '', 'SKU':variant['sku'],'Price':variant['price']}
            for i,option in enumerate(variant['options'] or [{'name':'Title','value':'Default Title'}],1):
                row[f'Option{i} name'] = option['name']
                row[f'Option{i} value'] = option['value']
            rows.append(row)
    files = {'shopify-products.csv':csv_bytes(headers,rows), 'claims.csv':csv_bytes(['Product ID','Claim','Fact ID','Fact','Source','Source excerpt'],ledger), 'listings.md':('\n'.join(lines)+'\n').encode()}
    review = '# Review before import\n\nLocally validated draft export. No live Shopify import has been tested by this script.\n\n'
    review += f'- Confirm target store currency is {currency}.\n- Check each handle is new; keep overwrite-existing-products disabled.\n- Review every claim against its source, including the product title.\n- Review variants, prices and draft/unpublished state in the import preview.\n- Configure inventory, tax, shipping and product media before activation.\n'
    if context['questions']:
        review += '\n## Unanswered questions\n\n'+'\n'.join('- '+q for q in context['questions'])+'\n'
    files['review.md'] = review.encode()
    receipt = {'schema_version':1,'context_sha256':digest,'copy_sha256':hashlib.sha256(copy_bytes).hexdigest(),'product_ids':list(drafts),'variants':len(rows),'currency':currency,'mode':'new-draft-products','live_import_tested':False,'semantic_claim_review':'required','files':{name:hashlib.sha256(data).hexdigest() for name,data in files.items()}}
    files['handoff.json'] = (json.dumps(receipt,indent=2)+'\n').encode()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--context',type=Path,required=True)
    parser.add_argument('--copy',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    try:
        require(not args.out.exists(), 'Output exists; use a new versioned directory')
        files = build(args.context.read_bytes(),args.copy.read_bytes())
        args.out.mkdir(parents=True)
        for name,data in files.items():
            (args.out/name).write_bytes(data)
        print(json.dumps({'output':str(args.out),'files':list(files),'status':'draft; live import untested'}))
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
