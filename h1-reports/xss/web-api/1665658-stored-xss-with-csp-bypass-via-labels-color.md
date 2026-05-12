# Stored XSS with CSP Bypass via Unsanitized Label Colors in GitHub Project Import

## Metadata
- **Source:** HackerOne
- **Report:** 1665658 | https://hackerone.com/reports/1665658
- **Submitted:** 2022-08-10
- **Reporter:** yvvdwf
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Content Security Policy Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
GitLab's GitHub project import functionality fails to sanitize label color values, allowing attackers to inject arbitrary JavaScript code that executes when labels are viewed. The injected payload bypasses Content Security Policy protections, enabling arbitrary client-side actions on behalf of victims.

## Attack scenario
1. Attacker sets up a malicious GitHub-compatible server endpoint that returns project data with XSS payload embedded in label color fields
2. Attacker crafts a GitHub import request to GitLab pointing to the malicious server, specifying a target namespace they control or a namespace where they have access
3. GitLab fetches project and label metadata from the attacker's server without proper sanitization of color field values
4. Malicious label color payload (e.g., JavaScript via data URI or SVG injection) is stored in GitLab's database as part of the imported project's label configuration
5. Victim or administrator views the imported project's labels page
6. Stored XSS payload executes in victim's browser context, bypassing CSP, allowing session hijacking, CSRF attacks, or credential theft

## Root cause
GitLab's GitHub import service does not validate or sanitize the 'color' field of imported labels before storing them in the database. The color field is later rendered without proper HTML encoding or Content Security Policy restrictions, allowing arbitrary script execution.

## Attacker mindset
Exploit the import functionality as a trusted data integration point to bypass standard input validation. Leverage the assumption that imported data from GitHub is safe, targeting administrative users or project members who have higher privileges and viewing permissions.

## Defensive takeaways
- Implement strict input validation for all imported data, treating external sources with the same scrutiny as user-supplied input
- Sanitize and validate color values against a whitelist of valid hex color codes or RGB formats before storage
- Apply context-aware output encoding when rendering label colors in HTML/CSS contexts
- Implement and enforce strong Content Security Policy headers that prevent inline script execution
- Use a security-focused templating engine that automatically escapes values by default
- Conduct security review of all data import mechanisms and third-party integrations
- Add automated tests for XSS payloads in all user-controllable and imported fields
- Implement a Web Application Firewall (WAF) rule to detect common XSS patterns in label imports

## Variant hunting
Check other import mechanisms (Bitbucket, GitLab, etc.) for similar unsanitized fields like description, title, or custom fields
Review all label-related endpoints for stored XSS in other fields (name, description)
Test project/milestone/issue imports for similar color field vulnerabilities
Investigate custom field imports and metadata handling in other integrations
Check if other styling-related fields (background, border-color, etc.) have similar issues

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter
- T1598: Phishing - Generic
- T1598.003: Spearphishing Link
- T1566: Phishing

## Notes
The vulnerability is particularly severe because: (1) it affects the import feature which is expected to be a trusted operation, (2) the CSP bypass indicates sophisticated payload encoding, (3) the attack surface includes all users who can import GitHub projects, (4) the stored nature means persistence across sessions and user browsing. The reporter demonstrated strong capability by creating a mock GitHub server to bypass GitHub's own label color restrictions, showing determination to exploit the actual target's weaknesses rather than limitations of the source platform.

## Full report
<details><summary>Expand</summary>

Gitlab allows to import a project from Github. It imports also the labels whose colors are not sanitized. This leads to Stored-XSS. 


# Step to reproduce

To reproduce, we need the following prerequisite: 

- Github does not allow neither to create arbitrary label colors. You can find in the attachment a dummy Github server
- A VM/machine to host the dummy server above with an public IP though that gitlab.com can access to.
- I created the dummy server using nodejs, so you need to have also nodejs on the machine
- A Gitlab personal access token. Go [here](https://gitlab.com/-/profile/personal_access_tokens?name=test&scopes=api) to create a new token with within `api` scope.


# Step 1: run the dummy server

- Copy the attachment file on your machine and decompress it to any folder, e.g., `/tmp/dummy-server`
- Go to `/tmp/dummy-server` then run this command: `node ./index.js YOUR_IP YOUR_PORT` in which, you should replace `IP` and `PORT` with the one you have. For example, `sudo node index.js 51.75.74.52 80`

# Step 2: trigger Gitlab import

- Open a new terminal, then run the following command in which:

   + `YOUR_IP` and `YOUR_PORT` by the values in the previous step
   + `YOUR_GITLAB_TOKEN` is the api token you've created in the pre-requirement
   + `YOUR_GITLAB_USERNAME` is the target namespace you want to import the project to. It can be your username, or a group name

```bash
curl -kv "https://gitlab.com/api/v4/import/github" \
  --request POST \
  --header "content-type: application/json" \
  --header "PRIVATE-TOKEN: YOUR_GITLAB_TOKEN" \
  --data '{
    "personal_access_token": "ghp_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "repo_id": "523303538",
    "target_namespace": "YOUR_GITLAB_USERNAME",
    "new_name": "xss-on-label-color",
    "github_hostname": "http://YOUR_IP:YOUR_PORT"
}'
```

For example:

```bash
curl -kv "https://gitlab.com/api/v4/import/github" \
  --request POST \
  --header "content-type: application/json" \
  --header "PRIVATE-TOKEN: AAAAAAAAAAAAAYYYYabc" \
  --data '{
    "personal_access_token": "ghp_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "repo_id": "523303538",
    "target_namespace": "yvvdwf",
    "new_name": "xss-on-label-color",
    "github_hostname": "http://51.75.74.52:80"
}'
```

After finishing, you can view the list of the labels of the imported project. You should see an popup created by this js `alert(document.domain)`

An example is available here (private project): https://gitlab.com/yvvdwf/xss-on-label-color/-/labels


# Impact

Stored-XSS with CSP-bypass allows attackers to execute arbitrary actions on behalf of victims at the client side.

## Impact

Stored-XSS with CSP-bypass allows attackers to execute arbitrary actions on behalf of victims at the client side.

</details>

---
*Analysed by Claude on 2026-05-12*
