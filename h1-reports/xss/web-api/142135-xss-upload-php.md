# XSS in upload.php via Unsafe eval() and Callback Parameter Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 142135 | https://hackerone.com/reports/142135
- **Submitted:** 2016-05-30
- **Reporter:** irek
- **Program:** VK.com (VKontakte)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Code Injection, Unsafe use of eval(), Callback Parameter Manipulation
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in upload.php?act=transport where the 'callback' GET parameter is used to dynamically invoke parent window functions without validation. The vulnerable sendData() function uses eval() to execute server responses, allowing attackers to inject arbitrary JavaScript code by crafting malicious image URLs embedded with JS code and manipulating request parameters.

## Attack scenario
1. Attacker identifies that the 'callback' parameter accepts user input and dynamically calls parent.{callback_value}() without validation
2. Attacker embeds JavaScript code into image files using imagejs library (in GIF, BMP, WebP formats)
3. Attacker crafts a malicious URL using VK's share.php proxy and upload_fails.php to generate valid hashes with role=share parameter
4. Attacker manipulates POST request parameters in the iframe to point to the malicious image URL via the proxy
5. When sendData() executes, it sends XHR request to attacker-controlled endpoint disguised as image upload
6. Server response containing JavaScript code is passed to eval() function, executing arbitrary code in victim's browser context

## Root cause
The application uses eval() to process XMLHttpRequest responses without sanitization. The callback parameter is not validated before being used to call parent window functions. Document.domain is set based on Location header regex without proper origin verification. No validation of image proxy URL destinations.

## Attacker mindset
Researcher found eval() usage suspicious and began analyzing control flow. Recognized that callback parameter could be arbitrary function names. Identified that imagejs allows embedding JS in valid image files. Leveraged VK's own proxy and hash generation mechanisms to bypass security controls. Used parameter manipulation to work around sanitation.

## Defensive takeaways
- Never use eval() on external data or user-controllable server responses
- Implement strict whitelist validation for callback function names
- Use postMessage() API instead of dynamic parent function calls for cross-frame communication
- Validate and sanitize all URL parameters, especially those used in proxies
- Implement Content Security Policy (CSP) with script-src restrictions
- Verify image file integrity and content-type before processing
- Avoid setting document.domain based on regex patterns - use explicit whitelist
- Implement hash/signature verification for sensitive operations like file uploads

## Variant hunting
Look for other endpoints using eval() on XMLHttpRequest responses
Search for other callback/function-name parameters in upload functionality
Test proxy endpoints (share.php, proxy_img) for arbitrary redirect capabilities
Find other places where document.domain is dynamically set
Look for steganographic file embedding techniques in other media types (SVG, PDF, MP4)
Test other image-hosting actions with hash manipulation
Analyze imagejs library for similar injection points in other VK apps

## MITRE ATT&CK
- T1190
- T1566.002
- T1547.010
- T1059.007

## Notes
The writeup appears incomplete (cuts off mid-sentence at 'вып'). The vulnerability cleverly chains multiple VK features: imagejs for code embedding, share.php proxy for serving malicious content, upload_fails.php for hash generation, and parameter dot-notation to bypass sanitation. The researcher notes that the hack wouldn't work on mobile user agents due to missing ajx2q() function, but the core XSS remains viable on desktop. The 'meaningless conditionals' mentioned suggest potential obfuscation or legacy code. This is a sophisticated multi-stage attack requiring knowledge of VK's internal systems.

## Full report
<details><summary>Expand</summary>

Добрый вечер!
Раскрутил интересную xss на upload.php.

**Демо [тут](https://vk.com/app5486273) или [тут](https://irek.wtf/vk.com/transport/).**

Как все было?
Увидел интересный экшн [upload.php?act=transport](https://pu.vk.com/c415824/upload.php?act=transport&to_act=add_doc&hash=8dfd93e60c78ddb4a9cf914c27f7642c&rhash=8171a35e59a63aab65846a26345ddbf6&aid=1&mid=17274528&callback=getUploadSvg), который служит для загрузки нарисованного граффити в документы. Глаз зацепился за вызов функции `eval` в строке 25. Обратите внимание на параметр `callback`, значением которого в данном случае является строка `getUploadSvg`.  На этой странице определена функция `sendData` (строки 11-52) и, помимо этого, выполняется следующий кусок кода (строки 55-64):

    var _ua = navigator.userAgent;
    var locDomain = location.host.toString().match(/[a-zA-Z]+\.[a-zA-Z]+\.?$/)[0];
    if (/opera/i.test(_ua) || !/msie 6/i.test(_ua) || document.domain != locDomain) {
      document.domain = locDomain;
    }
    if (window.parent) {
      parent.getUploadSvg(function(data) {
        sendData('/c415824/upload.php?transport=iframe&act=add_doc&hash=8dfd93e60c78ddb4a9cf914c27f7642c&rhash=8171a35e59a63aab65846a26345ddbf6&aid=1&mid=17274528&pda=', data);
      });
    }

, где есть два условных оператора с бессмысленными условиями 👳🏾. В первом проставляется `document.domain` для кроссдоменного выполнения сценариев, а во втором все самое интересное - вызывается функция родительского окна `parent.getUploadSvg`, где `getUploadSvg` это значение GET-параметра `callback` ~~(как уже было написано выше)~~ и его значение можно менять на любое другое (предположительно подходящее под паттерн `/^[a-zA-Z0-9]*$/`). То есть функции `parent.{значение параметра callback}` передается один аргумент, являющийся анонимной функцией. Эта анонимная функция принимает один параметр `data`, а в её теле происходит вызов функции `sendData` (строка 62):

    sendData('/c415824/upload.php?transport=iframe&act=add_doc&hash=8dfd93e60c78ddb4a9cf914c27f7642c&rhash=8171a35e59a63aab65846a26345ddbf6&aid=1&mid=17274528&pda=', data);


Тут первый аргумент это строка, содержащая относительный URL, в который попадают почти все исходные GET-параметры, проходя перед выводом санитизацию. Второй параметр это переменная `data`, о которой писал чуть выше.

Разберем саму функцию `sendData`. Она принимает три аргумента `url`, `file` и `sequel `. По понятным причинам, нам интересны только первые два. Стоит обратить внимание на строку 16

    var plain = /iphone|ipod|ipad|opera mini|opera mobi/i.test(navigator.userAgent);

и блок кода условного оператора в строках 29-41

    if (plain) {
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

      if (dataUrl.length > 15000) {
        fdataUrl = dataUrl.substr(0, 15000);
        ndataUrl = dataUrl.substr(15000);
        dataUrl = fdataUrl;
        more = 1;
      }

      xhr.send(ajx2q({Data: dataUrl, more: more, sequel: sequel || 0}));
    } else {

Остановились мы на этом потому, что в строке 40 происходит вызов функции `ajx2q `, которая не определена и, поэтому, сохранение граффити в документы не работает для юзерагентов удовлетворяющих регулярному выражению `/iphone|ipod|ipad|opera mini|opera mobi/i`. Следовательно и хак не будет работать. Если не обращать внимания на сей досадный факт, то можно заметить, что в функции `sendData` с помощью `XMLHttpRequest` происходит POST-запрос на URL, параметрами которого мы можем манипулировать. В случае успеха, результат запроса передается в функцию `eval`, что круто если каким-то образом заставить сервер выдавать нужный нам ответ на этот POST-запрос. Поскольку мы можем манипулировать параметрами URL, на который будет произведен запрос, я начал думать над тем как заставить сервер отвечать на запрос моим js-кодом. Тут я вспомнил о том, что существуют такие штуки как [imagejs](http://jklmnn.de/imagejs/) и [share.php](https://vk.com/share.php?url=https://irek.wtf/shareit.php). Первое нам интересно потому что позволяет встроить js-код прямо файлы картинок (Gif, Bitmap, WebP, Netbpm Anymap, Progressive Graphics) и файлы будут валидны. А в share.php как-раз есть проксирование изображений ([пример](https://pu.vk.com/c539421/upload.php?act=proxy_img&url=https%3A%2F%2Firek.wtf%2Fpikachu.gif&hash=f5b4a65619ba2c63a7bb018db018bfce)). Тут я столкнулся с другой проблемой - хэши. Это была боль, но методом тыка я понял, что если передать скрипту `upload_fails.php` все необходимые параметры и добавить к ним `role=share`, то можно получить необходимые валидные хэши, используя которые можно скрафтить конечный URL. На этом этапе использовалась особенность санитизации переданных параметров (при изучении демо обратите внимание на точки в названиях параметров, они там не случайно). Осталось разобраться с последней проблемой. Заключается она в том, что `sendData` просто так не вызывается. Надо найти такую js-функцию, для которой выполняются следующие условия:

* название функции должно содержать только те символы, которые можно передать через GET-параметр `callback` и функция должна быть глобальной;
* функция должна принимать в качестве аргумента другую callback-функцию и вызвать её передавая в качестве аргумента какой-нибудь объект.

Немного `for (... in window)` и такая функция была найдена - `requestAnimationFrame` ([документация](https://developer.mozilla.org/ru/docs/DOM/window.requestAnimationFrame)).

Далее реализовал демо, которое можно посмотреть [тут](https://vk.com/app5486273) или [тут](https://irek.wtf/vk.com/transport/). Выполняется `alert(document.cookie);`.

Таким образом, получили xss для браузеров, строка user-agent которых не попадают под паттерн `/iphone|ipod|ipad|opera mini|opera mobi/i` и в которых имплементирована функция `requestAnimationFrame ` (или с вендорными префиксами `mozRequestAnimationFrame`, `webkitRequestAnimationFrame`, `msRequestAnimationFrame`).

</details>

---
*Analysed by Claude on 2026-05-12*
