# DoS through cache poisoning using invalid HTTP parameters

## Metadata
- **Source:** HackerOne
- **Report:** 326639 | https://hackerone.com/reports/326639
- **Submitted:** 2018-03-16
- **Reporter:** irvinlim
- **Program:** Greenhouse
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Cache Poisoning, Denial of Service, HTTP Parameter Pollution, Insufficient Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Greenhouse job board endpoint fails to validate array-format HTTP parameters and instead reflects them directly into JavaScript configuration objects. These responses are cached by CloudFront and application-layer caches, allowing attackers to poison the cache with malformed URIs that prevent job boards and application iframes from loading on client websites.

## Attack scenario
1. Attacker crafts malicious URL with array-format parameters: ?for[]=twitter&for[]=&for[]=... (repeated empty parameters)
2. Attacker sends request to vulnerable endpoint https://boards.greenhouse.io/embed/job_board/js?for[]=...
3. Server fails to validate array parameters and reflects them into Grnhse.Settings object with URL-encoded brackets (%5B%5D)
4. Response is cached by CloudFront CDN and application-layer caches
5. Legitimate requests to ?for=twitter now receive cached poisoned response with malformed boardURI and applicationURI
6. Client websites embedding job board iframes fail to load, resulting in DoS lasting 5 minutes to 1+ hour depending on cache TTL

## Root cause
The application lacks proper input validation for HTTP parameters, particularly array-format parameters. It directly reflects unsanitized URL parameters into JavaScript objects that are then cached. The server fails to normalize or reject invalid parameter formats before caching responses, and there is insufficient cache validation or key differentiation between valid and invalid parameter formats.

## Attacker mindset
An attacker with knowledge of web caching mechanisms could exploit this to temporarily disrupt job board functionality across multiple client websites simultaneously. The attack requires low effort (simple URL crafting) but uncertain reliability due to unknown cache architecture. The attacker could use this to cause reputational damage or force attention to their security research.

## Defensive takeaways
- Implement strict input validation that rejects invalid parameter formats (e.g., array notation where not expected) rather than reflecting them
- Use cache-busting techniques and set appropriate Cache-Control headers with short TTLs or vary-based cache key generation
- Normalize all incoming parameters and validate against expected types before caching responses
- Consider using cache keys that include parameter validation state or implement cache invalidation mechanisms
- Monitor for suspicious parameter patterns and invalid cache hits indicating poisoning attempts
- Document and test cache behavior for edge cases and invalid inputs across all caching layers (CDN and application)
- Implement WAF rules to detect and block parameter pollution and malformed array parameters at the CDN level

## Variant hunting
Look for similar reflection vulnerabilities in other Greenhouse endpoints accepting parameters. Test other query parameters on the job_board/js endpoint with array notation. Check if other Greenhouse subdomains or API endpoints have similar caching behavior without input validation. Test HTTP parameter pollution variants (duplicate parameters, semicolon delimiters, etc.) on job application endpoints.

## MITRE ATT&CK
- T1190
- T1499

## Notes
This is a thoughtfully reported first vulnerability submission. The attacker acknowledged uncertainty about cache architecture and responsibly stopped testing rather than attempting to cause extended damage. The report references a related issue (298265) indicating a pattern of similar vulnerabilities. The evidence of CloudFront involvement (IP address correlation) strengthens the cache poisoning diagnosis. Real-world impact verified on Airbnb's job application page. The vulnerability likely affects all Greenhouse customers using the affected endpoint, making this a high-impact supply chain issue despite medium severity rating.

## Full report
<details><summary>Expand</summary>

I was taking a look into a related report (https://hackerone.com/reports/298265) and I discovered that the https://boards.greenhouse.io/embed/job_board/js?for= endpoint doesn't throw errors when I try to pass in an array of `for` parameters like this:

```
https://boards.greenhouse.io/embed/job_board/js?for[]=twitter&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=&for[]=
```

Instead, in the resultant JS, we can see that the HTTP parameters are escaped and injected into the `Grnhse.Settings` object:

```js
Grnhse.Settings = {
  targetDomain:   'https://boards.greenhouse.io',
  scrollOnLoad:   true,
  autoLoad:       true,
  boardURI:       'https://boards.greenhouse.io/embed/job_board?for%5B%5D=twitter&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=',
  applicationURI: 'https://boards.greenhouse.io/embed/job_app?for%5B%5D=twitter&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=&amp;for%5B%5D=',
  baseURI:        '',
  iFrameWidth:    650
};
```

When fetching the actual correct endpoint (https://boards.greenhouse.io/embed/job_board/js?for=twitter), we see that the result for `twitter` is cached, returning the same corrupted URIs in the JS file. From my tests, it seems that these endpoints are cached for an unknown amount of time, with some staying in the cache for only a few minutes while others may be an hour or longer.

I also found out that the particular endpoint is on CloudFront by observing one of the IP addresses which served the file (35.164.91.227) and corroborating it with the IP range list published by AWS (https://ip-ranges.amazonaws.com/ip-ranges.json). However, fetching from different edge servers seems to result in the same mutated file being fetched at the correct endpoint (https://boards.greenhouse.io/embed/job_board/js?for=twitter). I conclude that there is a second layer of caching somewhere on the application layer.

The impact of corrupting the `boardURI` and `applicationURI` values is that the `job_app` or `job_board` iframes would fail to load in the client's website since the URI is incorrect, resulting in a denial of service for the client. One example is that Airbnb's job application page shows a Greenhouse.io error page (see attached images), which I managed to replicate it twice and lasted for about 20 minutes and less than 5 minutes respectively.

I tried to investigate if I could reliably replicate this PoC by waiting for cache to expire, as well as across several domains, but failed to find anything conclusive without knowledge of the underlying network architecture. Additionally, I am not sure if what is going on at play is due to a cache, and seeing that some IDs take quite a while to recover back to its normal state, I will stop trying to replicate the attack for now.

P.S. This is my first report, so do let me know if I could be of more help!

## Impact

If the attacker has more patience and knowledge about the underlying architecture, the attacker could attempt to poison the cache reliably, resulting in an extended denial of service of Greenhouse job boards/application iframes in client sites.

</details>

---
*Analysed by Claude on 2026-05-24*
