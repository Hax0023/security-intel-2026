# Information disclosure in mmap module - python 2.7.12

## Metadata
- **Source:** HackerOne
- **Report:** 174632 | https://hackerone.com/reports/174632
- **Submitted:** 2016-10-08
- **Reporter:** aerodudrizzt
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
First thing first, the report was sent to python's security mailing list on the 27.8.16 and was fixed by benjamin on the 5.10.16 (rev 144f10202076), and acknowledged be me today (8.10.16).

In a security audit I made to the mmap module in python (2.7.12), I have found a **major information leak** vulnerability. Here are the relevant details:
* mmap module uses size_t pos, size for boundary checks 

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

First thing first, the report was sent to python's security mailing list on the 27.8.16 and was fixed by benjamin on the 5.10.16 (rev 144f10202076), and acknowledged be me today (8.10.16).

In a security audit I made to the mmap module in python (2.7.12), I have found a **major information leak** vulnerability. Here are the relevant details:
* mmap module uses size_t pos, size for boundary checks before read/write access to the mmaped file
* The resize() function, in both windows and linux, updates only the size variable, and **ignores** the pos variable
* resize() that shrinks the mapped file can lead to a situation in which pos > size, thus breaking the code's invariant
* A later call to read() or readline() can leverage this point into reading from a different memory page:
* read():
 * The only check is an assert() that size >= pos
 * Than an int variable is declared and used:
  * n = self->size - self->pos; // n is now negative
  * n is adjusted to be: n = PY_SSIZE_T_MAX;
  * n is now a poor upper bound to the read operation that follows
* readline():
 * no size checks are done, the checks are passed to the memchr() function
 * memchr(start, '\n', self->size - self->pos)
 * memchr() receives size_t as the length parameter, thus making the size bound negligible
 * read will now "steal" data from another page: PyString_FromStringAndSize(start, (eol - start))

The exploitation will only work in case that there is an adjacent memory page, otherwise the read() / memchr() will cause a segfault while reading outside of the process memory mapped pages.

I have exploited the vulnerability and demonstrated it's possible effects on a windows 7 computer. On a linux machine there should be (probably) some small adjustments to the demo script. Attached are the attack script and it's result in a successful attack attempt.

As i mentioned at the beginning, the vulnerability was fixed and acknowledged to block the described attacks.
Eyal.

</details>

---
*Analysed by Claude on 2026-05-24*
