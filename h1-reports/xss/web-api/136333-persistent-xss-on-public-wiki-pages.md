# Persistent XSS on public wiki pages

## Metadata
- **Source:** HackerOne
- **Report:** 136333 | https://hackerone.com/reports/136333
- **Submitted:** 2016-05-05
- **Reporter:** jobert
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
# Details
There's a persistent cross-site scripting (XSS) vulnerability in the wiki pages. This can lead to an account take over via the leaked API token.

# Proof of concept
As an attacker, create a new public repository. Make sure you have a client that is allowed to push to that repository. For this PoC, lets say the repository is located at `git@gitlab.com/dummy/test.git`. On the client, execu

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

# Details
There's a persistent cross-site scripting (XSS) vulnerability in the wiki pages. This can lead to an account take over via the leaked API token.

# Proof of concept
As an attacker, create a new public repository. Make sure you have a client that is allowed to push to that repository. For this PoC, lets say the repository is located at `git@gitlab.com/dummy/test.git`. On the client, execute the following commands:

git clone git@gitlab.com/dummy/test.git
cd test
echo "<script>alert('Hello world!');</script>" > index.html
git add index.html
git commit -m "This message is super important"
git push

Now go to https://gitlab.com/dummy/test/wikis/index.html. As you will see, this executes the JavaScript that is stored in the file.

{F91538}

# Impact
GitLab doesn't have a content security policy, which means that clients allow inline Javascript to be executed. This gives access to the current user its API token. The API token can be used to access the user its projects, do actions as the user, give access to potential confidential information, etc.

</details>

---
*Analysed by Claude on 2026-05-24*
