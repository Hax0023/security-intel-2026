# BAC – Bypass chatbot restrictions via unauthorized mention injection

## Metadata
- **Source:** HackerOne
- **Report:** 3112106 | https://hackerone.com/reports/3112106
- **Submitted:** 2025-04-25
- **Reporter:** yoyomiski
- **Program:** Dust (HackerOne)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Broken Access Control, Authorization Bypass, Insecure Direct Object References (IDOR), Client-side validation bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
A member user can bypass admin-enforced chatbot access restrictions by manually editing API requests to inject unauthorized agent mentions and configuration IDs. This allows unauthorized access to disabled or restricted chatbots like Gemini, completely circumventing permission controls. The vulnerability affects both disabled chatbots and those restricted to specific user groups.

## Attack scenario
1. Admin disables Gemini chatbot or restricts it from member users in the Manage Agents panel
2. Attacker (member user) initiates a normal chat with an authorized agent
3. Attacker intercepts the message edit API request (POST /api/w/[workspaceId]/assistant/conversations/[conversationId]/messages/[messageId]/edit) using Burp Suite
4. Attacker modifies the JSON payload, changing mention field and configurationId to the restricted agent (e.g., 'gemini-pro')
5. Attacker forwards the modified request with unauthorized agent reference
6. Server processes request without validating if user has permission to access the specified agent, allowing chatbot interaction

## Root cause
Server-side authorization validation is missing or insufficient in the message edit endpoint. The application trusts client-supplied configurationId and mention parameters without verifying that the authenticated user has permission to access the requested agent. Authorization checks likely occur only at the UI level, not at the API layer.

## Attacker mindset
An insider or low-privileged user seeking to gain unauthorized access to restricted tools or information available through disabled chatbots. The attacker recognizes that permission controls are enforced at UI/frontend level and exploits the lack of backend validation by directly manipulating API parameters.

## Defensive takeaways
- Implement server-side authorization checks on every API endpoint, validating user permissions for requested resources before processing
- Never rely on client-supplied IDs or configuration references—validate against user's authorized resources on the backend
- Enforce authorization at the API layer, not just the frontend/UI layer
- Implement a permission matrix or access control list (ACL) that is checked before executing any agent-related operations
- Use immutable, server-controlled tokens or session data to determine which agents a user can access
- Add audit logging for all agent access attempts and configuration changes
- Apply principle of least privilege—users should only access explicitly granted agents
- Sanitize and validate all user inputs, particularly mentions and configuration references

## Variant hunting
Check for similar bypass patterns in other message operations (create, delete, forward) by manipulating agent/mention parameters
Test conversation creation endpoints for authorization bypass using unauthorized agent mentions
Examine conversation listing endpoints to see if users can view/access conversations they shouldn't have permission for
Check if similar parameters exist in other workflow-based features (automation, templates) that might bypass restrictions
Test if disabled agents can be accessed through batch operations or bulk message edits
Investigate if agent permissions can be bypassed in API integrations or webhook configurations
Check for similar IDOR patterns in other configurationId-based operations across the application

## MITRE ATT&CK
- T1190
- T1199
- T1548

## Notes
This is a straightforward but critical BAC vulnerability. The attack is trivial to execute and requires no advanced techniques—just HTTP request manipulation. The impact is significant as it completely nullifies admin-enforced restrictions. The writeup clearly demonstrates exploitation with actual request/response examples. The vulnerability likely affects multiple chatbot agents, not just Gemini. The fact that disabled agents remain accessible post-exploitation suggests a fundamental architecture flaw where agent access control is not consistently enforced across all code paths.

## Full report
<details><summary>Expand</summary>

## Summary:
- A member user who is not authorized to use the Gemini chatbot can still send and receive messages from this chatbot by manually editing the request and changing the ```mention``` and ```configurationId```. This bypasses the permission control from the Admin side, leading to abuse of the chatbot beyond the scope of permission.
- Similar to other chatbots, if disabled, members can still use it.

## Steps To Reproduce:
1. Login admin (████████)
2. Go to “Manage Agents”Verify. That the **Gemini agent is disabled** or not available
{F4285482}
3. Now go back to  the member account (█████). we make a new chat . When chatting nomally. we select “which agent would you like to chat with?”
{F4285485}
4. In the step, turn on Burp and capture the request, we capture the request with API:
```POST /api/w/BSsJ1zPUYE/assistant/conversations/PdBk9DSYXA/messages/UyXjPLmW5j/edit```
{F4285487}
5. This request is passed to mention, we change mention and configurationId to gemini's ```gemini-pro``` and forward the request, the result is that we can chat with chatbot ```gemini``` even though the admin does not grant us permission to chat with this chatbot
```{"content":":mention[gemini-pro]{sId=gemini-pro} how are you?","mentions":[{"type":"agent","configurationId":"gemini-pro"}]}```
{F4285490}

Response:
{F4285491}
{F4285493}
{F4285494}

##HTTP header:
```
POST /api/w/BSsJ1zPUYE/assistant/conversations/PdBk9DSYXA/messages/UyXjPLmW5j/edit HTTP/2
Host: eu.dust.tt
Cookie: …
Content-Length: 124
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Chromium";v="135", "Not-A.Brand";v="8"
Content-Type: application/json
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36
Accept: */*
Origin: [https://eu.dust.tt](https://eu.dust.tt/)
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://eu.dust.tt/w/BSsJ1zPUYE/assistant/PdBk9DSYXA
Accept-Encoding: gzip, deflate, br
Priority: u=1, i

{"content":":mention[gemini-pro]{sId=gemini-pro} how are you?","mentions":[{"type":"agent","configurationId":"gemini-pro"}]}
```

## Impact

- Member users are not granted permissions, but can still use Gemini chatbot by editing requests → Clear violation of authorization policy

</details>

---
*Analysed by Claude on 2026-05-24*
