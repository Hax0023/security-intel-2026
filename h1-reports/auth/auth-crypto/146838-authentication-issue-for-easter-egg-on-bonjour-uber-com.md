# Authentication Issue for easter egg on bonjour.uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 146838 | https://hackerone.com/reports/146838
- **Submitted:** 2016-06-23
- **Reporter:** ddworken
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
This probably (ok, almost definitely) is just informative but thought I would throw it out here anyways. :)

[bonjour.uber.com](bonjour.uber.com) hosts an easter egg (view source and scroll down) where the passcode is insecurely stored as a javascript variable. The source for the easter egg is: 

``` html
<script type="text/javascript">//error easter egg - call stack is intentionally complex
var p

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

This probably (ok, almost definitely) is just informative but thought I would throw it out here anyways. :)

[bonjour.uber.com](bonjour.uber.com) hosts an easter egg (view source and scroll down) where the passcode is insecurely stored as a javascript variable. The source for the easter egg is: 

``` html
<script type="text/javascript">//error easter egg - call stack is intentionally complex
var pressed = [];
var passcode = 'abcde';
document.addEventListener('keypress', keyPressed);
function keyPressed(e) {
  pressed.push(String.fromCharCode(e.charCode));
  if (pressed.join('') == passcode) {
    throw new Error('sentry test');
    pressed = [];
  }
  if (passcode.indexOf(pressed.join(''))) {
    pressed = [];
  }
}
</script>
```

The problem is that the passcode is stored as a string which means I can analyze the code in order to figure out that I must type in abcde to get the sentry test error. Instead of including it that way, I would like to suggest the following code change to increase security: 

``` javascript
var pressed = [];
var hashedPasscode = '03de6c570bfe24bfc328ccd7ca46b76eadaf4334';
document.addEventListener('keypress', keyPressed);
function keyPressed(e) {
  pressed.push(String.fromCharCode(e.charCode));
  if (sha1(pressed.join('') )== hashedPasscode) {
    throw new Error('sentry test');
    pressed = [];
  }
}
```

You could even switch to scrypt or some other more secure hashing algorithm for added security! :P 

</details>

---
*Analysed by Claude on 2026-05-24*
