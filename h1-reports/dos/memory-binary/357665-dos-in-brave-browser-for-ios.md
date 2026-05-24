# Denial of Service in Brave Browser for iOS via Object Tag MIME Type

## Metadata
- **Source:** HackerOne
- **Report:** 357665 | https://hackerone.com/reports/357665
- **Submitted:** 2018-05-26
- **Reporter:** metnew
- **Program:** Brave Software
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Denial of Service, Crash/Exception, Resource Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
Brave browser for iOS crashes when processing an HTML object tag with specific MIME type values (text/html, application/json, application/pdf). The vulnerability allows an attacker to trigger an immediate browser crash during page load, affecting the Brave iOS application which forks from Mozilla Firefox.

## Attack scenario
1. Attacker crafts malicious HTML page containing an object element with type='text/html'
2. Attacker hosts page on web server or embeds in advertisement/email
3. Victim visits malicious page using Brave browser on iOS device
4. Browser attempts to process the object tag during page rendering
5. Unhandled exception occurs in MIME type handler, causing browser crash
6. User's browser becomes unresponsive and must close tab to recover

## Root cause
Improper handling of object tag MIME type attributes in Brave's iOS fork. Certain valid MIME types (text/html, application/json, application/pdf) trigger an unhandled exception during resource initialization, whereas Firefox properly sanitizes or handles these cases.

## Attacker mindset
Opportunistic malware distributor seeking to disrupt user experience and increase user frustration. Could be combined with other attacks to prevent users from accessing warnings or security notices. Low effort, high impact on user trust.

## Defensive takeaways
- Implement robust exception handling in object/embed tag processing code
- Validate and sanitize MIME type values before resource handler invocation
- Add tab recovery mechanism to restore previously crashed pages gracefully
- Test all valid MIME type combinations in object tag attributes
- Consider whitelisting supported MIME types rather than blacklisting problematic ones
- Add crash telemetry to detect malicious content patterns
- Implement content security policy enforcement for embedded objects

## Variant hunting
Test other HTML elements that accept MIME types (embed, iframe with type attribute), test with edge cases (empty type, whitespace, mixed case MIME types), fuzz MIME type parser with malformed values, check if video/audio/source tags are affected, test cross-origin object loading scenarios

## MITRE ATT&CK
- T1190
- T1499

## Notes
Report demonstrates responsible disclosure with PoC, crash logs, and video evidence. Severity is medium rather than high because: (1) requires user to visit attacker-controlled page, (2) crash is not exploitable for code execution, (3) user can close tab to recover. Reporter noted Brave's fork status and Firefox immunity is key evidence. Suggestion to implement crash recovery is valuable defensive guidance.

## Full report
<details><summary>Expand</summary>

## Summary:

Attacker could initiate DoS during page loading.

## Products affected: 

1.6 (18.05.17.13)
Device iPhone 6s (iOS 11.3.1)

## Steps To Reproduce:

PoC:
```html
<body>
    <script>
        let o = document.body.appendChild(document.createElement('object'));
        // application/json or application/pdf are valid values too
        o.type = 'text/html' // <-- triggers DoS
    </script>
</body>
```

The problem is the way Brave handles `<object>` tag with specific `type` attribute's values. 
Looks like unsupported mimeTypes or non-string values don't trigger crash, so I assume, that only valid mimeTypes could be used. Image mimeTypes don't trigger DoS.

## Supporting Material/References:

As I understood, Brave browser for iOS is a fork of Mozilla Firefox for iOS. 
Firefox isn't vulnerable, what makes this bug eligible. 

Crash log attached.
Screencast attached.

## Impact

The first page loaded after the browser crash is the crashed page. The PoC is immediate and doesn't require any additional interaction, so it could make browser broken, until the tab will be closed in offline.

> I suggest remembering the crashed page and ignoring it during browser opening. Probably, it could make all DoS attacks less dangerous.

> I'm not sure that the trick with tab closing in offline is obvious for most users.

</details>

---
*Analysed by Claude on 2026-05-24*
