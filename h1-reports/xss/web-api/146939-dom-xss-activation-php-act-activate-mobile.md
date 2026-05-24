# DOM XSS в /activation.php?act=activate_mobile

## Metadata
- **Source:** HackerOne
- **Report:** 146939 | https://hackerone.com/reports/146939
- **Submitted:** 2016-06-24
- **Reporter:** abr1k0s
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Поинтересовался тут функцией showOrderBox в API. Увидел там "Тестовое спецпредложение. Тестовое спецпредложение для разработчиков приложений."
При щелчке по кнопке "перейти в группу" попал на страницу /activation.php?act=activate_mobile&hash=мой_хэш&return=%2Foffersdesk%3Fact%3Dstart_offer%26offer_id%3D1237%26hash%3D17634e2103b0a99782%26test_mode%3D1%26aid%3D4846993%26app_currency%3D0%26from%3

Об

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

Поинтересовался тут функцией showOrderBox в API. Увидел там "Тестовое спецпредложение. Тестовое спецпредложение для разработчиков приложений."
При щелчке по кнопке "перейти в группу" попал на страницу /activation.php?act=activate_mobile&hash=мой_хэш&return=%2Foffersdesk%3Fact%3Dstart_offer%26offer_id%3D1237%26hash%3D17634e2103b0a99782%26test_mode%3D1%26aid%3D4846993%26app_currency%3D0%26from%3

Обратил внимание на параметр return. Увидел, что значение попадает в вывод страницы, предоставляя возможность осуществить xss атаку.

Сформировал следующую ссылку:
/activation.php?act=activate_mobile&hash=мой_хэш&return=javascript:alert(1);//offersdesk%3Fact%3Dstart_offer%26offer_id%3D1237%26hash%3D17634e2103b0a99782%26test_mode%3D1%26aid%3D4846993%26app_currency%3D0%26from%3

Получил alert при вводе в поле ввода правильного кода из смс.

Фрагмент уязвимого кода js: 
    params = {code: code, hash: 'a0096404730f329021'};
    callback = function(t) {
      if (t) {
        cur.phoneValidationMsg(t);
        return stop();
      }
      document.location = winToUtf('javascript:alert(1);//offersdesk?act=start_offer&amp;offer_id=1237&amp;hash=17634e2103b0a99782&amp;aid=4846993&amp;app_currency=0&amp;from=');
    }

</details>

---
*Analysed by Claude on 2026-05-24*
