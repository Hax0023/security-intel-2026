# HTML injection in API response including request url

## Metadata
- **Source:** HackerOne
- **Report:** 1719588 | https://hackerone.com/reports/1719588
- **Submitted:** 2022-10-02
- **Reporter:** prilvesh
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Remote File Inclusion
- **CVEs:** None
- **Category:** uncategorised

## Summary
Hi  Reddit , 
I found a way to  distribute, persist &   store  Illegal images    such as child porn , beheadings  on reddit and in plain sight  .
I can also store & distribute xml ,json   data eg illegal links .
I can also store & communicate illegal instructions  aka terrorist messages  in  html  and  plain text.
This hack  also bypasses all security related to detecting illegal messages & pictur

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

Hi  Reddit , 
I found a way to  distribute, persist &   store  Illegal images    such as child porn , beheadings  on reddit and in plain sight  .
I can also store & distribute xml ,json   data eg illegal links .
I can also store & communicate illegal instructions  aka terrorist messages  in  html  and  plain text.
This hack  also bypasses all security related to detecting illegal messages & pictures on reddit


## Impact:
Many possible impacts :
Criminals  could trade child porn ,beheading and other illegal  images on reddit  without detection .
Criminals & Terrorist groups could  distribute illegal  bombing & attack messages  
Criminals could store JavaScript code  
User will not be presented with Warning that you are navigating away from Reddit.com 
Criminals could  pretend to be Legitimate  Reddit employees and trick  reddit users into  navigating to & executing the code simply by right click Go to in there browser as  a result Criminals could  exploit reddit users &  steal there cookies and   infect them with  viruses etc once they execute the  stored code . 
All of the above would by pass Reedits automated  systems .
To execute this proof of concepts please Login to reddit as a user than navigate to the  url.


There are 3 classes 
1) Storage , Persistence by criminals
2) Retrieval , By criminals
3)Executions -involuntary by unsuspecting reddit users.
The data  retrieval can be voluntary eg criminal networks  doing scheduled drop offs and pick ups , or hackers deliberately persisting malicious code that infects or spies on involuntary curious users   landing form hrefs and following instructions but  instead  getting pawned  due to executing the JavaScript.


##PROOF OF Distributing child porn  
You will see BART SIMPSON image as an example but  its clear that he  API  isn't going to run any sort of Image recognition validation or neural net on  this API  input. The below demonstrates  misusing the  reditt.com  api  to store  illegal images
It also demonstrates criminals can than access and trade illegal  like child porn images in plain site on reddit. 


<code>
https://s.reddit.com/REDIT.EXPERIMENTAL.FEATURE:Hi.user.You.know.we.got.the.stuff.right.click.and.go.on.data..........data:image/jpeg;base64,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

</details>

---
*Analysed by Claude on 2026-05-24*
