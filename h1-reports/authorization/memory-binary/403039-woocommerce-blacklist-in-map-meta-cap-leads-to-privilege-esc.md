# WooCommerce Shop Manager Privilege Escalation via Unrestricted User Role Assignment

## Metadata
- **Source:** HackerOne
- **Report:** 403039 | https://hackerone.com/reports/403039
- **Submitted:** 2018-08-30
- **Reporter:** simonscannell
- **Program:** WooCommerce
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Privilege Escalation, Insufficient Access Control, Blacklist-based Authorization, Indirect Stored XSS
- **CVEs:** None
- **Category:** memory-binary

## Summary
WooCommerce Shop Manager role is granted edit_users capability but implements insufficient blacklist-based restrictions in map_meta_cap filter. A Shop Manager can assign any non-admin role to users, including roles with dangerous capabilities like unfiltered_html, enabling privilege escalation to Administrator through intermediate roles.

## Attack scenario
1. Attacker compromises or is assigned a Shop Manager account in WooCommerce
2. Attacker identifies a target user (customer/subscriber) and changes their role to Editor
3. Attacker resets the target user's password to gain access
4. Attacker logs in as the newly promoted Editor user
5. Attacker creates a post with JavaScript payload (unfiltered_html capability allows this)
6. Attacker or Admin views post, Stored XSS executes, leading to full administrative compromise

## Root cause
WooCommerce uses a blacklist approach in wc_modify_map_meta_cap that only blocks assignment of 'administrator' role. It fails to whitelist allowed roles or prevent assignment of other privileged roles (Editor, Author, etc.) that possess dangerous capabilities like unfiltered_html.

## Attacker mindset
An attacker with Shop Manager access seeks privilege escalation by exploiting the overly permissive role assignment functionality. Rather than directly escalating to Admin (which is blocked), the attacker takes a lateral approach by promoting a user to Editor role, which grants capability to post unfiltered HTML/JavaScript, enabling Stored XSS that can compromise administrative accounts.

## Defensive takeaways
- Use whitelist-based authorization instead of blacklist-based approaches for sensitive operations like role assignment
- Implement granular capability restrictions: Shop Managers should only assign roles explicitly permitted by policy
- Create a custom 'shop_manager_assignable_roles' whitelist containing only essential roles (e.g., shop_customer, shop_vendor if needed)
- Audit all roles for dangerous capabilities (unfiltered_html, manage_options, etc.) and restrict assignment accordingly
- Implement role hierarchy validation: prevent promotion to any role with capabilities exceeding the current user's own capabilities
- Log all user role assignments and privilege changes for audit trail and anomaly detection
- Consider removing edit_users capability from Shop Manager role and use custom user-specific editing functions instead

## Variant hunting
Check other custom roles in WooCommerce (Customer, Vendor) for similar permission escalation paths
Audit third-party plugins that register custom roles and verify if Shop Managers can assign them
Investigate whether Shop Managers can modify user meta fields that affect permissions (user_level, wp_capabilities)
Test if Shop Managers can create new custom roles with assign_product_cat or other shop capabilities
Examine if Shop Managers can leverage user capability modification through user_meta hooks
Check if map_meta_cap filter is properly applied to promote_user capability in all contexts

## MITRE ATT&CK
- T1548.003
- T1190
- T1197
- T1087
- T1078
- T1547

## Notes
This vulnerability demonstrates the dangers of blacklist-based access control. The fix should involve whitelist-based role assignment with explicit enumeration of allowed target roles. The attack chain is particularly effective because it bypasses the admin-role restriction while still achieving full compromise through intermediate privilege escalation and Stored XSS exploitation.

## Full report
<details><summary>Expand</summary>

When the Shopmanager role is defined for the first time, it receives the following WordPress core privileges:

```
	// Shop manager role.
		add_role(
			'shop_manager',
			'Shop manager',
			array(
				'level_9'                => true,
				'level_8'                => true,
				'level_7'                => true,
				'level_6'                => true,
				'level_5'                => true,
				'level_4'                => true,
				'level_3'                => true,
				'level_2'                => true,
				'level_1'                => true,
				'level_0'                => true,
				'read'                   => true,
				'read_private_pages'     => true,
				'read_private_posts'     => true,
				'edit_users'             => true,
				'edit_posts'             => true,
				'edit_pages'             => true,
				'edit_published_posts'   => true,
				'edit_published_pages'   => true,
				'edit_private_pages'     => true,
				'edit_private_posts'     => true,
				'edit_others_posts'      => true,
				'edit_others_pages'      => true,
				'publish_posts'          => true,
				'publish_pages'          => true,
				'delete_posts'           => true,
				'delete_pages'           => true,
				'delete_private_pages'   => true,
				'delete_private_posts'   => true,
				'delete_published_pages' => true,
				'delete_published_posts' => true,
				'delete_others_posts'    => true,
				'delete_others_pages'    => true,
				'manage_categories'      => true,
				'manage_links'           => true,
				'moderate_comments'      => true,
				'upload_files'           => true,
				'export'                 => true,
				'import'                 => true,
				'list_users'             => true,
			)
		);
```

Most interestingly is the following privilege:

```
'edit_users'             => true,
```

With edit_users privileges, Shop managers can by default edit any user and set any user to any user role (including Admin). Since this is obviously not desirable, WordPress added meta capabilities. This allows to restrict Shop managers to not simply assign themselves Admin privileges.

WooCommerce implements these restrictions the following way:

```
/**
 * Modify capabilities to prevent non-admin users editing admin users.
 *
 * $args[0] will be the user being edited in this case.
 *
 * @param  array  $caps    Array of caps.
 * @param  string $cap     Name of the cap we are checking.
 * @param  int    $user_id ID of the user being checked against.
 * @param  array  $args    Arguments.
 * @return array
 */
function wc_modify_map_meta_cap( $caps, $cap, $user_id, $args ) {
	switch ( $cap ) {
		case 'edit_user':
		case 'remove_user':
		case 'promote_user':
		case 'delete_user':
			if ( ! isset( $args[0] ) || $args[0] === $user_id ) {
				break;
			} else {
				if ( user_can( $args[0], 'administrator' ) && ! current_user_can( 'administrator' ) ) {
					$caps[] = 'do_not_allow';
				}
			}
			break;
	}
	return $caps;
}
add_filter( 'map_meta_cap', 'wc_modify_map_meta_cap', 10, 4 );
```

Whenever any capability related to users is in question, WooCommerce disallows it if the target for the modification is an admin. 

However, this "blacklist" kind of approach is insufficient. The consequence is that a Shop manager can modify any user and can assign any user role that is not admin.

This means that if I were to hack a Shopmanager account, who does NOT posses the "unfiltered_html" capability, I can simply assign the user role editor, which does have the ability to post JavaScript code, to a random user or customer, change their password, log in and then get a Stored XSS working and hack the admin.

Also, if there are any other custom user roles registered on a Wordpress installation, I can also assign those to me.

For example, the Plugin https://de.wordpress.org/plugins/backwpup/ registers the user type BackWpUp Admin, a user who can create and download backups of the WordPress installation.


Proof of Concept:

Simply login as a Shop manager, set the user role of a random user (e.g. a customer) to editor, change their password and then log into WordPress as that user. Then create a Post with your JavaScript Payload.

## Impact

Since Stored XSS is a very reliable way to escalate your privileges to Admin and this is occurs in every WooCommerce installation, I marked this as a high impact.

</details>

---
*Analysed by Claude on 2026-05-24*
