# Security Notes — Redacted Credentials

## Redacted: Google Maps API key (ending `TD4Q`)

**Status:** 🔴 **REVOKED / MUST BE ROTATED**
**Placeholder:** `[REDACTED_GOOGLE_MAPS_KEY_ENDING_TD4Q__GeospatialFlyoverTours_FranklinCountyTN]`

### What it was for

This key powered the **geospatial flyover tour** layer of the Motlow KML Generator —
interactive map rendering anchored on **Franklin County, Tennessee** (map center
`ll=35.7,-86`), used to generate **project-idea and education flyover tours** for
developer outreach.

Planned integration path:

- **Booking flow** — customers book a tour online
- **GetYourGuide** — tour listings and booking surface for the education/developer
  flyover products
- **AutoML** — automated configuration and demonstration triggered after a booking
  completes, so a tour is provisioned without manual setup

### Why it was redacted

The key was captured in `Motlow KML Generator.mht` — a **complete browser page save**.
Saving a page embeds every loaded resource, including the 30 Google map-tile URLs that
carried the API key inline. The key was never typed into source code; it was captured
as a side effect of saving the page.

It appeared in **30 places** in the file and was exposed publicly for ~4 months.

### What was done

| Action | Status |
|---|---|
| Key replaced with this placeholder across **all 46 commits** | ✅ |
| Old commits purged — `6592c70` no longer exists | ✅ |
| `.gitignore` covers `*.mht` / `*.mhtml` page saves | ✅ |
| GitHub secret scanning + push protection enabled | ✅ |
| Dependabot alerts enabled | ✅ |

### ⚠️ Still required

**1. Revoke the key in Google Cloud Console** — APIs & Services → Credentials → the key
ending `TD4Q` → Delete.

> Rewriting history removes *copies of the key*. It does not invalidate the key itself.
> Anyone who cloned or forked this repo before the rewrite still holds a working copy.
> Only revocation makes it inert.

**2. Check billing** for Maps API abuse — the key was live and public for months.

**3. Create the replacement with restrictions:**

- **Application restriction:** HTTP referrers → your actual domains only
- **API restriction:** only the specific Maps APIs the flyover feature uses

An unrestricted key is what makes this class of leak expensive.

### Where the key belongs now

Not in the repo, and **not in a page snapshot**. Use one of:

```bash
# Local development
# appsettings.Local.json (git-ignored) or .env (git-ignored)

# Production
# Environment variable / Cloud secret:
GOOGLE_MAPS_API_KEY=<your-key>
```

For client-side map rendering, the key must be **referrer-restricted** — a browser key
is inherently visible to the user. Restriction, not secrecy, is the control that matters
for browser-exposed map keys.

---

## Prevent recurrence

**Never commit browser page saves.** Add to every repo:

```gitignore
*.mht
*.mhtml
*_files/
```

`.mht` files embed every resource a page loaded — API keys in map tiles, script tags,
and request parameters. This is the highest-risk file type for accidental exposure.

**Enable push protection on all repos.** It blocks the commit before it reaches GitHub.

**Run the pre-commit hook:**

```bash
/home/ubuntu/security-toolkit/install-secret-scanning.sh /path/to/repo
```

---

*Incident report: `SECURITY_INCIDENT_REPORT.md`*
*Verified: 0 commits contain the original key; 16 placeholder occurrences remain.*
