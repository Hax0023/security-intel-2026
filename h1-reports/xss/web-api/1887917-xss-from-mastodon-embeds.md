# XSS from Mastodon Embeds in IRCCloud Web Client

## Metadata
- **Source:** HackerOne
- **Report:** 1887917 | https://hackerone.com/reports/1887917
- **Submitted:** 2023-02-27
- **Reporter:** lotsofloops
- **Program:** IRCCloud
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, Unsafe iframe Source Handling
- **CVEs:** None
- **Category:** web-api

## Summary
IRCCloud's web client automatically embeds Mastodon toots when URLs are detected, but fails to validate the embed URL before creating an iframe. An attacker running a malicious Mastodon server can inject a javascript: URL that executes arbitrary code in the context of the web client, allowing session token theft and user impersonation.

## Attack scenario
1. Attacker sets up a malicious Mastodon instance at a controlled domain (e.g., sm4.ca)
2. Attacker crafts a URL pointing to a fake toot (e.g., https://sm4.ca/@a/123456789012345678)
3. Attacker sends this link in a message to an IRCCloud channel with multiple users
4. IRCCloud web client fetches status data from the attacker's /api/v1/statuses/ endpoint
5. Attacker's server responds with a malicious JSON payload containing a javascript: URL in the 'url' field
6. Client creates an iframe with javascript: URL as src, executing the attacker's payload with access to parent context and session cookies

## Root cause
The IRCCloud web client extracts the 'url' field from Mastodon API responses without validating that it's a safe URL scheme (http/https). It directly uses this untrusted value as an iframe src attribute, allowing javascript: protocol URLs to execute. The client assumes data from any Mastodon-like server is trustworthy but fails to account for attacker-controlled servers.

## Attacker mindset
An attacker seeks to compromise IRCCloud users' accounts by exploiting the implicit trust placed in Mastodon embeds. By controlling a Mastodon server, they can inject malicious payloads that execute in the victim's browser context, stealing authentication tokens. This is especially attractive for mass compromise in shared channels.

## Defensive takeaways
- Validate all URLs before using them as iframe src attributes; only allow http/https schemes
- Implement Content Security Policy (CSP) to restrict iframe sources and prevent javascript: execution
- Sanitize or validate all data fetched from third-party APIs before rendering in iframes
- Consider disabling social media embeds by default rather than opt-out, especially when they leak IP addresses
- Use sandboxed iframes with minimal permissions rather than full document context access
- Implement URL scheme whitelisting at the point where iframe src is set
- Consider using a dedicated embed service or proxy that validates and re-serves embed content

## Variant hunting
Check for similar embed handling in other social media integrations (Twitter, Bluesky, etc.)
Audit all iframe creation points in the codebase for unsafe src attribute assignment
Test other API response fields that might be used as URLs (account.url, etc.)
Look for similar patterns where third-party API data is directly rendered without validation
Check if other IRC clients or chat applications have similar embed features vulnerable to this pattern
Test whether data: URLs or other protocol handlers can bypass validation

## MITRE ATT&CK
- T1190
- T1566
- T1566.002
- T1598

## Notes
The POC is particularly clever in that it exploits the assumption that any Mastodon server will return valid data. The attacker doesn't need to compromise an existing server—they can run their own. The /embed path appending is a detail that necessitates the // comment at the end of the payload. This vulnerability has batch compromise potential in shared channels, making it especially dangerous. The reporter also notes the secondary issue of IP leakage from embed fetches, which should be addressed separately.

## Full report
<details><summary>Expand</summary>

By default, the IRCCloud web client embeds Mastodon toots when a link to one is sent. Anyone can run a Mastodon server, and so the server from which toot data is fetched might be malicious. It is possible for an attacker to cause a web client user to execute arbitrary JavaScript in the context of the IRCCloud web client by tricking the web client into embedding a `javascript:` URL.

**POC**:
1. Ensure "Embed social media links" is enabled in settings under "Chat & embeds" (I think this is on by default)
2. Send a message with a link to https://sm4.ca/@a/123456789012345678 (the link itself 404s but IRCCloud only tries to use Mastodon API so it doesn't matter)
3. Wait a few seconds for the embed to load
4. Look at your session cookie

When the web client sees what looks like a toot URL, it tries to get canonical toot URL by making a query to `[domain]/api/v1/statuses/[toot ID]`. Here is what I serve at `https://sm4.ca/api/v1/statuses/123456789012345678`:

```json
{
  "account": {
    "url": "https://sm4.ca/@a"
  },
  "url": "javascript:top.document.body.innerHTML = \"hi your cookie is \" + document.cookie;//"
}
```

(`.account.url` is only present because the web client ensures it matches the original link)

The web client creates an `iframe` using `.url` as the src, which in this case is a `javascript:` URL. The specified script runs in a seperate document that has access to its parent, and can access anything the parent can. The `//` is needed at the end since the web client appends `/embed` to the embed URL.

(also apart from this particular issue, I don't think Mastodon embeds should be enabled unless "Embed 3rd party image and video links" is enabled since even when the Mastodon server isn't malicious your IP address is still leaked to an arbitrary server)

## Impact

An attacker who can send a message to an web-client-using IRCCloud user can obtain their session token and act as them. By sending a message with a malicious URL to a large channel an attacker could compromise many users at once.

</details>

---
*Analysed by Claude on 2026-05-12*
