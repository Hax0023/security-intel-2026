# Denial of Service in Brave Browser for iOS via Object Tag MIME Type

## Metadata
- **Source:** HackerOne
- **Report:** 357665 | https://hackerone.com/reports/357665
- **Submitted:** 2018-05-26
- **Reporter:** metnew
- **Program:** Brave
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Denial of Service, Crash/Hang, Resource Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
Brave browser for iOS crashes when an HTML object element with specific MIME type attributes (text/html, application/json, application/pdf) is dynamically created during page load. The crash is immediate, requires no user interaction, and persists across browser restarts unless the tab is manually closed offline.

## Attack scenario
1. Attacker creates a malicious webpage containing JavaScript that executes during page load
2. Script dynamically creates an HTML object element and sets its type attribute to a valid MIME type like 'text/html'
3. Brave's object tag handler attempts to process the MIME type, triggering an unhandled exception
4. Browser process crashes immediately, displaying the PoC page on next startup
5. User's Brave browser becomes non-functional until they manually close the offending tab while offline
6. Attacker can distribute the malicious page via social engineering or compromised websites to cause persistent DoS

## Root cause
Brave's fork of Firefox for iOS contains a vulnerability in the object element handler when processing certain valid MIME types. The code likely fails to properly validate or safely handle object instantiation for specific MIME types, causing a crash rather than graceful degradation.

## Attacker mindset
Adversary seeks to cause persistent disruption by exploiting browser crash handling. The attack is valuable because it requires zero user interaction, survives browser restart, and affects mobile users who may not know the offline tab-closing workaround.

## Defensive takeaways
- Implement proper exception handling around all object element MIME type processing
- Validate and sanitize MIME type attributes before attempting to instantiate handlers
- Maintain a blacklist of recently crashed pages to prevent immediate re-loading on startup
- Ensure graceful degradation for unsupported or problematic MIME types instead of crashing
- Add fuzzing tests for object/embed tag handling with various MIME types
- Implement recovery mechanisms to automatically skip problematic tabs on restart
- Consider sandboxing object element processing to contain crashes

## Variant hunting
Test embed tag with same MIME types instead of object tag
Try dynamic modification of type attribute after element creation
Test with data: URLs combined with MIME type attributes
Attempt nested object elements with conflicting MIME types
Test iframe with unsupported MIME type attributes
Verify if setting type attribute via JavaScript setAttribute vs HTML differs
Test with additional valid MIME types not mentioned in original report
Attempt to trigger with object elements in SVG or XML contexts

## MITRE ATT&CK
- T1499
- T1190

## Notes
Report explicitly notes that Firefox is not vulnerable despite Brave being a fork, indicating the vulnerability was introduced during Brave's modifications. Reporter suggests session recovery improvements as a mitigation. The offline tab-closing workaround is non-obvious to typical users, increasing real-world impact. Crash occurs in WebKit/rendering layer during object element processing.

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
