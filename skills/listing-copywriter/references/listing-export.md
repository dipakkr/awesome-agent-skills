# Listing copy and Shopify draft export

Write `listing-copy.json` after reading the current context:

```json
{
  "context_sha256": "SHA-256 of the exact store-context.json bytes",
  "products": [{
    "id": "linen-towel",
    "title": "Linen hand towel",
    "summary": {"text": "A hand towel made from 100% linen.", "fact_ids": ["material"]},
    "bullets": [{"text": "100% linen", "fact_ids": ["material"]}]
  }]
}
```

Select any nonempty subset of context products. Every summary and bullet needs at least one confirmed fact belonging to that product. Titles require editorial review against product identity. The script checks references and preserves data; the agent must judge whether the statement follows from the evidence.

The exporter creates new draft products only, using the current Shopify column names documented on 2026-10-28: Title, URL handle, Description, Published on online store, Status, SKU, Option1/2/3 name and value, Price. Do not add inventory, tax, weight, barcode or category defaults without merchant input. Empty optional second/third option columns are omitted when no selected product needs them. A zero-option variant uses Shopify's standard Title / Default Title representation.

[Shopify CSV documentation](https://help.shopify.com/en/manual/products/import-export/using-csv) explains required columns, option dependencies and overwrite behavior. Recheck before changing mappings. The script performs local validation; it cannot detect remote handle collisions or certify a live import. Before import, verify store currency, inspect the draft import preview and leave overwrite-existing-products disabled. After import, review options, price and draft status in the store.

`claims.csv` maps every summary and bullet to source excerpts. `handoff.json` records the context hash, product IDs, draft status and file hashes. `review.md` lists required merchant checks. No network call is made by the exporter.
