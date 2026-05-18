# Core principle: business terminology

Names must align with the terminology that actual people in the organization use. Never assume — always confirm with the user or infer from existing patterns.

## Why this matters

The semantic model is an authoritative source of truth for terminology. If users in the org call it "Turnover", don't model it as "Net Sales" or "Revenue" — those are different concepts in different orgs.

## Implications

- **The default naming rules in `naming-rules.md` are starting points, not law.** Override them when the user's org has established conventions.
- **Ask before mass-renaming.** A measure called `Turnover` in a SAP-aligned org is correct; renaming to `Revenue` is wrong.
- **Multi-language orgs**: pick the primary language (usually English) and use cultures (`../../model/add/culture.md`) for translations.

## Questions to ask first

Per `audit-workflow.md` Phase 2:

1. What terminology does your org use for key metrics? (Revenue, Turnover, Sales, Gross Sales)
2. Do you have documented naming conventions already?
3. How do you refer to prior periods? (1YP, PY, Prior Year, Last Year)
4. How do you express units in measure names? ((%), (Value), (Quantity))
5. Are there downstream reports that need rebinding after renaming?

## Anti-pattern: rename without context

Don't run the full rule set against a model without first understanding the business. You'll produce technically-clean names that don't match what users actually say.
