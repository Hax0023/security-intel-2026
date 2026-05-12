# Reflected XSS in Evernote Shared Note View via ionUrl Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1518343 | https://hackerone.com/reports/1518343
- **Submitted:** 2022-03-22
- **Reporter:** sarka
- **Program:** Evernote
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient URL Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in Evernote's shared note viewer endpoint that allows attackers to execute arbitrary JavaScript by bypassing a flawed URL validation check. The vulnerability exists in the renderAfterSaveNoteView() function which validates the ionUrl parameter by checking if it contains 'https://www.evernote.com/' substring rather than verifying it starts with the trusted domain. An attacker can inject a javascript: URI scheme followed by the domain substring in a comment to execute arbitrary code in victims' browsers.

## Attack scenario
1. Attacker crafts a malicious URL with view=after-save-note and ionUrl=javascript:alert(document.cookie)//https://www.evernote.com/
2. Attacker sends the URL to a victim via email, chat, or social engineering
3. Victim clicks the link to the Evernote shared note viewer
4. The vulnerable renderAfterSaveNoteView() function checks if 'https://www.evernote.com/' exists anywhere in ionUrl parameter (not validating it starts with the domain)
5. The function sets window.location.href to the javascript: URI, executing the attacker's payload
6. Attacker's JavaScript executes in victim's browser with full access to session cookies and DOM

## Root cause
The validation logic uses indexOf() to check if the trusted domain substring exists anywhere within the ionUrl parameter, rather than using startsWith() or prefix validation. This allows attackers to prepend arbitrary protocols (like javascript:) before the domain substring and use URL comments (//) to neutralize the validation bypass check.

## Attacker mindset
An attacker would recognize that substring validation is weaker than prefix validation and that javascript: URIs can be embedded in locations expected to receive URLs. They would exploit the comment syntax to effectively disable the validation check while maintaining the required substring.

## Defensive takeaways
- Use strict URL validation with startsWith() or URL parsing APIs rather than substring searches with indexOf()
- Implement allowlist-based URL validation that explicitly checks the protocol is http/https and domain matches exactly
- Use the URL constructor or similar APIs to parse and validate URLs rather than string manipulation
- Apply Content Security Policy (CSP) with default-src and script-src directives to prevent javascript: URI execution
- Perform server-side validation and sanitization of redirect parameters rather than relying solely on client-side checks
- Never trust user-controlled parameters in window.location.href assignments without robust validation
- Use a redirect endpoint that accepts only pre-approved destination URLs or sanitized paths

## Variant hunting
Search for other switch cases in the renderWithContext() function that might accept user-controlled parameters
Review other redirect/navigation functions in the application that use indexOf() for URL validation
Test other URL parameters (sn, title, noteGuid, noteKey) for similar validation bypasses
Check Evernote's other subdomains and endpoints for similar vulnerable redirect patterns
Look for DOM-based XSS in the renderContent() function that displays note content
Test if similar flawed validation exists in desktop or mobile client code
Search for other locations where window.location assignments occur with user-supplied data

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204.001

## Notes
The vulnerability is straightforward but demonstrates a common security mistake: using substring matching instead of proper prefix/protocol validation for URL redirects. The attacker demonstrates good understanding of JavaScript URL schemes and comment syntax to bypass the flawed check. The fix is simple but critical for security.

## Full report
<details><summary>Expand</summary>

## Summary:

There is a reflected XSS vulnerability on https://evernote.com, in the shared web note view, triggered through the ```view``` and ```ionUrl``` parameters of the ***/shard/s[SHARD_NUMBER]/client/snv*** endpoint.

## Description:


When a user creates a note and shares it, it is stored in the following endpoint, being accessible by its ```GUID``` and generated ```KEY```: ***https://www.evernote.com/shard/s[SHARD_NUMBER]/sh/[NOTE_GUID]/[NOTE_KEY]***.

The above link redirects to another generated link this is going to be used to access the ressource in the web note viewer, and has the following format:
***https://www.evernote.com/shard/s[SHARD_NUMBER]/client/snv?noteGuid=[NOTE_GUID]&noteKey=[NOTE_KEY]&sn=[PREVIOUS_LINK]&title=[NOTE_TITLE]***

When accessing from this web note viewer link, a script named ***main.68d4af6d45d9dcaab6e6.js*** is fetched from ***https://dashboard.svc.www.evernote.com/app/nv/***, used to format and display the note properly.

After analyzing this file, we can observe at line 3353 of this script (beautify the script first) a function named ```renderWithContext()``` that handles different ways of rendering the note:

```javascript
renderWithContext() {
    switch (this.view) {
		case "content-unavailable":
			return this.renderContentUnavailable({
				header: this.state.i18n.t("SharedNote.contentUnavailable.info"),
				body: this.state.i18n.t("SharedNote.contentUnavailable.downloadInfo")
			});
		case "saved":
			return this.renderContentUnavailable({
				header: this.state.i18n.t("SharedNote.contentUnavailable.savedOnMobile.info"),
				body: this.state.i18n.t("SharedNote.contentUnavailable.savedOnMobile.downloadInfo")
			});
		case "notelink":
			return this.renderNoteLinkView();
		case "after-save-note":
			return this.renderAfterSaveNoteView()
	}
	const { embedMode: e } = this.state;
	return e ? this.renderContent() : o.createElement("div", {
		className: Gn.appContainer
	}, this.renderHeader(), this.renderContent())
}
```

Since the ```this``` object represent the current URL parameters, the switch statement ```switch (this.view)``` gives away that we can reach this function by adding a ```view``` parameter in the URL. 

The vulnerable case here is ```after-save-note```. Here is what the ```renderAfterSaveNoteView()``` function looks like:

```javascript
renderAfterSaveNoteView() {
	if (W())
		if (R.isMobile) {
			const e = oe(R.isMobile);
			e && (window.location.href = e)
		} else {
			const e = function () {
				const e = W();
				let n = e && e.ionUrl;
				return n && -1 === n.indexOf(J.baseUrl) ? null : n
			}();
			e && (window.location.href = e)
		}
	return null
}
```

We can observe line 12 that this script sets the ```window.location.href ``` attribute to the variable ```e```.  As line 9 shows, we also control this variable ```e``` as it represents an additional parameter we have to add in the URL: ```ionUrl```.

However, we can see at line 10 a security measure that will try to prevent attacker from setting the ```window.location.href``` attribute to anything outside evernote.com: ```J.baseUrl``` contains the value "https://www.evernote.com/". This line basically checks if the substring "https://www.evernote.com/" is present in the provided ```ionUrl``` URL parameter.

That's where the vulnerability resides; it only checks if the substring "https://www.evernote.com/" is in the provided ```ionUrl``` URL parameter, but not that it starts by it.

**I was then able to execute javascript by passing the following payload to ```ionUrl``` : ```javascript:alert(document.cookie)//https://www.evernote.com/```, using javascript comments to comment-out the evernote link (and setting ```view``` to ```after-save-note``` in order to reach this function).**

Here is the POC that will display current cookies in an alert box:
https://www.evernote.com/shard/s1/client/snv?view=after-save-note&ionUrl=javascript:alert(document.cookie)//https://www.evernote.com/

***The link to the note doesn't have to valid, only the view and ionUrl parameters matter. An attacker could also have a valid note link that is properly displayed, and still execute the javascript silently. He can also force the user to sign-in beforehand to make sure to get his cookies.***

This has been tested  and working on up-to-date Firefox and up-to-date Chrome.
This exploit works on the latest version of Evernote.

## Steps To Reproduce:

  1. Click on the following link: https://www.evernote.com/shard/s1/client/snv?view=after-save-note&ionUrl=javascript:alert(document.cookie)//https://www.evernote.com/

## Supporting Material/References:

  {F1663424}   {F1663430}

## Impact

An attacker can execute script in a victim's browser, making him able to take over accounts of victims, make victims perform action without their consent, steal their private data, install malware, and so on.

</details>

---
*Analysed by Claude on 2026-05-12*
