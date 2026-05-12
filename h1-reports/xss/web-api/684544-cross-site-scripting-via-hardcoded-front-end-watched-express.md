# Cross-site scripting via hardcoded front-end watched expression in algorithm debugger

## Metadata
- **Source:** HackerOne
- **Report:** 684544 | https://hackerone.com/reports/684544
- **Submitted:** 2019-08-29
- **Reporter:** irisrumtub
- **Program:** Quantopian
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-site scripting (XSS), Insufficient input validation, Unsafe HTML rendering, Code injection
- **CVEs:** None
- **Category:** web-api

## Summary
A hardcoded watched expression in the algorithm debugger (`get_datetime().strftime()`) renders unsanitized output directly to the DOM. An attacker can override this expression via a custom class to inject malicious JavaScript that executes in the context of collaborators or users who clone and run the algorithm.

## Attack scenario
1. Attacker creates a malicious Python class that overrides `get_datetime()` to return XSS payload instead of datetime string
2. Attacker adds this class to algorithm code and triggers debugger validation, which sends WebSocket request with the watched expression
3. Debugger executes the malicious expression and receives XSS payload in response
4. Frontend JavaScript renders the response unsanitized into the DOM at the hardcoded calendar location
5. JavaScript payload executes in victim's browser context with access to quantopian.com origin
6. Attacker can steal algorithms, session tokens, or perform actions as the victim

## Root cause
The frontend code contains a hardcoded string constant (`get_datetime().strftime("%Y-%m-%d %H:%M:%S")#__QUANTOPIAN__`) used to identify watched expressions for the debugger. The response is directly rendered as HTML without sanitization because the developers assumed only legitimate datetime output would be returned. No validation exists on the backend to restrict what user-defined expressions can output.

## Attacker mindset
The attacker methodically reverse-engineered the debugger's WebSocket protocol, identified the hardcoded watched expression, verified unsanitized rendering through response interception, and discovered they could override Python built-in functions to inject arbitrary output. They recognized two distinct attack vectors: silent injection during collaboration and obfuscated payload distribution via algorithm cloning.

## Defensive takeaways
- Never render dynamic content into the DOM without sanitization, even if you believe only specific output formats will occur
- Avoid hardcoding sensitive strings in frontend code that can be relied upon for security decisions
- Implement content security policy (CSP) to prevent inline script execution
- Sanitize all WebSocket responses, especially those containing user-influenced data
- Use templating engines with auto-escaping for HTML rendering
- Validate that watched expression outputs conform to expected format on both frontend and backend
- Consider using textContent instead of innerHTML when displaying dynamic values
- Implement code review processes to catch assumptions about input trustworthiness

## Variant hunting
Search for other hardcoded frontend constants used to identify or display user-influenced data
Check for additional watched expressions or debugger display elements that might have similar patterns
Look for other WebSocket handlers that render responses without sanitization
Investigate if other Python execution contexts (backtests, live trading) have similar override opportunities
Test if other debugger features (variable inspection, memory display) have sanitization issues
Check for similar patterns in related products or alternative debugging interfaces

## MITRE ATT&CK
- T1190: Exploit public-facing application
- T1059: Command and scripting interpreter (Python)
- T1204: User execution
- T1566: Phishing (if algorithm link is shared)
- T1539: Steal web session cookie
- T1005: Data from local system

## Notes
This is a sophisticated vulnerability that combines frontend XSS with backend code execution capabilities. The attacker's understanding of the debugger architecture and WebSocket protocol was critical. The persistence mechanism (storing malicious class in algorithm) and silent attack vector (no visible UI changes) make this particularly dangerous. The report demonstrates excellent security research methodology including protocol analysis, assumption verification, and impact assessment.

## Full report
<details><summary>Expand</summary>

Hello, favorite security team. This is so far most interesting XSS i've found on your website. And also this is 10th bug i report you, so im gonna celebrate.

**Summary:** Via hardcoded front-end code in algo debugger one is able to execute XSS on algorithm collaborator. One is able to use python to change the output of that hardcoded expression, which is unsanitized HTML, where cross-site scripting fires. Additionally, one can store the malicious code in algorithm and share it, so XSS will fire on anyone who will clone and run the algorithm. 

**Description:** 
This is an interesting one. First, i noticed that when one validates the code **with debugger**, a certain web socket request is sent
```json
{"e":"set_watch","p":["get_datetime().strftime(\"%Y-%m-%d %H:%M:%S\")#__QUANTOPIAN__"]}
```
By lurking deeper, I've determined that this request sets watched expression, the one that is in charge of current date and time in the debugger:
{F569596}
To check the assumption that this place might contain unsanitized html, i've intercepted incoming web socket response with the result of aforementioned expression (datetime) and added an XSS payload to it, and it worked.

The fact that it is set as a user-defined watched expression got me thinking. We can remove it manually, and calendar will disappear. And we can set it again, and it will reappear, which was interesting. I've tried several different expressions with #__QUANTOPIAN at the end, but nothing appeared where calendar is supposed to be. I wrote to JD on Quantopian's slack, who was kind enough to tell me:
>exact string (including ```get_datetime()```, not just the trailing ```__QUANTOPIAN__``` part) is used as a command from our frontend javascript code to request the current algorithm execution time between each other command that the user sends. However, that exact string is stored as a constant in our frontend code, so only the response that matches that exact value will be shown in the date area.

...what basically means that any output that is generated by this exact expression goes directly into unsanitized HTML.

So we force this expression to output what we want by adding this class :)

----------------
```python
class get_datetime():
    def __init__(self):
        self.img = '<img src=x'+' one'+'rror=alert(1)>'
    def strftime(self, x=None):
        return self.img
```
--------------
And next time debugger is launched, expression ```get_datetime().strftime("%Y-%m-%d %H:%M:%S")#__QUANTOPIAN__``` outputs ```<img src=x onerror=alert(1)>```, executing javascript.

I'd like to additionally say that there are two vectors of the attack.
* attack on the collaborator. This is as sneaky, as #615672, because it requires no interaction with the victim. We can either wait for him to be away from keyboard and re-validate our algorithm code with malicious class. Or we can start the backtest even without the code visible, and just intercept outgoing POST request, and since it sends the whole code, we can add our malicious class there. It will not appear visible at any point, but xss will fire.
* attack on anyone who will clone malicious algorithm and run it in his own ide with debugger. First we can obfuscate the code (especially if algo is large, this becomes easier), and share it.

## Steps To Reproduce:

(Add details for how we can reproduce the issue)

  1. add xss class to algo code
  2. set breakpoint in code so debugger will open, start 
  3. execute it on collaborator, or obfuscate class and share it.

## Supporting Material/References:
{F569615}

## Test account information
tvburis+hackerone@gmail.com
irisrumtub+hackerone@mail.ru

## Impact

Execute our own javascript with all the consequences, steal algorithms (because xss happens on quantopian.com).

</details>

---
*Analysed by Claude on 2026-05-12*
