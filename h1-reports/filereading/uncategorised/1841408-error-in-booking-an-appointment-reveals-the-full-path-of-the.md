# Path Disclosure via Error Message in Calendar Appointment Booking

## Metadata
- **Source:** HackerOne
- **Report:** 1841408 | https://hackerone.com/reports/1841408
- **Submitted:** 2023-01-20
- **Reporter:** themarkib0x0
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Improper Error Handling
- **CVEs:** CVE-2023-33183
- **Category:** uncategorised

## Summary
When SMTP is misconfigured or unavailable, the calendar appointment booking endpoint returns a 500 error with verbose stack traces exposing the full server filesystem path including Nextcloud installation directory. An unauthenticated attacker can trigger this error by attempting to book an appointment, revealing sensitive path information such as `/var/snap/nextcloud/33060/nextcloud/` that could aid further reconnaissance.

## Attack scenario
1. Attacker navigates to a target Nextcloud instance and locates a public appointment booking calendar
2. Attacker submits a POST request to the `/index.php/apps/calendar/appointment/{id}/book` endpoint with valid appointment data
3. The server attempts to send a confirmation email via SMTP
4. SMTP service is unavailable or misconfigured, causing a Swift_TransportException
5. Application fails to catch or properly sanitize the exception before returning it in the JSON response
6. Attacker receives detailed stack trace with complete file paths, revealing installation structure and directory layout

## Root cause
The BookingService.php and BookingController.php do not properly handle SMTP exceptions. When email sending fails, the raw exception stack trace is serialized into the JSON response without sanitization. The error handling middleware or controller should catch these exceptions and return generic error messages to clients while logging detailed errors server-side only.

## Attacker mindset
An attacker would use this path disclosure for reconnaissance, mapping the exact Nextcloud version, installation location, and directory structure. This information could be leveraged to identify other vulnerabilities, plan targeted attacks, or locate configuration files. The attacker recognizes that public appointment booking features may not require authentication, making this a low-effort information gathering vector.

## Defensive takeaways
- Implement exception handling that catches service exceptions and returns generic error messages to clients
- Never expose full file paths or stack traces in API responses, regardless of error type
- Log detailed error information server-side only for debugging purposes
- Configure SMTP properly to prevent connection failures, or gracefully degrade when email service is unavailable
- Use centralized error response handlers to sanitize all error messages before they reach the API consumer
- Validate that public endpoints (like appointment booking) don't leak internal system information
- Implement input validation and SMTP connection testing before attempting to send emails

## Variant hunting
Search for other endpoints that trigger email sending (password reset, notifications, invitations)
Test other error conditions in Calendar app (invalid appointment IDs, permission issues, database errors)
Check other Nextcloud apps with email functionality (Mail, Notifications, Contacts) for similar issues
Look for verbose error responses in other POST/PUT operations that interact with external services
Test with intentionally malformed SMTP configurations to trigger various exception types
Examine other appointment-related endpoints for information disclosure

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1592 - Gather Victim Host Information
- T1526 - Exposure of Sensitive Information to an Unauthorized Actor

## Notes
This vulnerability requires minimal privileges (unauthenticated access to public calendar) but has limited impact as it only reveals server paths and does not enable direct exploitation. However, in defense-in-depth strategies, information disclosure should be taken seriously as it aids attackers in reconnaissance. The issue is particularly concerning on shared hosting or containerized environments where path information might reveal sensitive deployment details. The snap installation path `/var/snap/nextcloud/` suggests this was discovered on a snap-deployed Nextcloud instance.

## Full report
<details><summary>Expand</summary>

I figured out that when there is configuration of smtp then the user can reveal the full path of the website when booking an appointment.

## Steps To Reproduce:

1. Go to calendar and create and appointment.
2. Now visit that appointment with burp proxy on.
3. Select time and try to book the appointment.
4. Following request will be observed
```
POST /index.php/apps/calendar/appointment/9/book HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json
requesttoken: <token>
Content-Length: 138
Origin: http://129.146.173.97
DNT: 1
Connection: close
Cookie:<any valid-cookie>

{"start":1674205200,"end":1674205500,"displayName":"attackerbikram","email":"ohp@gmail.com","description":"","timeZone":"UTC"}
```
5. We will get following response
```
HTTP/1.1 500 Internal Server Error
Date: Fri, 20 Jan 2023 03:25:36 GMT
Server: Apache
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Pragma: no-cache
Cache-Control: no-cache, no-store, must-revalidate
X-Request-Id: lETN8J5NgoiwfMPABX3g
x-calendar-response: true
Content-Security-Policy: default-src 'none';base-uri 'none';manifest-src 'self';frame-ancestors 'none'
Feature-Policy: autoplay 'none';camera 'none';fullscreen 'none';geolocation 'none';microphone 'none';payment 'none'
X-Robots-Tag: none
Referrer-Policy: no-referrer
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-Permitted-Cross-Domain-Policies: none
X-XSS-Protection: 1; mode=block
Content-Length: 4472
Connection: close
Content-Type: application/json; charset=utf-8

{"status":"error","message":"Could not send mail: Connection could not be established with host 127.0.0.1 :stream_socket_client(): Unable to connect to 127.0.0.1:25 (Connection refused)","data":{"type":"OCA\\Calendar\\Exception\\ServiceException","message":"Could not send mail: Connection could not be established with host 127.0.0.1 :stream_socket_client(): Unable to connect to 127.0.0.1:25 (Connection refused)","code":0,"trace":[{"file":"\/var\/snap\/nextcloud\/33060\/nextcloud\/extra-apps\/calendar\/lib\/Service\/Appointments\/BookingService.php","line":159,"function":"sendConfirmationEmail","class":"OCA\\Calendar\\Service\\Appointments\\MailService"},{"file":"\/var\/snap\/nextcloud\/33060\/nextcloud\/extra-apps\/calendar\/lib\/Controller\/BookingController.php","line":185,"function":"book","class":"OCA\\Calendar\\Service\\Appointments\\BookingService"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/lib\/private\/AppFramework\/Http\/Dispatcher.php","line":225,"function":"bookSlot","class":"OCA\\Calendar\\Controller\\BookingController"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/lib\/private\/AppFramework\/Http\/Dispatcher.php","line":133,"function":"executeController","class":"OC\\AppFramework\\Http\\Dispatcher"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/lib\/private\/AppFramework\/App.php","line":172,"function":"dispatch","class":"OC\\AppFramework\\Http\\Dispatcher"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/lib\/private\/Route\/Router.php","line":298,"function":"main","class":"OC\\AppFramework\\App"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/lib\/base.php","line":1047,"function":"match","class":"OC\\Route\\Router"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/index.php","line":36,"function":"handleRequest","class":"OC"}],"previous":{"type":"Swift_TransportException","message":"Connection could not be established with host 127.0.0.1 :stream_socket_client(): Unable to connect to 127.0.0.1:25 (Connection refused)","code":0,"trace":[{"function":"{closure}","class":"Swift_Transport_StreamBuffer"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/3rdparty\/swiftmailer\/swiftmailer\/lib\/classes\/Swift\/Transport\/StreamBuffer.php","line":264,"function":"stream_socket_client"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/3rdparty\/swiftmailer\/swiftmailer\/lib\/classes\/Swift\/Transport\/StreamBuffer.php","line":58,"function":"establishSocketConnection","class":"Swift_Transport_StreamBuffer"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/3rdparty\/swiftmailer\/swiftmailer\/lib\/classes\/Swift\/Transport\/AbstractSmtpTransport.php","line":143,"function":"initialize","class":"Swift_Transport_StreamBuffer"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/3rdparty\/swiftmailer\/swiftmailer\/lib\/classes\/Swift\/Mailer.php","line":65,"function":"start","class":"Swift_Transport_AbstractSmtpTransport"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/lib\/private\/Mail\/Mailer.php","line":191,"function":"send","class":"Swift_Mailer"},{"file":"\/var\/snap\/nextcloud\/33060\/nextcloud\/extra-apps\/calendar\/lib\/Service\/Appointments\/MailService.php","line":138,"function":"send","class":"OC\\Mail\\Mailer"},{"file":"\/var\/snap\/nextcloud\/33060\/nextcloud\/extra-apps\/calendar\/lib\/Service\/Appointments\/BookingService.php","line":159,"function":"sendConfirmationEmail","class":"OCA\\Calendar\\Service\\Appointments\\MailService"},{"file":"\/var\/snap\/nextcloud\/33060\/nextcloud\/extra-apps\/calendar\/lib\/Controller\/BookingController.php","line":185,"function":"book","class":"OCA\\Calendar\\Service\\Appointments\\BookingService"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/lib\/private\/AppFramework\/Http\/Dispatcher.php","line":225,"function":"bookSlot","class":"OCA\\Calendar\\Controller\\BookingController"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/lib\/private\/AppFramework\/Http\/Dispatcher.php","line":133,"function":"executeController","class":"OC\\AppFramework\\Http\\Dispatcher"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/lib\/private\/AppFramework\/App.php","line":172,"function":"dispatch","class":"OC\\AppFramework\\Http\\Dispatcher"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/lib\/private\/Route\/Router.php","line":298,"function":"main","class":"OC\\AppFramework\\App"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/lib\/base.php","line":1047,"function":"match","class":"OC\\Route\\Router"},{"file":"\/snap\/nextcloud\/33060\/htdocs\/index.php","line":36,"function":"handleRequest","class":"OC"}],"previous":null}},"code":0

```

## Impact

Some internal paths of the website are disclosed.

</details>

---
*Analysed by Claude on 2026-05-24*
