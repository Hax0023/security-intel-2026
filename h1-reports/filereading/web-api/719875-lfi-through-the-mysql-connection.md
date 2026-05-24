# Local File Inclusion (LFI) via MySQL LOAD DATA LOCAL INFILE

## Metadata
- **Source:** HackerOne
- **Report:** 719875 | https://hackerone.com/reports/719875
- **Submitted:** 2019-10-22
- **Reporter:** muon4
- **Program:** Infogram
- **Bounty:** Unknown (not specified in report)
- **Severity:** High
- **Vuln:** Local File Inclusion (LFI), Insecure MySQL Client Configuration, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Infogram's MySQL connection feature fails to disable the LOAD DATA LOCAL capability, allowing authenticated attackers to read arbitrary local files from the server. An attacker can craft a malicious SQL query using LOAD DATA LOCAL INFILE to exfiltrate sensitive files like /etc/passwd and /etc/hosts through an attacker-controlled MySQL server.

## Attack scenario
1. Attacker authenticates to Infogram application
2. Attacker navigates to Data section and creates a new MySQL connection
3. Attacker configures the connection with a malicious SQL statement using LOAD DATA LOCAL INFILE pointing to a sensitive file path (e.g., /etc/passwd)
4. Attacker sets up an attacker-controlled MySQL server with minimal table/database structure matching the query
5. Attacker executes the connection test/creation, triggering the MySQL client to initiate connection to attacker's server
6. The MySQL protocol negotiation includes LOAD DATA LOCAL capability enabled (set to 1/true), causing the server to send the requested local file contents to attacker's database

## Root cause
The Infogram application uses a MySQL client library with LOAD DATA LOCAL feature enabled by default. The application does not sanitize or restrict SQL queries provided in the MySQL connection configuration, and critically fails to disable the LOAD DATA LOCAL capability when establishing connections to user-provided MySQL servers.

## Attacker mindset
An authenticated attacker with access to Infogram's data connection features seeks to pivot from application compromise to server file system access. By leveraging the default MySQL client configuration, the attacker exploits a well-known MySQL feature to exfiltrate sensitive server files containing credentials, configuration, and system information without direct file system access.

## Defensive takeaways
- Explicitly disable LOAD DATA LOCAL in MySQL client connection options when establishing connections to user-provided or untrusted MySQL servers
- Implement strict allowlists for file paths in SQL queries and reject any queries containing LOAD DATA, INTO OUTFILE, or similar file I/O operations
- Sanitize and validate all SQL queries before execution, using parameterized queries and prepared statements where possible
- Restrict the MySQL client's file system permissions to only necessary directories, not the entire server
- Implement connection sandboxing or use MySQL proxy layers that can filter dangerous SQL commands
- Apply principle of least privilege to database connection credentials used by the application
- Audit and log all SQL queries executed through the application, particularly those involving file operations

## Variant hunting
Check for similar LOAD DATA LOCAL exploitation in other data connection features (PostgreSQL, MongoDB, etc.)
Investigate whether INTO OUTFILE/DUMPFILE variants are also possible for writing files to attacker-controlled locations
Test if other file-reading SQL functions are available (LOAD_FILE() in MySQL, etc.)
Examine whether the vulnerability affects API-based connections or just UI-based flows
Determine if privilege escalation is possible by reading configuration files containing API keys or database credentials

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel
- T1105 - Ingress Tool Transfer
- T1557 - Man-in-the-Middle

## Notes
The vulnerability is particularly dangerous because it combines authenticated access with a default dangerous feature in MySQL clients. The attacker's use of tcpdump/wireshark to verify file exfiltration demonstrates practical proof-of-concept. The report clearly documents the MySQL protocol-level indication that LOAD DATA LOCAL is enabled (flag set to 1). This is a textbook example of failing to disable dangerous client-side features when connecting to untrusted servers.

## Full report
<details><summary>Expand</summary>

Hello team!

I've found a way to read Infogram's server local files through the MySQL connection.
The problem is that you're using the `LOAD DATA LOCAL` feature with your MySQL client. This how an attacker can easily send server's local files to her/his database.

I've successfully readed the `/etc/passwd` and `/etc/hosts` files from your server.

### Steps to reproduce
- Login 
- Make a new infographic or navigate to the existing one
- Now add new MySQL connection under `data` section
- Set the value of the SQL SELECT statement to the following:

```
LOAD DATA LOCAL INFILE '/etc/passwd'
INTO TABLE asd.asd
FIELDS TERMINATED BY "\n"
```

- Fill other necessary information (IP address, port etc..)
- Now setup/install the "evil" MySQL server with the database/table called `asd` and other needed information. Point your MySQL connection from infogram app to this server.
- Listen network traffic of the "evil" MySQL server. If you are using tcpdump you can do wireshark readable file with this command `tcpdump -s 0 port 3306 -i eth0 -w infogramsteal.pcap`
- Now click `Create` in the infogram app
- Once you get an error message at infogram app stop the tcpdump and open it with wireshark

In wireshark/pcap you can see some main points. First is the **login request** where you can see that `LOAD DATA LOCAL` is set to the value `1` which is basicly same than `true`: 
{F614430}
Also, you can see the **Request Command Unknown** which basicly contains the value of the file `/etc/passwd`:
{F614431}

Disable the `LOAD DATA LOCAL` feature if possible.

If you need any information please let me know.

Cheers!

## Impact

Reading local files from the server

</details>

---
*Analysed by Claude on 2026-05-24*
