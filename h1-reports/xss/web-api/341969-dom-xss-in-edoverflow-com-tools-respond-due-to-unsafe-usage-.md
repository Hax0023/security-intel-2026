# DOM XSS in edoverflow.com/tools/respond via unsafe innerHTML usage

## Metadata
- **Source:** HackerOne
- **Report:** 341969 | https://hackerone.com/reports/341969
- **Submitted:** 2018-04-23
- **Reporter:** karel_origin
- **Program:** edoverflow.com
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** DOM-based Cross-Site Scripting (XSS), Unsafe DOM Manipulation
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in the respond tool due to unsafe usage of innerHTML property with user-controlled input. User input from form fields is directly inserted into the DOM via innerHTML.replace() without sanitization, allowing arbitrary JavaScript execution through crafted payloads in the triager or hacker username fields.

## Attack scenario
1. Attacker creates a malicious HTML page with clickjacking overlay or social engineering to lure victim
2. Victim visits the malicious page and interacts with the draggable frog elements as instructed
3. Victim clicks 'Make friends!' button to submit the form with attacker-controlled usernames
4. Form submission triggers JavaScript that reads triager and hacker input values containing XSS payload (e.g., '<img src=x onerror=alert(1)>')
5. Code executes: document.body.innerHTML = document.body.innerHTML.replace('{{triager}}', triager) with malicious payload
6. Payload is parsed as HTML/JavaScript and executes in victim's browser context with access to cookies, localStorage, and session tokens

## Root cause
Direct assignment of user-controlled input to innerHTML via string replacement without HTML encoding or sanitization. The innerHTML property parses HTML and executes embedded scripts, making it dangerous for dynamic content insertion.

## Attacker mindset
Exploit trivial input validation gaps in client-side code. The vulnerability requires user interaction but is easily weaponizable through social engineering or clickjacking. Target developers' tools where security may be deprioritized.

## Defensive takeaways
- Never use innerHTML with user-controlled input; use textContent or innerText for plain text insertion
- If HTML insertion is required, use DOM APIs like createElement() and appendChild() instead of string manipulation
- Implement HTML encoding/escaping libraries (DOMPurify, xss package) before any dynamic content insertion
- Avoid string replacement patterns for template substitution; use proper template engines with auto-escaping
- Apply Content Security Policy (CSP) headers to mitigate XSS impact
- Use security linters (eslint-plugin-security) to detect unsafe DOM operations during development
- Validate and sanitize all user inputs on both client and server side
- Use type='button' instead of type='submit' if form submission logic is not required

## Variant hunting
Search for other instances of innerHTML.replace() or innerHTML += patterns with user input across the codebase
Audit localStorage and sessionStorage retrieval that feeds into innerHTML without sanitization
Check for DOM XSS in other tools on edoverflow.com (calculator, encoder, etc.) using similar patterns
Look for similar vulnerabilities in other developer tool websites sharing similar architecture
Test form handling in older code sections that may predate security awareness
Review any AJAX/fetch handlers that update innerHTML with server responses

## MITRE ATT&CK
- T1190
- T1204.001

## Notes
The vulnerability requires user interaction (form submission triggered by victim), reducing severity to medium. The attacker demonstrated clickjacking/social engineering as necessary prerequisite. The fix correctly migrates from innerHTML to innerText and uses proper DOM methods. The report shows good understanding of root cause but acknowledges limited real-world impact due to no authentication requirement and tool nature. Timeline and bounty amount not disclosed in writeup.

## Full report
<details><summary>Expand</summary>

Hi,

There's a DOM XSS vulnerability on [edoverflow.com](https://edoverflow.com/tools/respond/). This cannot be exploited without user-interaction so I had to make a clickjacking PoC to trick the user in triggering the payload her/himself.

#Reproduction Steps
1. Open the attached HTML document in FireFox.
2. Drag Frog 1 to the other (two) frogs.
3. Click on the "Make friends!" button.

Result: 
{F289573}

# Vulnerable JavaScript

```
<html>
<script>
/* ===========================================
  Allow users to submit usernames and store 
  them in localStorage for future use.
============================================*/
document.getElementById("form").addEventListener("submit", function(){
    var triager = document.getElementById("triager").value;
    var hacker = document.getElementById("hacker").value;
    console.log(hacker); // Why is this not executing?
    document.body.innerHTML = document.body.innerHTML.replace('{{triager}}', triager);
    document.body.innerHTML = document.body.innerHTML.replace('{{username}}', hacker);
    //localStorage.setItem("triager", triager);

//var retrieve = localStorage.getItem("triager"); // Why does this return "null"?
//document.body.innerHTML = document.body.innerHTML.replace('{{triager}}', retriev
document.getElementById("remove").addEventListener("click", function(){
    localStorage.removeItem("triager");
});
</script>
</html>
```

#Fix

~~~diff
- <input type="submit" name="submit" class="button">
+ <input type="button" class="button" id="submit">
~~~

~~~diff
       Allow users to submit usernames and store 
       them in localStorage for future use.
     ============================================*/
-    document.getElementById("form").addEventListener("submit", function(){
-        var triager = document.getElementById("triager").value;
-        var hacker = document.getElementById("hacker").value;
+       elem = document.getElementsByTagName("pre")[0].children[0];
+
+    document.getElementById("submit").addEventListener("click", function(){
+        var trger = document.getElementById("triager").value;
+        var hckr = document.getElementById("hacker").value;
         console.log(hacker); // Why is this not executing?
-        document.body.innerHTML = document.body.innerHTML.replace('{{triager}}', triager);
-        document.body.innerHTML = document.body.innerHTML.replace('{{username}}', hacker);
-        //localStorage.setItem("triager", triager);
+               elem.innerText = elem.innerText.replace("{{username}}", trger).replace("{{triager}}", hckr);
+        localStorage.setItem("triager", trger);
     });
 
-    //var retrieve = localStorage.getItem("triager"); // Why does this return "null"?
-    //document.body.innerHTML = document.body.innerHTML.replace('{{triager}}', retrieve);
+    if(localStorage.getItem("triager") != null) {
+       var trger = localStorage.getItem("triager"); // Why does this return "null"?
+       elem.innerText = elem.innerText.replace("{{triager}}", trger);
+    }
 
     document.getElementById("remove").addEventListener("click", function(){
         localStorage.removeItem("triager");
     });

~~~

Raw (JS attached)

## Impact

There is not much that can be done because it looks like most pages don't require authentication, I also don't think that the owner of this website would fall for something like this. ;)


Thanks,
Karel.

The hacker selected the **Cross-site Scripting (XSS) - DOM** weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers:

**URL**
https://edoverflow.com/tools/respond/

**Verified**
Yes



</details>

---
*Analysed by Claude on 2026-05-12*
