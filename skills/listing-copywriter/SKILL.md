---
name: listing-copywriter
description: Create evidence-grounded ecommerce product listings from a shared store brief or supplied product facts, with variant-preserving draft Shopify CSV exports and a reviewable claim ledger.
metadata:
  author: Claude Directory
  ownership: original-workflow
  version: 0.1.0
---

# Listing Copywriter

Turn approved product facts into useful listing copy and a reviewable catalogue handoff. Accept ordinary-language input. If `store-context.json` already exists, reuse it and ask only for missing facts. Otherwise construct the same compact context from the supplied brief; another skill is not required.

Read [workspace contract](references/workspace.md) for context fields and [listing export](references/listing-export.md) before producing machine-readable output.

## Write from evidence

Select products by their stable IDs. Separate factual statements from positioning ideas. Use only confirmed facts in public copy and attach the supporting fact IDs to each paragraph or bullet. Check that the evidence actually supports the wording; a valid reference ID alone does not establish truth. A material claim does not prove durability, a supplier claim does not prove certification, and a product photo does not establish a hidden feature.

Create a clear title, a useful summary and concise feature bullets. Adapt vocabulary to the user's audience and voice. Preserve units, quantities, care instructions and negative constraints. Avoid generic superlatives and invented customer proof. Keep unknown policy answers out of the listing and in the handoff questions. Reconcile copy against every variant; do not describe one color as if it applied to the entire product.

Save the proposed copy as `listing-copy.json`, including the SHA-256 of the exact context bytes. Review it against the source excerpts before exporting. Pricing, currency and SKU values come from context, never from persuasive copy. If price or currency is missing, return useful text drafts and a missing-input report; the exporter deliberately refuses to create an import file with a silent zero price.

## Export and review

For a Shopify new-product draft, run the bundled standard-library exporter:

```bash
python3 <skill>/scripts/export_listings.py --context <store-context.json> --copy <listing-copy.json> --out <new-directory>
```

It writes `listings.md`, `shopify-products.csv`, `claims.csv`, `handoff.json` and `review.md`. Product status is draft and online-store publication is false. It preserves supplied option combinations and SKUs, escapes HTML and refuses stale context, unknown/proposed claim references, duplicate variants, invalid prices and output overwrites. Read its report before delivery.

This CSV is for creating new draft products in a store with the same currency. Existing-product updates require a current store export and an explicit field-by-field merge; this exporter is not an update tool. Never reuse a handle without checking for a collision in the target store. The output does not configure inventory, taxes, shipping, payments, product images or sales channels. Review those settings in Shopify before activation.

For another platform, deliver the copy and a neutral variant table, then verify its current import schema before claiming an import-ready export. Do not rename Shopify CSV headers and claim compatibility.

## Finish

Deliver actual files, source references and outstanding questions. Describe the result as a locally validated draft CSV until a real Shopify test import has succeeded. Publishing and importing are separate actions that require the user's task authorization. Product image creation is outside this skill; any later creative workflow must use the same approved facts and current variants.

For a local reuse check, use either [contrasting evaluation brief](references/example-briefs.md) without changing this skill. These examples do not establish a live import or customer outcome.
