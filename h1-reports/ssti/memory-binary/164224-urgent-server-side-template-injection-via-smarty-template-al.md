# Urgent: Server side template injection via Smarty template allows for RCE

## Metadata
- **Source:** HackerOne
- **Report:** 164224 | https://hackerone.com/reports/164224
- **Submitted:** 2016-08-29
- **Reporter:** yaworsk
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Code Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
Hi All,
I've found an issue which has allowed me to execute file_get_contents and extract your /etc/passwd file.

##Description
It appears as though you are using smarty on the backend for templating. Entering a malicious payload as my firstname, lastname and nickname and then inviting a user to join the site results in the code being executed.

To start, I began with the payload {7*7} and receive

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

Hi All,
I've found an issue which has allowed me to execute file_get_contents and extract your /etc/passwd file.

##Description
It appears as though you are using smarty on the backend for templating. Entering a malicious payload as my firstname, lastname and nickname and then inviting a user to join the site results in the code being executed.

To start, I began with the payload {7*7} and received a template error in the email I received {F115749} Recognizing the injection, I then was able to confirm the version of smarty used via {$smarty.version} {F115750} Next I was able to test {php} tags by using ```{php}print "Hello"{/php}``` {F115751}. Finally I used file_get_contents to begin extracting the etc/pass file ```{php}$s = file_get_contents('/etc/passwd',NULL, NULL, 0, 100); var_dump($s);{/php}``` {F115752}

##Steps to reproduce
1. Edit your profile
2. Add the payload ```{php}$s = file_get_contents('/etc/passwd',NULL, NULL, 0, 100); var_dump($s);{/php}``` as your first name, last name and user name (I'm not sure which field is vulnerable)
3. Invite a friend using another email of yours
4. View the email and you will see part of the etc file dumped

##Vulnerability
Since the {php} tags are being parsed and executed, we can execute php functions. In this case, you'll see I'm able to extract the etc/passwd file. While I haven't tried, an attacker can more than likely create a shell on the server.

Please let me know if you have any questions.
Pete

</details>

---
*Analysed by Claude on 2026-05-24*
