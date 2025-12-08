# Available Tag Filters

These are the canonical tags used by the scrapers and exposed to the frontend for tag-based filtering.

- software
- engineering
- engineer
- developer
- tech
- it
- product
- operations
- manager
- senior
- junior
- management
- consulting
- finance
- financial
- accounting
- legal
- hr
- recruiting
- admin
- intern
- internship
- sales
- marketing
- growth
- customer-support
- support
- writing
- copywriting
- content
- design
- creative
- ui-ux
- media
- video
- editor
- analytics
- qa
- security
- health
- healthcare
- medical
- education
- teaching
- trainer
- architect
- logistics
- supply-chain
- manufacturing
- hardware

Notes:
- The frontend extracts the available tags from the `tags` property of each job object returned by the `/get_jobs` API. Ensure that `Posting.to_dict()` includes `tags` so the UI can show the filters (this repository already updates that behavior).
- `TAG_FILTERS` is defined in `Backend/Helper_Scripts/parsing.py` as a canonical list that can be used by tooling if you want to present a fixed whitelist of filters.