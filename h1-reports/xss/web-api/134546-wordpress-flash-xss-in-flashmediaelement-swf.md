# WordPress Flash XSS in flashmediaelement.swf via Invalid URL Encoding Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 134546 | https://hackerone.com/reports/134546
- **Submitted:** 2016-04-26
- **Reporter:** cure53
- **Program:** WordPress
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Flash ExternalInterface Exploitation, URL Encoding Bypass, Unsafe URL Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
WordPress's bundled flashmediaelement.swf contains a reflected XSS vulnerability due to improper URL sanitization. The Flash file attempts to block GET parameters by comparing parsed URL query strings against flashVars, but this validation can be bypassed using invalid URL-encoded characters that the Flash player tolerates but the validation logic does not account for.

## Attack scenario
1. Attacker crafts a malicious URL with flashVars parameter names containing invalid URL escape sequences (e.g., %g)
2. The invalid escape sequence is stripped by the Flash player, revealing the true parameter name (e.g., jsinitfunction)
3. The 'GET Killer' validation code parses the URL string and sees the obfuscated parameter name with %g
4. Validation fails to match obfuscated name with the cleaned flashVar name, bypassing the protection
5. Malicious flashVar payload reaches vulnerable Flash methods like ExternalInterface.call()
6. JavaScript code is executed in the victim's browser with the privileges of the WordPress site

## Root cause
The sanitization logic in flashmediaelement.swf uses string matching between URL-encoded parameter names and actual flashVar names. It fails to account for the Flash player's tolerance of invalid URL encoding, which strips invalid escape sequences during parameter parsing. The validation compares the raw URL string (with %g) against decoded flashVar names (without %g), resulting in a mismatch that allows GET parameters to bypass the protection.

## Attacker mindset
The attacker recognized that URL encoding validation often differs between parsing layers. By introducing invalid escape sequences that browsers/Flash players discard but the validation code preserves, the attacker created a semantic gap allowing the bypass. Understanding Flash-specific parameter handling and ExternalInterface capabilities enabled exploitation of this common-but-flawed protection pattern.

## Defensive takeaways
- Sanitize and normalize input at a single layer after parsing, not before or during
- When blocking GET parameters, perform comparison on decoded/normalized values, not raw URL strings
- Understand platform-specific parsing behavior (Flash vs JavaScript differ in tolerance for malformed encoding)
- For Flash files, prefer allowlist approaches over blocklist/filter approaches when restricting parameter sources
- Consider serving Flash files with X-Content-Type-Options: nosniff and appropriate CORS headers to limit attack surface
- Retire Flash usage where possible; if required, audit all ExternalInterface.call() usages for injection vulnerabilities

## Variant hunting
Test other similar Flash-to-JavaScript bridge mechanisms for equivalent encoding bypass techniques
Search for similar parameter filtering patterns using whitespace variations, double-encoding, or Unicode bypasses
Check other WordPress bundled Flash files (mediaelement variations, older versions) for identical vulnerable code
Investigate whether navigateToURL() is also exploitable with similar encoding tricks in flashmediaelement.swf
Look for Flash files in other projects using identical 'GET Killer' protection pattern and test with invalid URL encoding
Test whether different invalid escape patterns (%x, %u, etc.) bypass validation in other contexts

## MITRE ATT&CK
- T1190
- T1059.001
- T1598.002
- T1566.002

## Notes
This vulnerability represents a critical failure in defense-in-depth for Flash security. The researchers (Heiderich, Kinugawa, Inführ) demonstrated sophisticated understanding of cross-layer parsing differences. The PoC URL uses backticks in alert`1` which is valid JavaScript but shows the attacker payload clearly. The vulnerability affected all WordPress installations with the vulnerable Flash file until patched. This is exemplary of why Flash usage became increasingly problematic and contributed to its eventual deprecation.

## Full report
<details><summary>Expand</summary>

Intro
==

WordPress is vulnerable against a reflected XSS that stems from an insecure URL sanitization problem performed in the file *flashmediaelement.swf*. The code in the file attempts to remove *flashVars* [¹](https://helpx.adobe.com/flash/kb/pass-variables-swfs-flashvars.html) in case they have been set GET parameters but fails to do so, enabling XSS via *ExternalInterface* [²](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/flash/external/ExternalInterface.html).

The attack technique was first described by Soroush Dalili in 2013 [³](https://soroush.secproject.com/blog/2013/10/catch-up-on-flash-xss-exploitation-bypassing-the-guardians-part-1/). The vulnerability in *flashmediaelement.swf* was discovered in April 2016, first identified as SOME[⁴](http://www.benhayak.com/2015/06/same-origin-method-execution-some.html) bug by Kinugawa. Then, after a team review, the XSS potential was discovered and analyzed by Heiderich, Kinugawa and Inführ. Finally, it was discovered, that this file comes packaged with latest WordPress and the issue was reported here by Heiderich et al. 

**PoC:**
https://example.com/wp-includes/js/mediaelement/flashmediaelement.swf?%#jsinitfunctio%gn=alert`1`

Background
==

In the browser-world, a Flash file can be fed with parameters in multiple ways.

**Way One:** *flashVars*

```html
<embed src="myFlashMovie.swf"
    quality="high"
    bgcolor="#ffffff"
    width="550"
    height="400"
    name="myFlashMovie"     
    FlashVars="myVariable=Hello%20World&mySecondVariable=Goodbye"
    align="middle"
    allowScriptAccess="sameDomain"
    allowFullScreen="false"
    type="application/x-shockwave-flash"
    pluginspage="http://www.adobe.com/go/getflash"
/>
```

**Way Two:** GET parameters

```
myFlashMovie.swf?myVariable=Hello%20World&mySecondVariable=Goodbye
```

Quite obviously, *flashVars* via GET give an attacker more leverage, especially in case the Flash file can be opened directly in the browser. No need to embed it, just attach the *flashVars* via GET and the fun begins. 

Not unlike many other Flash files, *flashmediaelement.swf* attempts to protect itself from *flashVars* being set via GET.

Attackers often abuse *flashVars* to exploit Flash XSS bugs originating from insecure handling of `navigateToURL`[⁵](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/flash/net/package.html), `ExternalInterface.call`[⁶](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/flash/external/ExternalInterface.html#call%28%29) and other risky methods. So, why not get rid of GET parameters in the first place:

```actionscript
// get parameters
// Use only FlashVars, ignore QueryString
var params:Object, pos:int, query:Object;

params = LoaderInfo(this.root.loaderInfo).parameters;
pos = root.loaderInfo.url.indexOf('?');
if (pos !== -1) {
	query = parseStr(root.loaderInfo.url.substr(pos + 1));

	for (var key:String in params) {
		if (query.hasOwnProperty(trim(key))) {
			delete params[key];
		}
	}
}

[...]

private static function parseStr (str:String) : Object {
	var hash:Object = {},
		arr1:Array, arr2:Array;

	str = unescape(str).replace(/\+/g, " ");

	arr1 = str.split('&');
	if (!arr1.length) {
		return {};
	}

	for (var i:uint = 0, length:uint = arr1.length; i < length; i++) {
		arr2 = arr1[i].split('=');
		if (!arr2.length) {
			continue;
		}
		hash[trim(arr2[0])] = trim(arr2[1]);
	}
	return hash;
}
```

From: https://github.com/johndyer/mediaelement/blob/master/src/flash/FlashMediaElement.as

The code shown above parses the URL query string and checks, if the GET parameter names spotted in there are also present among the flashVars (or vice versa). If a parameter name appears in both URL and the *flashVars* array, then the parameter must have been set via GET. If not, all is fine - and the parameter must have been set via *flashVars*. 

Let's call this code "The GET Killer"!

This way of "scrubbing" *flashVars* and making sure that no GET parameters can be used is fairly common and assumed to work well. But it can be bypassed using a dirty trick: invalid characters in the name of the GET parameters. Let's have a quick look at our PoC again:  

**PoC:**
https://example.com/wp-includes/js/mediaelement/flashmediaelement.swf?%#jsinitfunctio%gn=alert`1`

Notice something? We obfuscate the name of our GET parameter a bit.

```
jsinitfunctio%gn < see the %g?
```

The Flash player is very tolerant when handling input via GET. Invalid URL escapes for example will simply be stripped! This means, that despite us calling the GET parameter `jsinitfunctio%gn`, the parameter that really arrived in the Flash file is again called `jsinitfunction` because the invalid parts are stripped.

That of course messes up the "The GET Killer". Because now, the label it checks for based on the parsed URL string contains the `%g` but the actual flashVar does not! No match, no scrub. We can submit data by using GET again. 

Just like this: `({'jsinitfunctio%gn':''}).hasOwnProperty('jsinitfunction') // false`

But that's not all. The file *flashmediaelement.swf* ships more defensive mechanisms. One of them if for example a black-list that checks, that the parameter values paired with risky methods don't contain characters like parenthesis. Because that would indicate, that someone tries to smuggle in some executable code, like an `alert(1)` instead of just providing a callback, like `alert`.

```actionscript
private function isIllegalChar(s:String, isUrl:Boolean):Boolean {
	var illegals:String = "' \" ( ) { } * + \\ < >";
	if (isUrl) {
		illegals = "\" { } \\ < >";
	}
	if (Boolean(s)) { // Otherwise exception if parameter null.
		for each (var illegal:String in illegals.split(' ')) {
			if (s.indexOf(illegal) >= 0) {
				return true; // Illegal char found
			}
		}
	}
	return false;
}
```

From: https://github.com/johndyer/mediaelement/blob/master/src/flash/FlashMediaElement.as

As you can see, the method shown above checks the input for malicious characters that indicate executable JavaScript. Parenthesis, curlies, operators and all the nasty characters. From the ECMAScript 5 world. 

What is missing? The new ways of executing code offered by ECMAScript 6 by using back-ticks[⁷](https://developer.mozilla.org/de/docs/Web/JavaScript/Reference/template_strings). Let's have a look at the PoC again:

**PoC:**
https://example.com/wp-includes/js/mediaelement/flashmediaelement.swf?%#jsinitfunctio%gn=alert`1`

Notice something? We don't use parenthesis to execute the alert. We use back-ticks instead. And they are not blacklisted of course.

But we are still not finished, there is yet another security mechanism installed by *flashmediaelement.swf* to make the attacker's life harder. And this is a check for the `ExternalInterface.objectID`[⁸](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/flash/external/ExternalInterface.html#objectID). This particular member is only present, in case the embedding HTML element (`<embed>` or `<object>`) is applied with an "ID" attribute. Here is the important bit of code:


```actionscript
if (_output != null) {
	_output.appendText(txt + "\n");
	if (ExternalInterface.objectID != null && ExternalInterface.objectID.toString() != "") {
		var pattern:RegExp = /'/g; //'
		ExternalInterface.call("setTimeout", _jsCallbackFunction + "('" + ExternalInterface.objectID + "','message','" + txt.replace(pattern, "’") + "')", 0);
	}
} 
```

From: https://github.com/johndyer/mediaelement/blob/master/src/flash/FlashMediaElement.as

So, again. If the Flash file wasn't properly embedded but opened directly, the whole thing will not work.

Now, let's have a look how browsers actually embed Flash files when they are supposed to open them "directly" (by requesting the Flash/SWF file from the affected server). Because browers generate quite a bit of markup when opening an SWF directly.

**Firefox does this:**
```html
<html><head><meta name="viewport" content="width=device-width; height=device-hei

</details>

---
*Analysed by Claude on 2026-05-12*
