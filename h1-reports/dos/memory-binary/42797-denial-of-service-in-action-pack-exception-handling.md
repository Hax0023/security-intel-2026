# Denial of Service in Action Pack Exception Handling via Deeply Nested Parameters

## Metadata
- **Source:** HackerOne
- **Report:** 42797 | https://hackerone.com/reports/42797
- **Submitted:** 2015-01-07
- **Reporter:** ff7f00
- **Program:** Rails/Ruby on Rails
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Denial of Service (DoS), Resource Exhaustion, Stack Overflow, Exception Handling Flaw
- **CVEs:** None
- **Category:** memory-binary

## Summary
Rails Action Pack fails to properly handle deeply nested query/body parameters, causing a SystemStackError during parameter normalization that triggers recursive exception handling loops. A single maliciously crafted request with hundreds of nested hash levels exhausts server resources, crashing single-threaded servers immediately and degrading multi-worker deployments.

## Attack scenario
1. Attacker crafts HTTP GET request with deeply nested parameters using format: foo[a][a][a]...[a]=bar (repeated 300+ times)
2. Rails Action Pack receives request and begins parsing parameters via normalize_encode_params() in actionpack/lib/action_dispatch/http/parameters.rb
3. Parameter parsing recurses deeply into nested hash structure, exhausting call stack and triggering SystemStackError
4. Exception handler attempts to log the error and normalize parameters again, recursively calling the same vulnerable function
5. Each exception handling attempt causes additional SystemStackErrors, creating exponential resource consumption
6. Server process exhausts memory/stack resources and becomes unresponsive or crashes; concurrent requests amplify impact on multi-worker servers

## Root cause
The normalize_encode_params() method in Action Pack recursively processes nested parameters without depth limits or stack safety checks. When exception handling occurs, the logging code re-normalizes the same problematic parameters, creating a recursive exception loop that rapidly depletes system resources rather than gracefully handling the error.

## Attacker mindset
An attacker with knowledge of Rails internals recognizes that parameter parsing is a universal code path executed before any application logic. By exploiting the unbounded recursion in parameter normalization and the flawed exception handling that re-triggers the vulnerable code path, a single request can reliably crash production servers without requiring application-level authentication or logic exploitation.

## Defensive takeaways
- Implement maximum nesting depth limits for parameter parsing with early rejection of excessively nested structures
- Add stack depth guards or tail-call optimization checks in recursive parameter processing functions
- Separate exception path from normal path: cache problematic parameters to prevent re-normalization during error logging
- Implement rate limiting and request size validation at HTTP layer before parsing
- Use non-recursive algorithms for parameter flattening or implement iterative depth-first traversal with explicit stack management
- Add comprehensive input validation for parameter structure complexity in addition to value validation
- Monitor for repeated SystemStackError exceptions as potential DoS indicator

## Variant hunting
Test other web frameworks (Django, Express, etc.) for similar parameter parsing recursion vulnerabilities
Investigate if XML/JSON body parsing in Action Pack has similar unbounded recursion issues
Check if other Rails features (route matching, middleware processing) have similar exception-handling loops
Test multipart form data parsing with deeply nested file upload parameters
Examine cookie parsing and header processing for similar recursive patterns
Look for similar issues in other Ruby gems that parse user-supplied nested structures

## MITRE ATT&CK
- T1190
- T1499
- T1499.4

## Notes
This vulnerability demonstrates a critical flaw in exception handling architecture: error handlers that re-execute vulnerable code paths can amplify DoS impact exponentially. The issue affects all Rails versions handling the request (4.2.0 confirmed) and impacts both single-threaded (Webrick, Thin) and multi-worker (Unicorn) deployments. The single-request impact on Webrick demonstrates the severity of unbounded recursion in universal code paths. Heroku multi-worker impact required concurrent requests, indicating some resilience from worker isolation but not from single-instance architectures.

## Full report
<details><summary>Expand</summary>

# Severity

Medium

# Impact

Attackers can cause an application to be unreachable, causing a denial of service condition.

# Details

When a Rails application receives a request with either body or query parameters, these parameters are converted to a params hash. Hashes can be passed to the application in the form of user[name]=foo&user[address]=bar. Action Pack will then convert this into a hash in the form of `{ user[:name] => "foo", user[:address] => "bar" }`. By passing a very large nested hash in the form of nested_hash[X1][X2]...[Xn], it is possible to create a denial of service condition in the form of a SystemStackError that is not handled properly. See the Bug Notes section on my attempt to figure out where this is occurring.

This was tested in the latest Rails 4.2.0 release with Ruby versions ruby-1.9.3-p551, 2.1.5p273, and ruby 2.2.0p0.

Production Webrick and single threaded Thin servers can be taken out with a single request. I set Burp Suite to a high number of concurrent requests and was able to get Heroku to produce a generic application unavailable message on a production application I had hosted, so Unicorn will be effected as well with workers constantly dying and being relaunched.

# Bug Notes

It seems that the initial SystemStackError is thrown during normalize_encode_params(params) in actionpack/lib/action_dispatch/http/parameters.rb, Line 47. This method is then called again during the logging/creating of the exception when the logging code attempts to normalize and encode the parameters again. It's possible that a loop is being hit here every time the SystemStackError occurs.

I set a byebug break point in the GET and POST methods located at actionpack/lib/action_dispatch/http/request.rb, line 299, then set 'catch SystemStackError'. The SystemStackError is raised 2 more times before finally running out of resources and hanging the process. The normalize_encode_params is a recursive method that creates a new hash in a block before calling itself so I believe a lot of resources are being allocated for this method when it gets deep into the nested hash.

# Reproduction Steps

For Webrick:

1. rails new dos_test
2. cd dos_test
3. bundle exec rails generate controller welcome index
4. Uncomment the `root 'welcome#index'` line in config/routes.rb
5. SECRET_KEY_BASE='foo' bundle exec rails s -e production
6. Then in a separate window, run the following cURL command:

```
curl -i -s -k  -X 'GET' \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-binary $'foo[a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a][a]=bar' \
'http://localhost:3000/'
```

Note that Webrick will hang and will have to be killed manually. If the Webrick server handles this level of nesting, more nesting levels can be created by adding [a] until the application hangs.

If you have any questions at all or need clarification, I’d be happy to help.

</details>

---
*Analysed by Claude on 2026-05-24*
