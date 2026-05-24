# Reflected Cross-Site Scripting in Serendipity (serendipity.SetCookie)

## Metadata
- **Source:** HackerOne
- **Report:** 373950 | https://hackerone.com/reports/373950
- **Submitted:** 2018-06-29
- **Reporter:** bb9866f3f743d6bf69b6836
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary

The *Smarty* template responsible of creating *JavaScript* snippets assigning cookies to users is during sorting of entries in the administration interface is affected by a reflected cross-site scripting.

## Description

In `templates/2k11/admin/entries.inc.tpl`, the following code is dynamically creating a *JavaScript* snippet consisting of calls to `serendipity.SetCookie()`:

```htm

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

## Summary

The *Smarty* template responsible of creating *JavaScript* snippets assigning cookies to users is during sorting of entries in the administration interface is affected by a reflected cross-site scripting.

## Description

In `templates/2k11/admin/entries.inc.tpl`, the following code is dynamically creating a *JavaScript* snippet consisting of calls to `serendipity.SetCookie()`:

```html
    <script>
        $(document).ready(function() {
    {foreach $filter_import AS $f_import}
        serendipity.SetCookie("entrylist_filter_{$f_import}", "{$get_filter_{$f_import}}" )
    {/foreach}
    {foreach $sort_import AS $s_import}
        serendipity.SetCookie("entrylist_sort_{$s_import}", "{$get_sort_{$s_import}}" )
    {/foreach}
        });
    </script>
```

However, *Smarty* is not aware of the context is is not told to escape it as `javascript` (https://www.smarty.net/docsv2/en/language.modifier.escape) and no prior encoding is performed on data injected in the template (see `include/admin/entries.inc.php:216`):

```php
<?php
// [...]
case 'editSelect':
        $data['switched_output'] = false;
        $filter_import = array('author', 'category', 'isdraft');
        $sort_import   = array('perPage', 'ordermode', 'order');

        foreach($filter_import AS $f_import) {
            serendipity_restoreVar($serendipity['COOKIE']['entrylist_filter_' . $f_import], $serendipity['GET']['filter'][$f_import]);
            $data["get_filter_$f_import"] = $serendipity['GET']['filter'][$f_import];
        }

        foreach($sort_import AS $s_import) {
            serendipity_restoreVar($serendipity['COOKIE']['entrylist_sort_' . $s_import], $serendipity['GET']['sort'][$s_import]);
            $data["get_sort_$s_import"] = $serendipity['GET']['sort'][$s_import];
        }
```

For the record, the function `serendipity_JSsetCookie` is also vulnerable, but it's not in use in this version:
```php
<?php
// [...]
function serendipity_JSsetCookie($name, $value) {
    $name  = serendipity_entities($name);
    $value = urlencode($value);

    echo '<script type="text/javascript">serendipity.SetCookie("' . $name . '", unescape("' . $value . '"))</script>' . "\n";
}
```

## Steps To Reproduce

  1. Access https://blog.fuzzing-project.org/serendipity_admin.php?serendipity[action]=admin&serendipity[adminModule]=entries&serendipity[adminAction]=editSelect&serendipity[filter][author]=1xx");alert(document.domain);// while being authenticated;
  1. Notice the execution of `alert(document.domain)` within the context of  `blog.fuzzing-project.org`.

## Impact

By accessing a link specially crafted by an attacker and exploiting this vulnerability, an authenticated victim could be forced to perform actions on its behalf on the domain blog.fuzzing-project.org. If the victim is authenticated as administrator, it could be used to compromise the website or the underlying server (through the installation of `serendipity_plugin_externalphp`).

</details>

---
*Analysed by Claude on 2026-05-24*
