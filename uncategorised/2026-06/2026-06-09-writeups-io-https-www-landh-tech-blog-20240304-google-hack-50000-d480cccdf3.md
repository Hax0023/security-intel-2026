# IDOR Vulnerability in Google Bard/Gemini Vision Feature - $50,000 Bounty

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** High
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Unauthorized Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered an IDOR vulnerability in Google Bard's Vision feature that allowed attackers to access and describe other users' images without authorization. By manipulating file paths in API requests, an attacker could substitute another user's image path with their own request, causing the AI to process and describe arbitrary images belonging to other users. This vulnerability exposed sensitive user-uploaded content to unauthorized access.

## Attack scenario (step by step)
1. Attacker User A uploads an image to Google Bard's Vision feature via the web interface while intercepting traffic with a proxy tool
2. Attacker extracts the POST request to /BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate and identifies the file path parameter in the request body (e.g., /contrib_service/ttl_1d/1689251070jtdc4jkzne6a5yaj4n7m)
3. Attacker obtains another user's (User B) image file path through enumeration, guessing, or other reconnaissance techniques
4. Attacker crafts a new request with User B's image path but submits it with their own credentials, causing the API to process User B's image
5. The Bard AI processes and returns a detailed description of User B's private image without any permission verification
6. Attacker gains unauthorized access to sensitive information contained in other users' uploaded images

## Root cause
The application failed to implement proper authorization checks on the file path parameter before passing it to the Vision AI processing function. The API trusted the file path provided by the client without verifying ownership or access permissions, allowing path substitution attacks. Direct object references (file paths) were exposed and not properly protected with access control lists.

## Attacker mindset
A collaborative red teaming approach where the attacker identifies that AI features represent a new attack surface with potentially overlooked security controls. The attacker recognizes that developers building AI integrations may focus on functionality over security fundamentals like access control, especially in emerging technology areas. The use of request interception and parameter manipulation is a standard technique applied to a new domain.

## Defensive takeaways
- Implement strict authorization checks before processing user-supplied object references; verify user owns/has permission to access the resource
- Use indirect object references (tokens/UUIDs) instead of exposing direct file paths or internal identifiers to clients
- Apply the principle of least privilege - ensure each API endpoint validates that the authenticated user has explicit permission for the requested resource
- Conduct security-focused code reviews for new AI/LLM feature integrations, as teams may overlook basic security principles when focused on novel functionality
- Test access control across all parameters, not just obvious user IDs - file paths, object keys, and identifiers are equally important
- Implement comprehensive logging and monitoring for unauthorized access attempts and cross-user resource requests

## Variant hunting
Similar IDOR patterns likely exist in other Google AI features introduced around the same timeframe. Test all user-uploaded content processing features (images, documents, audio) for path traversal or direct object reference vulnerabilities. Check file storage, cache mechanisms, and temporary file handling in LLM chat features. Look for enumerable patterns in temporary file paths and TTL-based storage identifiers. Test vision/image processing in competing LLM products (OpenAI, Claude, Microsoft) for identical vulnerability classes.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate External Targets
- T1087 - Account Discovery
- T1566 - Phishing

## Notes
This finding was part of Google's exclusive LLM bugSWAT event held during Defcon in Las Vegas, indicating Google's proactive approach to AI security testing. The vulnerability demonstrates that as companies rapidly deploy AI features, fundamental security controls like access checks are frequently overlooked. The collaborative nature of the research (three researchers) highlights the value of diverse perspectives in security testing. The writeup emphasizes that new technology domains (LLMs/AI) create fresh attack surfaces where standard security principles must be reapplied. The $50,000 bounty reflects the severity and scope of unauthorized access to user data.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
