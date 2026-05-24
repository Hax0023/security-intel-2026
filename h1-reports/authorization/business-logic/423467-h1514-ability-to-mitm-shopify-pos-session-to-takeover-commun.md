# Man-in-the-Middle Attack on Shopify PoS Customer View WebSocket Communication

## Metadata
- **Source:** HackerOne
- **Report:** 423467 | https://hackerone.com/reports/423467
- **Submitted:** 2018-10-13
- **Reporter:** teknogeek
- **Program:** Shopify
- **Bounty:** Not specified in excerpt
- **Severity:** High
- **Vuln:** Man-in-the-Middle (MiTM), Cryptographic Protocol Weakness, Insufficient Input Validation, Network Service Exposure, Key Exchange Vulnerability
- **CVEs:** None
- **Category:** business-logic

## Summary
Shopify PoS application exposes a WebSocket service listening on all interfaces (0.0.0.0) that can be intercepted via ARP spoofing attacks on local networks. An attacker can manipulate cryptographic messages to inject a malicious public key, allowing them to decrypt and modify communications between merchant and customer terminals, enabling unauthorized transaction manipulation.

## Attack scenario
1. Attacker positions themselves on the same WiFi network as Shopify PoS merchant and customer terminals
2. Attacker performs ARP spoofing to intercept network traffic between merchant PoS device and customer view terminal
3. Attacker captures initial QR code connection string containing initial public key and nonce by sniffing WebSocket handshake
4. Attacker crafts malicious CryptoMessage with CryptoType=ACK and injects their own public key via receiverPublicKey parameter
5. Victim terminal accepts attacker's public key due to insufficient validation in receiveMessageFromServer() method
6. Attacker establishes encrypted communication with victim terminal and modifies transaction amounts or payment details

## Root cause
The ClientCryptoProtocol.receiveMessageFromServer() method blindly accepts and sets a new receiver public key from any incoming message with ACK cryptoType without validating it matches the originally established key from the QR code. The WebSocket server listens on 0.0.0.0 instead of restricting to localhost, and no mutual authentication is performed during key exchange.

## Attacker mindset
A malicious merchant or network attacker seeking to manipulate customer payments by intercepting and modifying transaction communications on shared WiFi networks. The attacker recognizes that the cryptographic implementation lacks proper key pinning and mutual authentication, allowing them to inject their own keys into the protocol.

## Defensive takeaways
- Implement certificate pinning for initial public key established from QR code; reject any key exchange attempts after initial establishment
- Restrict WebSocket service to listen only on localhost (127.0.0.1) unless multi-device communication is absolutely required
- Add mutual authentication with cryptographic signatures to verify both parties' identities before accepting key material
- Implement strict validation of CryptoType enum values and corresponding message structure; use different message types for key exchange vs data transmission
- Employ secure key derivation from the initial QR code seed rather than allowing arbitrary key replacement
- Use TLS/mTLS for all network communication instead of custom WebSocket cryptography
- Implement rate limiting and anomaly detection for repeated key exchange attempts
- Add timestamp/nonce validation to prevent replay attacks during key exchange

## Variant hunting
Search for similar custom cryptographic protocol implementations in Shopify mobile apps that accept dynamic key material from network messages. Examine any QR-code-initiated connection flows that perform subsequent key exchanges without pinning. Test other WebSocket-based services for similar ACK message handling vulnerabilities. Review other Shopify point-of-sale or customer-facing applications for hardcoded listening on 0.0.0.0.

## MITRE ATT&CK
- T1557.002
- T1040
- T1187
- T1555
- T1573.001
- T1056.004

## Notes
This vulnerability combines network-layer (ARP spoofing) and application-layer (cryptographic protocol flaw) attacks. The reporter correctly identified that the defense-in-depth approach was insufficient. The vulnerability is particularly severe in retail environments where PoS devices are frequently on shared commercial WiFi networks. The attacker doesn't need to obtain the initial QR code; they only need to manipulate the key exchange after the customer view has already scanned it.

## Full report
<details><summary>Expand</summary>

Hi @iv-rodriguez,

After a decent amount more digging and research, I must disagree with you on the "expecting to work offline" portion. The code actually specifically listens on all local interfaces (`0.0.0.0`) and the wifi network address is specifically used in the QR code connection string, as shown here in `com.shopify.pos.customerview.server.CustomerViewWebSocketServer::getConnectionString()` in the `com.shopify.pos` app:

```java
private final String getConnectionString() {
    String initialPublicKey = this.crypto.initialPublicKey();
    String initialNonce = this.crypto.initialNonce();
    String currentWifiIpAddress = NetworkUtility.getCurrentWifiIpAddress(PosApplication.Companion.getInstance());
    StringBuilder stringBuilder = new StringBuilder();
    stringBuilder.append(this.protocol);
    stringBuilder.append("://");
    stringBuilder.append(currentWifiIpAddress);
    stringBuilder.append(':');
    stringBuilder.append(this.port);
    stringBuilder.append(';');
    stringBuilder.append(initialPublicKey);
    stringBuilder.append(';');
    stringBuilder.append(initialNonce);
    stringBuilder.append(';');
    PayloadManager payloadManager = this.payloadManager;
    if (payloadManager == null) {
        Intrinsics.throwUninitializedPropertyAccessException("payloadManager");
    }
    stringBuilder.append(payloadManager.getSchemaVersion());
    return stringBuilder.toString();
}
```
This can also be seen from netstat on the device:

```
vbox86p:/ # netstat -an | egrep 'LISTEN[^I]'
tcp        0      0 0.0.0.0:24800           0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:24801         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:27042         0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:22468           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:24810           0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:24811         0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:6379            0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:5037          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN
tcp        0      0 :::5000                 :::*                    LISTEN <---
tcp        0      0 :::24296                :::*                    LISTEN
tcp        0      0 :::6379                 :::*                    LISTEN
tcp        0      0 :::5555                 :::*                    LISTEN
```


In addition to this, the main point of this attack is to show how a merchant can abuse this functionality to cause extra charges to the customer, unknowingly. I was able to build a relay server for the WebSocket and could snoop on the raw messages without any issue.

Using an ARP spoofing attack it would be possible to MiTM the WebSocket between the real server and the customer while on the same network. At this point, you still need to obtain the initial public key that is in the QR code. This can be done by forcing the client to accept a new one by altering the message types to contain a new receiverPublicKey.

This faulty logic can be seen here in `com.shopify.pos.customerview.common.crypto.ClientCryptoProtocol::receiveMessageFromServer()` in the `com.shopify.pos.customerview` app:

```java
public void receiveMessageFromServer(String str, CryptoType cryptoType, String str2) {
    Intrinsics.checkParameterIsNotNull(str, "message");
    Intrinsics.checkParameterIsNotNull(cryptoType, "type");
    Intrinsics.checkParameterIsNotNull(str2, "publicKeyString");
    if (WhenMappings.$EnumSwitchMapping$0[cryptoType.ordinal()] != 1) {
        str = new Hex().decode(str);
        Intrinsics.checkExpressionValueIsNotNull(str, "decodedMessageString");
        str = handleIncomingMessage(str, cryptoType, str2);
        if (str != null) {
            getDecryptedMessageHandler().invoke(new String(str, Charsets.UTF_8));
            str = handleOutgoingMessage(CryptoConstant.ACK.encoded(), cryptoType);
            if (str != null) {
                str = new Hex().encode(str);
                Intrinsics.checkExpressionValueIsNotNull(str, "Hex().encode(cipherText)");
                String publicKey = getSenderKeyPair().getPublicKey().toString();
                Intrinsics.checkExpressionValueIsNotNull(publicKey, "senderKeyPair.publicKey.toString()");
                getEncryptedMessageHandler().invoke(new CryptoMessage(cryptoType, str, publicKey));
                return;
            }
            return;
        }
        return;
    }
    str = new Hex().decode(str2);
    Intrinsics.checkExpressionValueIsNotNull(str, "Hex().decode(publicKeyString)");
--->setReceiverPublicKey(str);
    onAckReceived();
}
```

Normally, when the customer view initially connects to the server, the public key and nonce from the QR code are stored from the `com.shopify.pos.customerview.common.crypto.ClientCryptoProtocol::start()` method in the `com.shopify.pos.customerview` app:

```java
public void start(String str, String str2, Function0<Unit> function0) {
    Intrinsics.checkParameterIsNotNull(str, "publicKeyString");
    Intrinsics.checkParameterIsNotNull(str2, "randomString");
    Intrinsics.checkParameterIsNotNull(function0, "startCompletion");
    setSenderKeyPair(getCrypto().generateKeyPair());
    setReceiverKeyPair(getCrypto().generateKeyPair());
    str = new Hex().decode(str);
    str2 = new Hex().decode(str2);
    Intrinsics.checkExpressionValueIsNotNull(str, "publicKey");
--->setReceiverPublicKey(str);
    Intrinsics.checkExpressionValueIsNotNull(str2, "random");
    byte[] encrypt = encrypt(str2, getSenderKeyPair(), str);
    str = encrypt(str2, getReceiverKeyPair(), str);
    if (encrypt != null) {
        if (str != null) {
            CryptoType cryptoType = CryptoType.SENDER_INIT;
            String encode = new Hex().encode(encrypt);
            Intrinsics.checkExpressionValueIsNotNull(encode, "Hex().encode(sCiphertext)");
            String publicKey = getSenderKeyPair().getPublicKey().toString();
            Intrinsics.checkExpressionValueIsNotNull(publicKey, "senderKeyPair.publicKey.toString()");
            getEncryptedMessageHandler().invoke(new CryptoMessage(cryptoType, encode, publicKey));
            CryptoType cryptoType2 = CryptoType.RECEIVER_INIT;
            str = new Hex().encode(str);
            Intrinsics.checkExpressionValueIsNotNull(str, "Hex().encode(rCiphertext)");
            String publicKey2 = getReceiverKeyPair().getPublicKey().toString();
            Intrinsics.checkExpressionValueIsNotNull(publicKey2, "receiverKeyPair.publicKey.toString()");
            getEncryptedMessageHandler().invoke(new CryptoMessage(cryptoType2, str, publicKey2));
            function0.invoke();
        }
    }
}
```

As you can see in the code above, the same `setReceiverPublicKey(...)` method is used in the start method as well as the receiveMessageFromServer method. This is the public key that is later used to encrypt the messages with Curve25519 before being sent to and from the server. As a result, when the message type satisfies the if statement below, the rest of the logic is skipped, and the receiver public key can be overridden:

```java
public void receiveMessageFromServer(String str, CryptoType cryptoType, String str2) {
    Intrinsics.checkParameterIsNotNull(str, "message");
    Intrinsics.checkParameterIsNotNull(cryptoType, "type");
    Intrinsics.checkParameterIsNotNull(str2, "publicKeyString");
--->if (WhenMappings.$EnumSwitchMapping$0[cryptoType.ordinal()] != 1) {
        str = new Hex().decode(str);
        Intrinsics.checkExpressionValueIsNotNull(str, "decodedMessageString");
...
    }
    str = new Hex().decode(str2);
    Intrinsics.checkExpressionValueIsNotNull(str, "Hex().decode(publicKeyString)");
    setReceiverPublicKey(str);
    onAckReceived();
}
```

Combining this together...

- the device listens on `0.0.0.0:5000` but instructs clients to connect to the wifi IP address
- the comm

</details>

---
*Analysed by Claude on 2026-05-24*
