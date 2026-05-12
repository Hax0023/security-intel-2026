# CSS Sanitizer Bypass: position: fixed !important Phishing Overlay in Roundcube

## Metadata
- **Source:** HackerOne
- **Report:** 3590586 | https://hackerone.com/reports/3590586
- **Submitted:** 2026-03-07
- **Reporter:** nullcathedral
- **Program:** Roundcube
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** CSS Injection, Input Validation Bypass, Phishing, XSS (Non-Stored Visual)
- **CVEs:** None
- **Category:** memory-binary

## Summary
Roundcube's CSS sanitizer bypasses its fixed-position overlay protection when the value includes the !important flag. The sanitizer's strcasecmp() check for 'fixed' fails on 'fixed !important', allowing the malicious CSS to pass through token-based validation and reassemble, enabling attackers to create full-viewport phishing overlays in HTML emails.

## Attack scenario
1. Attacker crafts an HTML email with a CSS rule using 'position: fixed !important' instead of plain 'position: fixed'
2. Email is sent to Roundcube user, arriving in inbox
3. When user opens the email, rcube_utils.php's sanitize_css_block() is invoked to sanitize the CSS
4. The strcasecmp($value, 'fixed') check fails because $value is 'fixed !important', not 'fixed'
5. The CSS value falls through to explode_css_property_block(), which tokenizes it into ['fixed', '!important'], both passing individual allowlists
6. Reassembled CSS renders 'position: fixed !important', creating a full-viewport overlay with phishing content (fake login prompt, etc.) that covers the entire message view or browser window

## Root cause
The sanitizer uses an exact string comparison (strcasecmp($value, 'fixed') === 0) to detect and convert fixed positioning. This fails when CSS importance modifiers or other tokens are appended to the value. The fallback tokenization logic does not account for compound values and treats each token independently, allowing dangerous combinations to reconstruct and persist in the output.

## Attacker mindset
An attacker recognizes that security controls often check for exact matches or simple patterns. By appending CSS modifiers like !important, the attacker bypasses the fixed-position detection while maintaining the same visual effect. This technique is a classic case of security-through-string-matching being defeated by CSS syntax flexibility. The attacker leverages Roundcube's trust in HTML emails to deliver a convincing phishing overlay that users encounter in a high-trust context.

## Defensive takeaways
- Parse CSS properties into structured tokens (property name, value, modifiers) before validation rather than relying on string matching
- Use a whitelist approach where only specific (property, value, modifier) combinations are allowed; deny all others
- When sanitizing sensitive properties like 'position', strip the entire property and all its modifiers if any dangerous value is detected, rather than attempting a conversion
- Validate CSS using a proper CSS parser or AST, not string operations or simple tokenization
- For email rendering contexts, consider a stricter default-deny policy for position properties, allowing only 'static' and 'relative'
- Implement defense-in-depth: even if CSS is sanitized, use iframe sandboxing or viewport restrictions to limit overlay impact
- Regularly audit CSS sanitization logic against CSS specification changes and edge cases (e.g., calc(), var(), multiple modifiers)

## Variant hunting
Test other CSS importance/cascade techniques: 'position: fixed!important' (no space), 'position: fixed  !important' (extra spaces)
Try other positioning values with modifiers: 'position: sticky !important', 'position: -webkit-sticky !important'
Test compound CSS values: 'position: fixed; z-index: 99999 !important' in a single property (if parser concatenates)
Check if other dangerous properties have similar exact-match checks: 'display', 'visibility', 'overflow', 'clip'
Attempt CSS variable injection: 'position: var(--pos)' where --pos is defined as 'fixed !important'
Try CSS custom properties with fallbacks: 'position: var(--pos, fixed !important)'
Test calc() expressions: 'position: calc(0 + fixed) !important' (unlikely but worth checking)
Check for case-sensitivity bypasses: 'position: FIXED !important', 'position: Fixed !important'
Investigate other sanitizer functions in the codebase for similar exact-match validation patterns

## MITRE ATT&CK
- T1566.002 - Phishing: Spearphishing Link (email with phishing overlay)
- T1566.001 - Phishing: Spearphishing Attachment (HTML email content)
- T1583.006 - Acquire Infrastructure: Web Services (attacker's phishing server)
- T1598.003 - Gather Victim Information: Web 3PO Cookie (credential harvesting via phishing overlay)
- T1190 - Exploit Public-Facing Application (CSS injection via email handler)

## Notes
This vulnerability is particularly dangerous in email clients because users expect to see benign content in emails and are in a lower-security mindset. The phishing overlay can convincingly impersonate Roundcube's own UI (e.g., 'Session Expired' message) to steal credentials. The !important flag is a common CSS technique that developers may not anticipate as a bypass vector. The vulnerability demonstrates why CSS sanitization is difficult and why security teams should use established libraries (e.g., DOMPurify with strict CSS configs) rather than custom implementations. The fix should involve parsing CSS at a semantic level rather than string-level checks.

## Full report
<details><summary>Expand</summary>

When sanitizing CSS, Roundcube's `sanitize_css_block()` in [rcube_utils.php](https://github.com/roundcube/roundcubemail/blob/4e95ebe12/program/lib/Roundcube/rcube_utils.php) converts `position: fixed` to `position: absolute` to prevent overlay attacks ([L555-557](https://github.com/roundcube/roundcubemail/blob/4e95ebe12/program/lib/Roundcube/rcube_utils.php#L555-L557)).

However, the check uses `strcasecmp($value, 'fixed') === 0`, which requires the **entire** trimmed value to be exactly `"fixed"`. The value `"fixed !important"` fails this comparison. The value then flows through the generic token-based validation path, where `explode_css_property_block()` splits it into tokens `['fixed', '!important']` that both individually pass the allowlist, reassembling as `position: fixed !important` in the output.

## Steps To Reproduce

Step 1: Send an HTML email with the following body:

```html
<!DOCTYPE html>
<html>
<head><title>Account Update</title></head>
<body>
<p>Please see below for your account details.</p>

<style>
.overlay {
    position: fixed !important;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: white;
    z-index: 99999;
    display: flex;
    align-items: center;
    justify-content: center;
}
.dialog {
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 30px;
    max-width: 400px;
    text-align: center;
    font-family: Arial, sans-serif;
}
</style>

<div class="overlay">
  <div class="dialog">
    <h2>Session Expired</h2>
    <p>Your Roundcube session has expired due to inactivity.</p>
    <p><a href="https://ATTACKER_SERVER/phish/login" style="background:#0066cc;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;">Sign In Again</a></p>
  </div>
</div>

</body>
</html>
```

Step 2: Open the email in Roundcube.

Step 3: Observe the phishing overlay covering:
- The **preview pane** (iframe) in normal view
- The **full browser viewport** when the message is opened in a new window (no iframe)

{F5484824}
{F5484826}

## Impact

CSS injection, phishing

</details>

---
*Analysed by Claude on 2026-05-12*
