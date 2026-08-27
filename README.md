# Firm Skills Hub

Central skills repository for all Hermes Agent profiles of the firm.

Layout: one folder per profile under `firm/<profile-name>/skills/`, mirroring each
profile's local `~/.hermes/profiles/<name>/skills/` directory.

| Profile | Role |
|---|---|
| developer | IT side — feature coding, Django backend |
| data-engineer | IT side — deterministic ingestion & ETL |
| supervisor | IT side — code reviewer |
| financial-auditor | Audit craft worker |
| financial-auditor-supervisor | Audit reviewer / two-man-rule inspector |
| client-service | Client communication & intake |

## Sync policy
- Direction: profiles -> this hub (one-way, commit + push).
- New or modified skills in any profile get committed here by the sync hook.
- Craft-specific skills are authored into the owning profile only.
