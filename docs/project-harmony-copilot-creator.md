# Project Harmony Copilot Creator Integration Design

This design adds a **planning-only** pattern for Project Harmony to ingest structured records, evaluate deterministic rules, and route evidence into an approval workflow. It does not deploy an agent, provision infrastructure, train a model, create an external relationship, or approve an operational, legal, financial, regulatory, safety, grant, privacy, contract, or publication decision.

## External design reference

The public repository [GM-Copilot-App](https://github.com/Cmccombs01/GM-Copilot-App) describes itself as a deterministic ingestion engine for turning complex TTRPG PDFs into verified virtual-tabletop JSON. Its publicly described focus on controlled ingestion, deterministic checks, and audit-oriented outputs is useful as a **design reference** for Project Harmony. This repository does not claim a partnership, endorsement, license, access right, code reuse, or affiliation with GM-Copilot Studios or Caleb McCombs.

Any future reuse of code, branding, prompts, data, or other protected material requires license review and, when necessary, written permission from the relevant rightsholder. Project Harmony should build its implementation from its own requirements, its own data rights, and its own validation evidence.

## Ingestion pattern

Each incoming record should retain the original payload, source identifier, collection time, owner, rights classification, and sensitivity label. A controlled schema validation step should then check required fields, units, field types, and relationships such as site, sample, lot, batch, or transport identifiers. Deterministic rules may flag exceptions, but a failed rule should create a reviewable record rather than silently alter or discard source data.

Validated records should enter an evidence queue. The queue should link the original record, validation result, reviewer, decision status, and downstream output. Public-facing claims must be generated only from the approved-claims register. An ingestion or model output cannot establish remediation efficacy, product safety, carbon accounting, financing, permit status, market demand, or contractual commitment on its own.

## Gemini approval-stage advisory flow

The **Systems Administrator** is the human-in-the-loop. After consulting that role, **Gemini 3.1 Pro** may review coherence, traceability, technical language, multilingual readiness, and evidence completeness. The review output can support an approval recommendation within the Project Harmony workflow. The Systems Administrator records the final decision, any conditions, and exceptions in a decision log.

The decision log must retain the source version, decision scope, evidence links, Systems Administrator consultation, Gemini review output, final status, timestamp, and conditions or exceptions. This advisory flow does not displace an approval that requires a responsible project authority, qualified professional, contract counterparty, regulator, or other legally required reviewer.

## Credential and publication controls

Gemini credentials belong in the Manus managed Gemini connector or a secure secret manager. They must never be committed to source control, pasted into code, placed in static websites, or embedded in client-side applications. A credential exposed in chat, logs, screenshots, or version history must be rotated before use. The configuration validator in this repository rejects credential-like fields in the public planning artifacts.

English remains the controlled source language. Spanish and Dutch translations may follow an approved English version. Simplified Chinese and Japanese should be added only for a defined audience and owner. A qualified translator or relevant subject-matter reviewer must review technical, legal, environmental, laboratory, carbon, financial, and commercialization language before publication. Translations may clarify language, but must not strengthen a claim.

## Micro-pilot planning assumptions

The accompanying micro-pilot configuration uses the user-provided 25% scale factor from a stated 52,000-square-foot, 5-ton-per-hour reference model. It produces a 13,000-square-foot planning footprint, 1.25 tons per hour, 10 tons per eight-hour shift, and 2,500 tons per year on a 50-week, five-shift schedule. These are internal arithmetic assumptions, not engineering approvals, yield guarantees, contract commitments, project financing, grant eligibility, capacity claims, or operating results.

The exact site address is intentionally excluded from this public repository. Any site-specific information must be held in an access-controlled system and shared only after the appropriate review.
