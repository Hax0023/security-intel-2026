# Improper Access Control in Account Import Flow Allows Cross-Tenant ActionText Reference Resolution and Data Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 3543475 | https://hackerone.com/reports/3543475
- **Submitted:** 2026-02-07
- **Reporter:** xavlimsg
- **Program:** fizzy.do
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Improper Access Control / Authorization, Cross-Tenant Data Exposure, Insecure Direct Object References (IDOR), Data Import/Export Vulnerability
- **CVEs:** None
- **Category:** uncategorised

## Summary
The account import flow in fizzy.do fails to validate tenant ownership when processing ActionText attachment references from user-uploaded content. An attacker can craft malicious ZIP imports containing GIDs that reference victim-account records, causing the system to resolve and persist signed references (SGIDs) to cross-tenant data without authorization checks. This enables unauthorized data reference and potential disclosure of victim attachable content in the attacker's account context.

## Attack scenario
1. Attacker creates a malicious ZIP file for account import containing ActionText HTML with attacker-crafted GID values pointing to victim-tenant record IDs
2. Attacker uploads the ZIP through the normal account import flow (`imports_controller.rb:38`), triggering `Account::Import#perform`
3. The import processor calls `ActionTextRichTextRecordSet#import_batch`, which processes ActionText attachments and invokes `convert_gids_to_sgids` on attacker-controlled GID strings
4. The vulnerable `convert_gids_to_sgids` method resolves GIDs globally without checking if the resolved record belongs to the importing account, successfully finding victim-owned records
5. The method creates and persists an SGID (signed reference) to the victim record and stores it in the attacker's imported rich text
6. Victim's attachable data is now referenced and potentially rendered in the attacker's account context, causing unauthorized cross-tenant data access and disclosure

## Root cause
Missing tenant ownership validation in `app/models/account/data_transfer/action_text_rich_text_record_set.rb` method `convert_gids_to_sgids` (lines 83-89). The export path includes a check (`record&.account_id == account.id`) at line 69, but the import path completely omits this authorization check when resolving GID values to SGID references. The code trusts attacker-supplied GID strings and resolves them globally without verifying the resolved record belongs to the importing account.

## Attacker mindset
An attacker with account access seeks to escalate privileges by accessing cross-tenant data. They recognize that the import mechanism processes user-supplied rich text content and leverage the missing authorization check to craft GIDs referencing victim records. By uploading a malicious import, they can establish persistent unauthorized references to victim data without triggering alerts, enabling both discovery of victim record structures and potential information disclosure.

## Defensive takeaways
- Always validate tenant/ownership context before resolving or creating references to persistent objects, especially in import/export flows
- Apply consistent authorization checks across mirror code paths (import and export should have equivalent security controls)
- Treat all user-supplied identifiers (including GIDs from ZIP imports) as untrusted and validate against current tenant context before dereferencing
- Implement defense-in-depth: verify ownership at multiple layers (resolution, persistence, and access time)
- Add integration tests that specifically verify cross-tenant access attempts are blocked during import operations
- Audit all data transfer/import flows for similar missing tenant checks, particularly in rich text, attachment, and reference resolution code

## Variant hunting
Search codebase for: (1) Other import/export paths processing user-supplied identifiers without tenant checks; (2) Any `convert_*_to_*gid` or similar reference-minting methods lacking account_id validation; (3) Places where `GlobalID.find` or similar global resolution occurs within account-scoped operations; (4) Rich text or attachment processing in multi-tenant contexts missing ownership verification; (5) Any discrepancy between export-time and import-time authorization logic in the same file

## MITRE ATT&CK
- T1190
- T1199
- T1526

## Notes
The reporter provided two reproducible PoC paths: a standalone integration test and a full Rails environment demo, both confirming the vulnerability in production code. The presence of correct authorization logic in the export path (line 69) makes this a clear oversight rather than design choice. The SGID (signed global ID) mechanism itself is not the issue—the problem is minting SGIDs without first validating the resolved record's ownership. This is a multi-tenant SaaS vulnerability with significant business impact, allowing attackers to discover and reference arbitrary victim data through a normal user feature.

## Full report
<details><summary>Expand</summary>

## Description

The account import flow processes ActionText attachment HTML from user-uploaded ZIP content.

In `app/models/account/data_transfer/action_text_rich_text_record_set.rb`, import-time method `convert_gids_to_sgids` converts attacker-controlled `gid` values into persisted `sgid` values by resolving the target record globally:

- `app/models/account/data_transfer/action_text_rich_text_record_set.rb:83`
- `app/models/account/data_transfer/action_text_rich_text_record_set.rb:87`
- `app/models/account/data_transfer/action_text_rich_text_record_set.rb:88`
- `app/models/account/data_transfer/action_text_rich_text_record_set.rb:89`

The import path has no tenant ownership check before minting the signed reference.

Reachable import path from normal upload flow:

- `app/controllers/account/imports_controller.rb:38`
- `app/models/account/import.rb:37`
- `app/models/account/import.rb:39`

For comparison, export path has an account check (`record&.account_id == account.id`) in the same file at `app/models/account/data_transfer/action_text_rich_text_record_set.rb:69`.

## Reproduction Path A (Fastest for triage, deterministic)

This path is self-contained and exercises the real vulnerable import code path (`import_batch`) without requiring full web flow setup.

### Prerequisites

- Ruby and Bundler installed
- Repo cloned

### Steps

1. Enter repo:

```bash
cd /path/to/fizzy
```

2. Install/check dependencies:

```bash
bundle check || bundle install
```

3. Run standalone integration PoC:

```bash
bundle exec ruby security-poc/integration_test_standalone.rb
```

4. Expected success signals in output:

- `RESULT: IMPACT_CONFIRMED=true`
- `imported.account_id = <attacker_account_id>`
- `resolved_account_id = <victim_account_id>` (different tenant)
- `attachable_text = @alice_secret`

### Why this is valid

This script loads and executes the real vulnerable file:

- `app/models/account/data_transfer/action_text_rich_text_record_set.rb`

And runs:

- `Account::DataTransfer::ActionTextRichTextRecordSet#import_batch`

So the exploit condition is validated directly against production logic.

## Reproduction Path B (Full product-equivalent import flow)

This path uses the Rails environment and import conversion path end-to-end.

### Steps

1. Enter repo:

```bash
cd /path/to/fizzy
```

2. Install/check dependencies:

```bash
bundle check || bundle install
```

3. Run full import impact demo:

```bash
DISABLE_BOOTSNAP=1 RAILS_ENV=development \
bundle exec rails runner security-poc/demo_import_cross_account_impact.rb
```

4. Expected success signals:

- `cross_account_reference=true`
- `IMPACT_CONFIRMED=true`
- `imported_rich_text_account_id=<attacker_account_id>`
- `resolved_account_id=<victim_account_id>`
- `leaked_attachable_text=@alice`

### Note

In slower environments, Rails boot may take a few minutes before script output appears.

## Evidence from local execution

Observed in local runs:

- Path A (`integration_test_standalone.rb`): `RESULT: IMPACT_CONFIRMED=true`
- Path B (`demo_import_cross_account_impact.rb`): `IMPACT_CONFIRMED=true`

Both runs showed attacker-owned imported rich text resolving a victim-owned attachable record.

## Supporting files

- `security-poc/integration_test_standalone.rb`
- `security-poc/demo_import_cross_account_impact.rb`
- `security-poc/patch_action_text_gid.py`

## Suggested remediation

In `convert_gids_to_sgids`, only mint `sgid` when resolved record belongs to importing account:

- Resolve record safely (handle not found)
- Require `record.respond_to?(:account_id) && record.account_id == account.id`
- Drop or ignore cross-account references

## Impact

## Impact

- Cross-tenant unauthorized data reference in imported rich text.
- Victim-account attachable data is resolved/rendered in attacker-account context.
- Persisted unauthorized reference (`sgid`) remains stored until removed.

</details>

---
*Analysed by Claude on 2026-05-24*
