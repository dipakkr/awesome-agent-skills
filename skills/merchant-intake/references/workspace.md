# Store context contract version 1

The agent writes this JSON from the user's conversation. Users do not need to edit it. Use explicit null values for unknown scalar fields and empty arrays for missing lists. Keep source excerpts short, factual and limited to the task; no credentials, customer records or confidential cost data.

```json
{
  "schema_version": 1,
  "business": {
    "name": "Example brand",
    "platform": "Shopify",
    "country": "IN",
    "currency": "INR",
    "stage": "prelaunch",
    "audience": "People organizing a small home",
    "voice": "Practical and warm"
  },
  "sources": [{"id": "founder-brief", "label": "Founder supplied brief", "excerpt": "Exact relevant supplied facts"}],
  "products": [{
    "id": "linen-towel",
    "handle": "linen-towel",
    "title": "Linen hand towel",
    "facts": [{"id": "material", "text": "100% linen", "source": "founder-brief", "status": "confirmed"}],
    "variants": [{"sku": "TOWEL-NAT", "options": [{"name": "Color", "value": "Natural"}], "price": "1200.00", "source": "founder-brief"}]
  }],
  "questions": ["Confirm shipping charges before launch"]
}
```

- `business` fields are strings or null. Country uses a supplied country code, currency a supplied three-letter currency code. Platform names are not evidence of a connected account.
- Sources have unique IDs. Confirmed facts and variants must reference an existing source. Preserve the evidence excerpt; do not fabricate it to justify drafted copy.
- Product IDs, handles, titles and facts remain stable across tasks. Handles use lowercase letters, digits and hyphens. Do not auto-change an existing handle when editing a title.
- Fact IDs are unique within a product. Status is `confirmed`, `proposed` or `unknown`. The latter two never support public claims.
- Each variant has a unique SKU across the workspace. Preserve all supplied option combinations. Use zero options for a genuinely single-variant product, or one to three named options with the same names/order across all variants of that product.
- Prices are nonnegative decimal strings with at most two decimal places for this pilot, or null when unknown. A supplied zero is allowed; an absent price is never converted to zero. More precise currency rules require a different exporter.
- The JSON contains listing context only. Keep shipping/returns policies in a separate source-grounded policy brief when requested; this v1 listing export does not apply policies automatically.
- `questions` is a list of unresolved questions, not a list of invented answers. A stage with no product facts is valid for a planning brief but cannot yield an import file yet.

Copy the user's original brief alongside the structured context for review when permitted. The context hash in downstream artifacts detects changes, not semantic truth. Recheck sources whenever facts are updated.
