# Unauthorized Music Track Download via Missing Permission Check on /musicstore/download

## Metadata
- **Source:** HackerOne
- **Report:** 43770 | https://hackerone.com/reports/43770
- **Submitted:** 2015-01-14
- **Reporter:** wkcaj
- **Program:** Vimeo
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Missing Authorization, Broken Access Control, Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The /musicstore/download endpoint fails to verify that the user has purchased or has rights to download a track. Attackers can directly access the download endpoint with a track_id from non-free tracks without payment, bypassing the checkout process. The endpoint redirects to Amazon S3 to serve the file regardless of payment status.

## Attack scenario
1. Attacker logs into Vimeo and navigates to the Music Store
2. Attacker identifies a paid track and clicks 'Add to Cart' to observe the POST request to /cart/music
3. Attacker extracts the track_id parameter from the POST request
4. Attacker crafts a GET request to /musicstore/download with the track_id and license_id=4 parameters
5. The server redirects to Amazon S3 without verifying purchase/payment status
6. Attacker downloads the copyrighted music track without payment

## Root cause
The /musicstore/download endpoint performs no authorization checks before issuing a redirect to the S3 download URL. The application likely relies on frontend controls (hiding download links for unpaid tracks) rather than server-side authorization validation. The license_id parameter is not properly validated against the user's actual purchases.

## Attacker mindset
An opportunistic threat actor seeking to obtain paid digital content without payment. Low technical skill required—simple parameter manipulation and URL crafting. Motivation is financial gain through content piracy, exploiting the gap between frontend restrictions and backend authorization.

## Defensive takeaways
- Always perform server-side authorization checks before granting access to protected resources; never rely solely on frontend UI controls
- Validate that the requesting user has a valid, paid license/purchase for the requested track before issuing download URLs
- Implement proper session-based entitlement checks and maintain audit logs of all download access
- Use cryptographic tokens or signed URLs that embed purchase verification and are validated server-side
- Implement rate limiting and anomaly detection on the /musicstore/download endpoint
- Apply the principle of least privilege—verify both user identity and resource entitlement before redirecting to content delivery
- Consider time-limited, single-use download tokens instead of direct track_id parameters

## Variant hunting
Check for similar IDOR vulnerabilities on other endpoints handling digital assets (e.g., /movies/download, /ebooks/download, /software/download)
Test if license_id values other than 4 can be used to access different license tiers without payment
Attempt to download tracks with expired or revoked licenses to verify real-time entitlement validation
Test whether modifying the user_id or uid parameter in the download request allows downloading tracks purchased by other users
Check if the S3 redirect URLs contain predictable patterns that could allow direct enumeration/access without the download endpoint
Test other HTTP methods (POST, PUT, DELETE) on the /musicstore/download endpoint

## MITRE ATT&CK
- T1190
- T1566

## Notes
The reporter responsibly chose not to complete the download without payment verification, demonstrating ethical disclosure practices. The vulnerability is particularly concerning because it directly impacts revenue for content creators. The use of Amazon S3 redirects may have created a false sense of security, but the authorization logic must be in the application layer, not reliant on S3 access controls. This is a classic example of a broken access control vulnerability (OWASP A01:2021).

## Full report
<details><summary>Expand</summary>

Hello,

I'm not sure how serious this is to be honest. If you're downloading tracks without paying, then I'm sure you could find a copy somewhere on the internet anyway. But I guess it's still an issue.

When browsing the Music Store (https://vimeo.com/musicstore), some tracks are free. To download these, a `GET` request is sent to `/musicstore/download`, with a query string of `track_id=[track_id]&license_id=4`.

For non-free tracks, the link is replaced with an Add to Cart icon, and you're expected to go through the checkout procedure. This is done by a `POST` request to `/cart/music`with a body of `action=add&license_id=2&license_name=Personal&price=1.99&track_id=110947&track_title=Remind%2BMe&uid=110947_2&&&token=[token]`.

Copying the `track_id` from the Add to Cart request and transplanting it into the `/musicstore/download` successfully redirects you to Amazon S3 to download the track, despite you not having paid for it.

Note: I submitted the `GET` request to `/musicstore/download`, but didn't follow the 302 redirect to S3 to download the track since I didn't pay for it. Because of this I can't 100% verify that the resulting file is the track, but judging by the URL it looks like it is.

### Proof-of-Concept
**Accounts Needed**
* User #1 - Standard Vimeo user

**Steps**
1. Login, and browse to https://vimeo.com/musicstore
2. Find a **non-free** track, and click the Add to Cart icon
3. Inside the `POST` request to `/cart/music` copy the `track_id`
4. Browse to the following URL, replacing `[track_id]` with the one from step 3. You should be redirected to S3 to download the track (without paying): `https://vimeo.com/musicstore/download?track_id=[track_id]&license_id=4`

If you need anymore info just shout,
Cheers,
Jack

</details>

---
*Analysed by Claude on 2026-05-24*
