# Open Redirect in ck.php and lg.php - Revive Adserver

## Metadata
- **Source:** HackerOne
- **Report:** 1081406 | https://hackerone.com/reports/1081406
- **Submitted:** 2021-01-19
- **Reporter:** mbeccati
- **Program:** Revive Adserver
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect
- **CVEs:** CVE-2021-22873
- **Category:** uncategorised

## Summary
Revive Adserver's impression and click tracking scripts (ck.php and lg.php) are vulnerable to open redirects through unvalidated parameters (dest, oadest, ct0). Attackers can craft malicious URLs appearing to come from a trusted domain, redirecting users to phishing or malware sites. This feature was historically accepted in the ad industry but represents a genuine security risk.

## Attack scenario
1. Attacker crafts a malicious URL: example.com/ck.php?dest=evil.com/phishing
2. Attacker embeds this link in an ad, email, or social media, disguising it with legitimate domain
3. Victim clicks the link, seeing trusted 'example.com' in URL bar initially
4. ck.php or lg.php processes the dest/oadest/ct0 parameter without validation
5. User is silently redirected to attacker's malicious site (phishing page, malware, etc.)
6. Victim believes they arrived at legitimate destination due to initial domain trust

## Root cause
Tracking scripts were intentionally designed to support third-party redirect parameters to enable external ad server tracking. Developers failed to implement whitelist validation or domain allowlist controls on redirect destinations, trusting user-supplied parameters implicitly.

## Attacker mindset
An attacker would abuse this as a trust exploitation vector, leveraging the legitimate domain to bypass user skepticism. This is particularly effective against users checking URLs superficially. The attacker gains a 'trusted intermediary' position to deliver phishing, malware, or credential harvesting attacks.

## Defensive takeaways
- Implement strict whitelist validation for all redirect parameters
- Use relative redirects or validate against a list of pre-approved domains
- Require explicit allow-listing of redirect destinations in configuration
- Add user warnings before external redirects from tracking endpoints
- Disable open redirects entirely if not actively used by customers
- Apply same-origin or same-host policies to redirect parameters
- Log and monitor unusual redirect patterns for detection

## Variant hunting
Search for other tracking/analytics endpoints (pixel endpoints, impression trackers, click handlers) accepting redirect parameters. Check for similar patterns in: metrics.php, track.php, pixel.php, action.php, or any param named: redirect, url, next, returnUrl, callback, redir, target, continue

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Spearphishing Link
- T1189 - Drive-by Compromise

## Notes
This vulnerability exploits the historical 'feature not bug' mentality in ad-tech. The legitimate tracking use case complicates remediation - proper fix requires maintaining functionality while enforcing security. The relative obscurity of these endpoints (ck.php, lg.php) may have allowed this to persist undetected. Severity is medium rather than high because it requires user interaction and domain trust exploitation rather than direct system compromise.

## Full report
<details><summary>Expand</summary>

An opportunity for open redirects has been available by design since the
early versions of Revive Adserver's predecessors in the impression and
click tracking scripts to allow third party ad servers to track such
metrics when delivering ads. Historically the display advertising
industry has considered that to be a feature, not a real vulnerability.

The lg.php and ck.php delivery scripts are subject to open redirect via
either dest, oadest and/or ct0 parameters.

## Impact

Users seeing a trustworthy domain could be redirected to a malicious URL without realising.

</details>

---
*Analysed by Claude on 2026-05-24*
