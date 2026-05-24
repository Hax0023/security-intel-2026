# inconsistently Rejection Logic in file:// URLs with Authority

## Metadata
- **Source:** HackerOne
- **Report:** 3494098 | https://hackerone.com/reports/3494098
- **Submitted:** 2026-01-08
- **Reporter:** unknowperson0212
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Path Traversal
- **CVEs:** None
- **Category:** uncategorised

## Summary
curl's `file://`  protocol handler inconsistently applies path sanitization. in reject `file://../` as Bad File:// URL" but allows the same traversal when an authority/host (e.g.,`localhost`) is present (`file://localhost/../`). this inconsistency misleads developers who rely on the `bad file:// URL` error for sandbox enforcement.

##Root Cause:
The `Bad File:// URL` check only triggers for "relat

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

curl's `file://`  protocol handler inconsistently applies path sanitization. in reject `file://../` as Bad File:// URL" but allows the same traversal when an authority/host (e.g.,`localhost`) is present (`file://localhost/../`). this inconsistency misleads developers who rely on the `bad file:// URL` error for sandbox enforcement.

##Root Cause:
The `Bad File:// URL` check only triggers for "relative" URLs (no Host). Adding a valid/invalid host bypasses this safety check, allowing path traversal to proceed.

##Step to Reproduce:

1. `echo "SECRET" > /tmp/secret.txt`
2. `curl file:///tmp/secret.txt` -> Works (Expected).
3. `curl file://../../../../tmp/secret.txt` -> Blocked ("Bad file://URL").
4. `curl file://localhost/../../../tmp/secret.txt` -> Works (Bypass The Check in #3)
{F5200477}

While `file://` is not designed as a security sandbox, the existence of the specific `Bad file:// URL` rejection creates a **False security guarantee**. Developers implicitly trust this error to block traversal. Bypassing this specific control breaks that trust, leading to insecure sandboxing logic in dependent application.

## Impact

Bypass off application-level sandboxing that depends on URL parsing validation

</details>

---
*Analysed by Claude on 2026-05-24*
