# Stored XSS in Business Account Company Page

## Metadata
- **Source:** HackerOne
- **Report:** 771882 | https://hackerone.com/reports/771882
- **Submitted:** 2020-01-10
- **Reporter:** konqi
- **Program:** drive2.ru
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS) - Stored/Persistent, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Drive2.ru business account company management panel where the company name field is not properly sanitized before being displayed on the company page. An attacker can inject arbitrary JavaScript code (e.g., <svg/onload=confirm(document.domain)>) in the company name field that will automatically execute for all users viewing the company page.

## Attack scenario
1. Attacker registers on drive2.ru and enables a business account
2. Attacker navigates to the company management panel and fills in company registration details
3. Attacker enters malicious XSS payload in the 'Company Name' field (e.g., <svg/onload=confirm(document.domain)>)
4. Attacker saves the company information; the payload is stored in the database without sanitization
5. Any user browsing the attacker's company page triggers automatic execution of the malicious JavaScript
6. Attacker can steal session cookies, redirect users to phishing sites, or perform other malicious actions

## Root cause
The application fails to properly encode or sanitize user input before storing and rendering the company name field in HTML context. The backend accepts the input without validation and the frontend renders it directly in the DOM without HTML entity encoding.

## Attacker mindset
An attacker with a business account can persistently compromise all visitors to their company page by injecting malicious scripts that execute in their browsers. This requires minimal technical knowledge and no victim interaction beyond visiting the company page, making it a highly efficient attack vector.

## Defensive takeaways
- Implement strict input validation on all user-provided data, especially fields displayed publicly
- Apply proper HTML entity encoding to all dynamic content rendered in HTML context (< > & " ')
- Use Content Security Policy (CSP) headers to restrict script execution origins
- Set HttpOnly and Secure flags on all session/authentication cookies to prevent JavaScript access
- Consider using templating engines with auto-escaping enabled by default
- Implement server-side output encoding using established libraries (OWASP ESAPI, similar)
- Perform regular security testing including manual XSS payload testing on all user input fields

## Variant hunting
Test other business account fields (company description, address, contact info) for similar XSS vulnerabilities
Check if business account settings pages have similar encoding issues
Test user profile fields on regular accounts for stored XSS
Verify if other HTML contexts (emails, notifications, reports) properly encode user data
Test for DOM-based XSS in JavaScript that processes company data
Check if file upload features (company logo/images) validate content-type properly

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (via XSS redirect)
- T1539 - Steal Web Session Cookie
- T1005 - Data from Local System

## Notes
This is a classic stored XSS vulnerability with moderate-to-high impact. The attack requires an attacker to have a business account but no special privileges. The persistence nature of the vulnerability means the attacker doesn't need to send malicious links to victims. The report is written in Russian and demonstrates good understanding of XSS attack mechanics and mitigation strategies.

## Full report
<details><summary>Expand</summary>

Приложение уязвимо к атакам Типа "Межсайтовое выполнение сценариев". Тип XSS - Хранимый (Persistent). Для воспроизведения атаки нужно зарегистрироваться на сайте drive2.ru и подключить бизнес-аккаунт. После чего переходим в панель управления компанией и заполняем все необходимые поля для успешной регистрации на сайте. Нам интересует поле "Название компании" которое и выводится на сайте без необходимой фильтрации. Заполняем форму компании, а в поле "Название компании" пишем наш payload, например:
```html
<svg/onload=confirm(document.domain)>
```
После успешного сохранения данных переходим на страницу компании и наш JavaScript автоматически выполняется.
{F680923}
{F680924}

## Impact

Уязвимость недостаточной фильтрация данных, которые попадают в контекст HTML можно использовать по разному, от банального фишинга  до проведения атаки XSS. В нашем случай XSS хранимый, что делает атаку более опасным, так как нет необходимости отправлять жертве ссылку которая содержит вредоносный код. При браузинге страницы компании XSS payload выполнится автоматически. С помощью XSS атакующий может красть пользовательские куки, которые не защищены флагом "httpOnly". Помимо этого можно выполнить редирект на вредоносные сайты и так далее. Для защиты от подобных уязвимостей рекомендую тщательно проверять данные которые попадают в контекст HTML. Спецсимволы которые могут быть использованы для проведения атаки XSS/Content Injection должны быть сконвертированы в сущности HTML. Рекомендуется использовать флаги "secure" и "httpOnly" для сессионных/авторизационных кук.

</details>

---
*Analysed by Claude on 2026-05-12*
