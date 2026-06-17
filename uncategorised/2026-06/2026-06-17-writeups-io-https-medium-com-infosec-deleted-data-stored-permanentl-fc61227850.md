# Deleted Data Stored Permanently on Instagram/Facebook Data Backup

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Facebook Bug Bounty Program
- **Bounty:** Not awarded (closed as informative)
- **Severity:** Medium
- **Vuln types:** Improper Data Deletion, Data Retention Policy Violation, Privacy Disclosure, Insufficient Data Sanitization
- **Category:** uncategorised
- **Writeup:** https://medium.com/infosec/deleted-data-stored-permanently-on-instagram-facebook-bug-bounty-2020-26074c229955

## Summary
A researcher discovered that deleted photos and conversations from 5-6 years ago were still accessible in Instagram's data backup export feature. The backup included photos deleted within minutes of upload and conversations deleted weeks prior, contradicting user expectations of permanent deletion. Facebook's response indicated deleted content persists in CDN for up to 90 days, but the researcher found evidence of much older deleted data still recoverable.

## Attack scenario (step by step)
1. Attacker requests personal data backup from Instagram settings
2. Attacker downloads and extracts the provided backup ZIP file
3. Attacker reviews backup contents and discovers deleted photos from years prior
4. Attacker extracts direct CDN URLs from conversation JSON files containing deleted attachments
5. Attacker validates that URLs with valid signatures still serve deleted photos/videos from 4-6 years ago
6. Attacker demonstrates privacy violation by accessing content user believed was permanently deleted

## Root cause
Instagram/Facebook's data export/backup feature includes deleted content that persists on CDN servers beyond stated retention policies. The backup generation process does not filter or exclude deleted items, and CDN signature URLs remain valid for deleted media far longer than the documented 90-day retention window.

## Attacker mindset
Opportunistic researcher performing legitimate account maintenance who stumbled upon the issue. Motivated by privacy concerns rather than malicious intent, attempting to clarify the disconnect between user-facing deletion and backend data retention policies.

## Defensive takeaways
- Implement data filtering in export/backup features to exclude deleted content older than retention policy window
- Synchronize CDN content deletion timelines with user-facing deletion operations and documented policies
- Validate that signature-based URLs expire consistently with content deletion timeframes
- Conduct periodic audits of backup export contents against deletion logs
- Document and enforce actual data retention timelines that match user-facing privacy policies
- Implement content deletion verification before including items in user exports
- Consider default exclusion of deleted items from backups with optional recovery for recent deletions only

## Variant hunting
['Check other data export features (Facebook photos, messenger exports, download your data) for similar deleted content leakage', 'Test whether deleted private messages appear in conversation exports beyond stated retention periods', 'Verify if deleted stories, temporary content, or disappearing messages are included in backups', 'Examine CDN signature URL generation and expiration mechanisms across Facebook properties', 'Test backup exports from accounts with various deletion patterns and ages', 'Check if deleted business account data appears in exports for company accounts', 'Investigate whether archived vs deleted items are properly distinguished in backup exports']

## MITRE ATT&CK
- T1530 - Data from Cloud Storage
- T1213 - Data from Information Repositories
- T1005 - Data from Local System
- T1123 - Audio Capture
- T1113 - Screen Capture

## Notes
The bug bounty was closed as 'informative' rather than accepted. Facebook's response emphasized policy (90-day deletion window) rather than addressing the discrepancy between policy and observed behavior (5-6 year old deleted content). The researcher demonstrated legitimate privacy concern but the organization did not treat data retention exceeding policy as a security issue. This represents a potential gap between documented privacy policies and actual technical implementation, which could have implications for regulatory compliance (GDPR, CCPA).

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
