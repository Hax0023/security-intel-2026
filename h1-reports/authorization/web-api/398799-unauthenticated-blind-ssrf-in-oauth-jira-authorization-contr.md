# Unauthenticated Blind SSRF in OAuth Jira Authorization Controller

## Metadata
- **Source:** HackerOne
- **Report:** 398799 | https://hackerone.com/reports/398799
- **Submitted:** 2018-08-24
- **Reporter:** jobert
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Server-Side Request Forgery (SSRF), Host Header Injection, Insufficient Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
The OAuth Jira authorization controller's access_token endpoint is vulnerable to unauthenticated SSRF attacks by accepting arbitrary Host headers without validation. An attacker can craft POST requests to make GitLab perform HTTP/HTTPS requests to internal network resources, potentially reaching services that should not be directly accessible.

## Attack scenario
1. Attacker identifies the vulnerable endpoint at /-/jira/login/oauth/callback on a GitLab instance
2. Attacker crafts a POST request to the access_token endpoint with a malicious Host header pointing to internal IP/hostname (e.g., 162.243.147.21:81)
3. GitLab's oauth_token_url helper constructs a URL using the attacker-controlled Host header
4. Gitlab::HTTP.post executes the request with allow_local_requests: true, sending traffic to the internal target
5. Attacker observes the connection attempt to the internal service, confirming network reachability
6. If the internal service is unauthenticated, attacker may retrieve sensitive information or trigger unintended actions

## Root cause
The access_token method uses the Rails routing helper oauth_token_url which constructs URLs based on the Host header without validation. The Host header is user-controlled and not validated before being used in Gitlab::HTTP.post with allow_local_requests: true, enabling attackers to target arbitrary internal network addresses.

## Attacker mindset
An attacker seeks to probe internal network topology and access services that should be isolated from the internet. By exploiting the blind SSRF, they can discover open ports on internal systems, identify services, and potentially exploit unauthenticated internal endpoints without direct network access.

## Defensive takeaways
- Validate and whitelist the Host header against expected OAuth provider hostnames before using it in URL construction
- Avoid using user-controlled input (including HTTP headers) directly in URL construction for external service calls
- Implement explicit hostname/IP validation before making requests with allow_local_requests: true
- Use hardcoded OAuth token endpoint URLs instead of dynamically constructing them from headers
- Implement rate limiting and logging for OAuth callback endpoints to detect suspicious patterns
- Consider disabling allow_local_requests by default and only enabling for explicitly trusted endpoints
- Add timeouts and request size limits to mitigate Denial of Service impact from hanging connections

## Variant hunting
Check other OAuth provider integrations (GitHub, Google, etc.) for similar Host header usage patterns
Review all endpoints using oauth_*_url helpers to identify similar vulnerabilities
Search for other uses of allow_local_requests: true with user-influenced URL parameters
Identify other Rails routing helpers that derive URLs from request context without validation
Look for SSRF vulnerabilities in webhook handlers, API integrations, and external service connectors
Check for similar issues in other callback endpoints (payments, authentication, webhooks)

## MITRE ATT&CK
- T1190
- T1570
- T1040
- T1589
- T1595

## Notes
This vulnerability is classified as blind SSRF because the attacker cannot directly see the response from internal services - only the limited OAuth token response is returned. However, the ability to make requests to internal systems is confirmed by TCP connection observations. The 60-second timeout creates a denial of service vector. The vulnerability requires no authentication, making it immediately exploitable. The attack complexity is rated High because exploitation requires knowledge of internal network topology or services to be valuable, and responses are limited to JSON token data.

## Full report
<details><summary>Expand</summary>

The `Oauth::Jira::AuthorizationsController#access_token` endpoint is vulnerable to a blind SSRF vulnerability. The vulnerability allows an attacker to make arbitrary HTTP/HTTPS requests inside a GitLab instance's network.

# Proof of concept
To reproduce the vulnerability, follow the steps below.

 - spin up a GitLab EE instance with the latest version (11.2.1-ee)
 - send a `POST` request to the `/-/jira/login/oauth/callback` endpoint, as shown below. In the request, point the `Host` header to the hostname / IP address and port number you want to send the request to:

```
curl -X POST -H 'Host: 162.243.147.21:81' 'https://gitlab.com/-/jira/login/oauth/access_token'
```

 - Observe a `POST` request being sent to `162.243.147.21:81` (in this case HTTPS):

```
Listening on [0.0.0.0] (family 0, port 81)
Connection from [35.231.137.154] port 81 [tcp/*] accepted (family 2, sport 58558)
��ؒ����
��/$����4�i�,�֟J%>�+�/�,�0�����#�'�	��$�(�
�gk39@j28��<=/5�l162.243.147.21

 Connection closed, listening again.
```

# Vulnerable code
The following code can be found in the `Oauth::Jira::AuthorizationsController#access_token` method.

```ruby
def access_token
  auth_params = params
                  .slice(:code, :client_id, :client_secret)
                  .merge(grant_type: 'authorization_code', redirect_uri: oauth_jira_callback_url)

  auth_response = Gitlab::HTTP.post(oauth_token_url, body: auth_params, allow_local_requests: true)
  token_type, scope, token = auth_response['token_type'], auth_response['scope'], auth_response['access_token']

  render text: "access_token=#{token}&scope=#{scope}&token_type=#{token_type}"
end
```

The `GItlab::HTTP.post` call is using the `oauth_token_url` directly. This `_url` Rails routing helper uses the `Host` header to construct the URL it needs to point to. Because every host is accepted in GitLab, the constructed URL can point to an internal system. This is how it's supposed to work. However, the `Host` header should be checked before making the `post` call to avoid an attacker being able to make arbitrary requests.

## Impact

The response of the server is actually interpreted, but this is limited to a JSON response that returns an `access_token`, `scope`, and `token_type`. However, this may have additional consequences in case there are unauthenticated endpoints within the instance's network. This isn't very likely, which is why the attack complexity is set to High. It has a minor impact on Availability, because a thread is blocked on the TCP read timeout, which is set to 60 seconds (`curl -X POST -H 'Host: 162.243.147.21:81'   0.03s user 0.01s system 0% cpu 1:00.76 total`). The integrity impact is currently set at High, but this depends on additional factors, such as what other internal services can be hit. The user does not need to be authenticated to execute the call.

</details>

---
*Analysed by Claude on 2026-05-24*
