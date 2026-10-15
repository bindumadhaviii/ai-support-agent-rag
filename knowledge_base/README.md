# Knowledge Base — Ridgeline Outfitters

These documents are the store's customer-facing help content. The support agent
retrieves passages from them (RAG) and must cite the document it relied on.

Ridgeline Outfitters is a fictional online store selling outdoor gear. Its product
catalog and orders match the seed data in `backend/app/db/seed.py`.

## Structure

| Folder | Contents |
|---|---|
| `policies/` | Returns, refunds, exchanges, warranty, cancellations, final sale |
| `shipping/` | Shipping options, tracking, international, lost packages, address changes |
| `products/` | Product specs, care, fit, and size charts |
| `account/` | Sign-in, payments, gift cards, privacy and security |
| `help/` | Contact options, rewards program, general FAQ |

## Document format

Every document starts with front matter used for citations and filtering:

```yaml
---
id: returns-policy          # stable ID used in citations
title: Return Policy
category: policies
last_updated: 2026-09-15
---
```

## Rules for editing

- **One source of truth per fact.** If a number changes (for example the return
  window), update every document that mentions it and re-run the evals.
- **Customer-facing only.** Internal rules (such as the exact approval logic for
  refunds) live in backend code, not here.
- Keep facts consistent with the backend: the 30-day return window and the
  $200 refund review threshold are also enforced in code.
