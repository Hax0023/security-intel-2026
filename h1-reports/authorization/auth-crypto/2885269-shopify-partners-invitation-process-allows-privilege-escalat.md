# Shopify Partners Invitation Process Allows Privilege Escalation Without Email Verification

## Metadata
- **Source:** HackerOne
- **Report:** 2885269 | https://hackerone.com/reports/2885269
- **Submitted:** 2024-12-06
- **Reporter:** mr_asg
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Authentication, Privilege Escalation, Insufficient Email Verification, Account Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Shopify removed email verification requirements from its Partners invitation process, allowing attackers to create accounts using target employee email addresses and accept pending invitations to escalate privileges to Owner. An authenticated low-privilege member can exploit this to escalate to Owner by harvesting invited owner emails and accepting their invitations without verification.

## Attack scenario
1. Attacker gains low-privilege member access to target Shopify Partners account (via social engineering, credential compromise, or legitimate onboarding)
2. Attacker views the email list of invited owners/members within the Partners dashboard
3. Attacker creates a new Shopify account using harvested victim email address (no verification required)
4. Attacker accepts the pending invitation for that email address using the attacker-controlled account
5. Attacker is now promoted to Owner/elevated privilege level within the Partners account
6. Attacker gains full control over sensitive partner data, shop integrations, and billing information

## Root cause
Recent change in Shopify's invitation workflow removed email verification step that previously ensured only legitimate email owners could accept invitations. The system trusts that whoever creates an account with a given email can accept invitations for that email without confirming ownership.

## Attacker mindset
Opportunistic insider or external actor targeting high-value SaaS platforms. Initial compromise via low-privilege access (contractor, vendor, social engineering) or public employee email lists, then lateral movement to admin access. Focus on account takeover to gain control over victim organization's partner ecosystem, integrations, and financial data.

## Defensive takeaways
- Reintroduce email verification (click confirmation link sent to email) for all invitation acceptance workflows
- Implement time-limited invitation tokens that expire after 7-14 days
- Require MFA for invitation acceptance, especially for elevated roles
- Add audit logging for all invitation acceptance and privilege escalation events
- Implement email ownership verification when creating accounts with emails that match pending invitations
- Restrict visibility of invited member email lists to necessary parties only
- Add rate limiting on invitation acceptance to detect bulk exploitation
- Implement step-up authentication for accepting Owner-level invitations

## Variant hunting
Check if other Shopify invitation flows (shop staff invites, app partner programs) have similar verification gaps
Investigate if email verification removal applies to other account types or permission transfers
Test if invitation tokens can be reused across accounts or if they validate email ownership
Examine if similar patterns exist in other Shopify account management features (team transfers, billing contacts)
Check if invitations sent before the change still require verification (logic inconsistency)
Test automated bulk account creation with common employee email patterns targeting organizations

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (removed verification is an exposed weakness)
- T1078 - Valid Accounts (create account with victim email)
- T1548 - Abuse Elevation Control Mechanism (privilege escalation via invitation acceptance)
- T1556 - Modify Authentication Process (circumvent email verification)
- T1199 - Trusted Relationship (exploit partner/member access)
- T1621 - Multi-Factor Authentication Bypass (no MFA on invitations)

## Notes
Critical flaw in a business-critical workflow affecting Shopify's partner ecosystem. The vulnerability chain is elegant: weak authentication (no email verification) + information disclosure (visible email lists) + privilege escalation (invitation acceptance without confirmation). Report shows clear internal vs external attack vectors. Video PoC attached but not visible in text writeup. Typical of auth regression bugs where security controls are removed for convenience without replacement. Likely affected thousands of partner accounts.

## Full report
<details><summary>Expand</summary>

## **Summary**
A recent change in Shopify’s invitation process for joining **Shopify Partners** has introduced a vulnerability that allows unauthorized users to gain access to accounts and escalate their privileges without email verification. This report provides a detailed walkthrough of the vulnerability, exploitation method, and potential impact.

## **Vulnerability Details**

### **Issue:**  
- **Invitations to join Shopify Partners no longer require Invitation email link verification.**

{F3818639}

- An attacker can exploit this by creating an account using email addresses of employees at a target organization. Once an invitation is sent to one of these email addresses, the attacker can accept the invitation and gain unauthorized access to the **Shopify Partners** account.

---

## **Steps to Reproduce**

### **Note:**
==The following steps simulate a scenario where a **low-privilege member** discovers an **invited owner** and uses that email address to escalate privileges. This approach simplifies the reproduction steps instead of demonstrating the creation of multiple accounts with different employee emails and waiting for invitations.==

---

### **Reproduction Steps:**

1. **Have a Shopify Partners Account:**
   - Make sure to have a **Shopify Partners account**.

2. **Invite Members and Owners:**
   - Add a new member (attacker-controlled account) to the **Shopify Partners account**.
   - Add a new **owner** (victim's email) to the account.

3. **Harvest the Invited Owner’s Email:**
   - As a **member**, view the email list of invited owners.

4. **Create a New Account Using the Victim’s Email:**
   - Create a new **Shopify** account using the victim’s email address (no email verification required).

5. **Accept the Invitation Using the New Account:**
   - Log into the new attacker-controlled account using the victim’s email.
   - Accept the invitation to join the **Shopify Partners account**, thereby escalating privileges to **Owner**.

---



## **Suggested Mitigation**

To resolve this issue, the following measures are recommended:
- Reintroduce **email verification** for the invitation process to ensure that only the legitimate user can accept invitations.
- Implement **multi-factor authentication (MFA)** on invitations to enhance security and prevent unauthorized access.
- Ensure that invitations and access rights are validated with more robust security protocols.

---


**Additional Information:**
A Proof of Concept (PoC) video is attached to demonstrate the exploit and the steps taken to successfully escalate privileges using the method described above.

████
---

## **Conclusion**
The vulnerability allows unauthorized users to gain access to sensitive **Shopify Partners accounts** and escalate their privileges without proper verification. Immediate attention is recommended to patch this issue and enhance the security of the platform.

---

Please refer to the attached video for a visual demonstration of the exploit.

## Impact

## **Impact Analysis**

### **Internal Escalation by Low-Privilege Member:**
- A **low-privilege member** can escalate their role by exploiting this vulnerability to accept an invitation sent to a victim's email, gaining unauthorized access to **Owner** privileges.

### **External Attack by Unaffiliated Attacker:**
- An **external attacker** can gather email addresses of employees and create accounts using those emails. The attacker can then monitor for invitations and exploit them to gain unauthorized access to the **Shopify Partners account**.

---

## **Security Impact**

This vulnerability enables unauthorized access to **Shopify Partners accounts** and facilitates privilege escalation without proper verification. This is especially concerning as attackers can leverage publicly available email addresses to target potential victims, leading to unauthorized access and modification of sensitive data.

</details>

---
*Analysed by Claude on 2026-05-24*
