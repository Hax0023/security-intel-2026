# PNG Compression Denial of Service via zTXt Chunk

## Metadata
- **Source:** HackerOne
- **Report:** 454 | https://hackerone.com/reports/454
- **Submitted:** 2013-11-23
- **Reporter:** spipm
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service, Algorithmic Complexity, Resource Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
A maliciously crafted PNG file with a zTXt (compressed text) chunk containing highly compressible data (e.g., repeated zeros) can be crafted to be extremely small (<1MB) while decompressing to gigabytes of data. When image processing services attempt to identify or convert such files, the zlib decompression causes severe resource exhaustion leading to denial of service.

## Attack scenario
1. Attacker crafts a PNG file with a zTXt chunk containing 50MB of zeros or other highly repetitive data
2. The zlib compression algorithm compresses this to approximately 49KB, resulting in a final PNG file under 1MB
3. Attacker uploads the malicious PNG to a service that processes images (e.g., HackerOne using Paperclip/ImageMagick)
4. The service's image identification tool (identify) or conversion tool (convert) attempts to decompress the zTXt chunk
5. Decompression requires massive memory and CPU resources to expand the compressed data
6. Service experiences timeout, resource exhaustion, or crashes, resulting in denial of service for legitimate users

## Root cause
Image processing services do not validate or limit the decompression ratio of PNG ancillary chunks before processing. The zlib library's inflate() function will decompress all data without bounds checking on output size, allowing zip bomb style attacks using legitimate PNG chunks.

## Attacker mindset
An attacker researching image format vulnerabilities systematically tests different image formats (JPEG, GIF, PNG) for similar weaknesses. Upon discovering PNG's zTXt chunk supports arbitrary compression, they exploit zlib's property that highly repetitive data compresses extremely well, creating a compression bomb that bypasses file size checks.

## Defensive takeaways
- Implement decompression size limits before processing PNG ancillary chunks
- Set maximum allowed decompression ratios (e.g., reject if output would exceed 100x input size)
- Validate and sanitize all PNG chunks; consider rejecting or limiting optional ancillary chunks like zTXt
- Use resource limits and timeouts for all image processing operations
- Keep zlib and image processing libraries updated to patch known vulnerabilities
- Monitor for unusual compression ratios or processing times during image handling
- Consider sandboxing image processing in separate processes with strict resource quotas

## Variant hunting
Research other PNG ancillary chunks (iTXt, tEXt, etc.) for similar compression issues. Investigate TIFF, WebP, and other formats supporting optional compressed metadata. Test GIF and JPEG for analogous compression bomb vulnerabilities in their extension blocks.

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
This is a classic compression bomb vulnerability (zip bomb style attack) applied to PNG metadata. The vulnerability exists not in the PNG format itself but in unsafe decompression of untrusted compressed data without size validation. The researcher ethically disclosed by providing proof-of-concept code and offering to continue research on other chunks. Similar vulnerabilities likely exist in other ancillary chunks and other image formats with compression support.

## Full report
<details><summary>Expand</summary>

[ztxt]: http://www.libpng.org/pub/png/spec/1.1/PNG-Chunks.html#C.zTXt "zTXT Documentation"
[tech]: http://www.zlib.net/zlib_tech.html "zlib technical details"
[zlibvuln1]: http://www.kb.cert.org/vuls/id/680620
[zlibvuln2]: http://www.kb.cert.org/vuls/id/238678


PNG compression DoS
---------------------
 Because I did JPEG and GIF I just had to check out the PNG format.

Found
---------------------
A PNG file is composed of multiple chunks.
One of the optional ancillary chunks is called zTXT ([ztxt]).
This chunk allows storage of compressed text data using the zlib library.
From the zlib [tech] details:
"The test case was a 50MB file filled with zeros; it compressed to roughly 49 KB"
I used this to store a huge amount of data in a small PNG (smaller than 1 MB). When sent to HackerOne the service timed out. I think it's because Paperclip tried to `identify` and `convert` my image again.

As a attachment I sent the Python code I made to create the PNG, and the PNG itself. 
Usage: python createpng.py filename

Fixes
---------------------
For an easy fix every PNG file with the string "zTXt" in it should be rejected. Other data chunks may be exploitable, but I haven't looked into them yet. When this bug is fixed I will continue my research.

Theory
---------------------
Make sure your zlib library is updated . Because of old exploits in zlib's inflate() ([zlibvuln1], [zlibvuln2]), attackers might make a PNG that can exploit old machines. 

</details>

---
*Analysed by Claude on 2026-05-24*
