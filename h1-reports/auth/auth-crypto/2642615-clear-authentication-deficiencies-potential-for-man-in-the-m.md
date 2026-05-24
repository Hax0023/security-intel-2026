# 明確な認証不備および潜在的な中間者攻撃の可能性（Clear Authentication Deficiencies & Potential for Man-in-the-Middle Attacks）

## Metadata
- **Source:** HackerOne
- **Report:** 2642615 | https://hackerone.com/reports/2642615
- **Submitted:** 2024-08-06
- **Reporter:** trapedev
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Key Exchange without Entity Authentication
- **CVEs:** None
- **Category:** auth-crypto

## Summary
English follows Japanese.

ソニーグループ株式会社 様

この度，弊社製品のWH-1000XM5に深刻なセキュリティ脆弱性を確認いたしましたのでご報告いたします．
セキュリティ研究者として，貴社製品の継続的なセキュリティと完全性を確保するために，このような発見を報告することは極めて重要であると考えます．

# Sec.0 要約

- 本レポートは，貴社製品のWH-1000XM5に確認された認証不備の脆弱性を示します．
- 本脆弱性をBluetoothの既存攻撃と組み合わせることで，容易にMitM攻撃を達成できます．
- 報告者は，本脆弱性へのCVE番号の割り当てを要求します．

# Sec.1 脆弱性の種類

認証不備

# Sec.2 脆弱性の詳細

悪意ある第三者（以後，攻撃者）WH-1000XM5とペアリングされたデバイスになりすますことで，WH-1000X

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

English follows Japanese.

ソニーグループ株式会社 様

この度，弊社製品のWH-1000XM5に深刻なセキュリティ脆弱性を確認いたしましたのでご報告いたします．
セキュリティ研究者として，貴社製品の継続的なセキュリティと完全性を確保するために，このような発見を報告することは極めて重要であると考えます．

# Sec.0 要約

- 本レポートは，貴社製品のWH-1000XM5に確認された認証不備の脆弱性を示します．
- 本脆弱性をBluetoothの既存攻撃と組み合わせることで，容易にMitM攻撃を達成できます．
- 報告者は，本脆弱性へのCVE番号の割り当てを要求します．

# Sec.1 脆弱性の種類

認証不備

# Sec.2 脆弱性の詳細

悪意ある第三者（以後，攻撃者）WH-1000XM5とペアリングされたデバイスになりすますことで，WH-1000XM5が**ペアリングモードでなくても**，且つ**WH-1000XM5のユーザの操作を一切必要とせず**攻撃者デバイスと接続されます．

Bluetoothパケットを確認すると，WH-1000XM5の再接続時の認証に不備があり，Secure Simple Paring（SSP）の再接続時プロセスに準拠していません．

# Sec.3 影響を受ける製品

[WH-1000XM5](https://www.sony.jp/headphone/products/WH-1000XM5/)

**NOTE**
本脆弱性は，WH-1000XM5に限らない可能性があります．

# Sec.4 PoC

本セクションでは，PoCに必要なデバイスとセットアップ，そして本脆弱性を再現する手順を説明します．

## .4.1 PoC デバイス

**Victim's Master Device**

| Manufacturer | Model | Operation System | Driver | Bluetooth Version |
|--------------|-------|-------------------|--------|-------------------|
| Microsoft | Surface Laptop 4 | Windows 11 Home | Intel(R) Wireless Bluetooth(R) | 5.1 |

**Victim's Slave Device**

|  Manufacturer | Model | Bluetooth Version | 
|--------------|-------|-------------------|
| Sony Corporation | WH-1000XM5 | 5.2 |

**Attacker's Device**

| Model | Operation System | System | Debian version | Kernel version | BlueZ version | Bluetooth Manufacturer | Bluetooth Version |
|-------|------------------|--------|----------------|----------------|---------------|------------------------|-------------------|
| Raspberry Pi 4 Model B | Raspberry Pi OS | 32bit | 11 bullseye | 6.1 | 5.55 | Cypress Semiconductor | 5.0 |

## .4.2 PoC セットアップ

WH-1000XM5とSurface Laptop 4を予めペアリングします．

## .4.3. PoC 手順

1. Raspberry PiのBluetoothアドレスとアダプタのBluetooth名を，Surface Laptop 4と同様の設定にスプーフィングします．
2. Raspberry PiのBluetoothアダプタの状態を`Discoverable`にします．
3. WH-1000XM5を一定時間放置・あるいは手動により電源を切ります．
4. Surface Laptop 4の電源を切ります．
5.  WH-1000XM5の電源を入れます（NOTE: ペアリングモードへの移行を避けるため，電源ボタンは5秒間以上押さないことに留意してください）．

以上の手順を順に踏んだ場合，WH-1000XM5は**ペアリングモードでないにも関わらずRaspberry Piとペアリング・接続されます**．本脆弱性を再現した際にRaspberry Pi側で確認されたBluetoothパケットを添付します（`WH-1000XM5_vuln_poc.pcapng`を参照）．この時，Raspberry PiはWH-1000XM5と過去にペアリングしたことが**無い**点に留意してください．

**NOTE: **
本脆弱性の再現場面が現実的であることを示すために，Surface Laptop 4の電源を切った後にWH-1000XM5の電源を入れた理由を説明します．私（報告者）は，WH-1000XM5をもう一台のデバイス（Pixel 7 Pro）とペアリングしていました．WH-1000XM5へPixel 7 Proを用いて音楽を流すために，WH-1000XM5の電源を入れました．本脆弱性は，Pixel 7 ProのBluetoothの設定画面を開き，WH-1000XM5との接続を試みる間に，**一切の操作を介せず自動的に**Raspberry PiとWH-1000XM5が接続されました．

# Sec.5 潜在的なMitM攻撃

██████の研究チームは，Bluetoothの省電力モードを用いたデバイスハイジャック攻撃を提案しています．詳しくは，2024年7月に情報処理学会から発刊された論文「[Bluetooth省電力モードを用いるデバイスハイジャック攻撃](https://ipsj.ixsq.nii.ac.jp/ej/?action=pages_view_main&active_action=repository_view_main_item_detail&item_id=237288&item_no=1&page_id=13&block_id=8)」をご確認ください．

省電力モードではありませんが，WH-1000XM5には一定時間無操作状態の場合に自動的に電源が切れる仕様が定義されています（[ヘルプガイド](https://helpguide.sony.net/mdr/wh1000xm5/v1/ja/contents/TP1000533411.html)より）．本挙動は省電力モードの一種のSleepモードの挙動に類似するものです．彼らは，攻撃者が本挙動のようなBluetoothセッションの一時的な切断を悪用することで，Bluetoothセッションをハイジャック可能であること実証しています（[参考](https://ipsj.ixsq.nii.ac.jp/ej/?action=pages_view_main&active_action=repository_view_main_item_detail&item_id=237288&item_no=1&page_id=13&block_id=8)）．

WH-1000XM5とLaptopがペアリング済みであると仮定し，WH-1000XM5の電源が自動的に切れた場合，攻撃者はWH-1000XM5になりすましてLaptopとのペアリングが可能です．一方，攻撃者がLaptopになりすました場合，本レポートの脆弱性によりWH-1000XM5と攻撃者がペアリング可能です．従って，攻撃者はWH-1000XM5とLaptopの通信の中間者になります．本結果は，完全性や可用性のみならず，機密性にも重大な脅威をもらたします．

# Sec.6 要望

- 本脆弱性は，貴社製品の仕様，またBluetoothのプロトコルの仕様では決してないと考えます．本レポートに対する貴社のレスポンスを頂ければと思います．
- 貴社がCNAの場合，CVE番号を付与してください．CNAでない場合，私からIPA/JPCERTに報告しCVE番号の付与を依頼させていただきます．

# 付録

## Raspberry PiのBluetooth名を変更する方法

Raspberry PiのBluetooth名を変更する方法を説明します．
まず，`/etc`ディレクトリ下に`machine-info`ファイルを作成します．
作成した`machine-info`ファイルを開き，`PRETTY_HOSTNAME`変数にBluetooth名を定義します．
例えば，Bluetooth名を`Example Laptop`としたい場合，`PRETTY_HOSTNAME=Example Laptop`とします．
設定後，Bluetoothサービスを再起動してください．

## Raspberry PiのBluetoothアドレスを変更する方法

Raspberry PiのBluetoothアドレスを変更するGolangのスクリプトを本レポートに添付します（`main.go`参照）．
Raspberry Pi上で`main.go`ファイルをbuildし，以下のコマンドを例にBluetoothアドレスを変更することができます．

```bash
# ソースコードのビルド
go build main.go -o chgbtaddr

# アドレスの変更
# ex.) LaptopのBluetoothアドレスを00:11:22:33:44:55と仮定
./chgbtaddr -addr 00:11:22:33:44:55

# サービス再起動
sudo systemctl restart bluetooth.service
```



本レポートへのご対応ありがとうございます．**追加の情報やより詳細な情報が必要な場合（e.g., PoCの一連を示すデモ動画，商品番号 etc.）は，ご連絡いただければ可能な限り対応いたします**．本レポートに記載の潜在的なセキュリティリスクに対処するため，迅速なご回答とご協力をお待ちしております．

敬具
██████████

****************************************
██████████
Tel: ███
E-mail : ██████
****************************************

===========================


Dear Sony Group Corporation

I hereby report that I have identified a serious security vulnerability in our product, the WH-1000XM5.
As a security researcher, I believe it is extremely important to report such findings to ensure the ongoing security and integrity of your company's products.

# Sec.0 Executive Summary

- This report details an authentication vulnerability identified in your company's WH-1000XM5 product.
- By combining this vulnerability with existing Bluetooth attacks, a Man-in-the-Middle (MitM) attack can be easily achieved.
- The reporter requests the assignment of a CVE number for this vulnerability.

# Sec.1 Vulnerability Type

Authentication Deficiencies

# Sec.2 Vulnerability Details

A malicious third party (hereinafter referred to as the attacker) can impersonate a device that has been paired with the WH-1000XM5, allowing the attacker's device to connect to the WH-1000XM5 even when it is not in pairing mode and **without requiring any operation from the WH-1000XM5 user**.
Upon examining the Bluetooth packets, it appears that there is a flaw in the authentication process during reconnection of the WH-1000XM5. It does not comply with the reconnection process of Secure Simple Pairing (SSP).

# Sec.3 Affected Specification

[WH-1000XM5](https://www.sony.jp/headphone/products/WH-1000XM5/)

**NOTE**
This vulnerability may not be limited to the WH-1000XM5.

# Sec.4  PoC

This section presents the devices and setup required for the Proof of Concept (PoC), as well as the steps to reproduce this vulnerability.

## .4.1 PoC Devices

**Victim's Master Device**

| Manufacturer | Model | Operation System | Driver | Bluetooth Version |
|--------------|-------|-------------------|--------|-------------------|
| Microsoft | Surface Laptop 4 | Windows 11 Home | Intel(R) Wireless Bluetooth(R) | 5.1 |

**Victim's Slave Device**

|  Manufacturer | Model | Bluetooth Version | 
|--------------|-------|-------------------|
| Sony Corporation | WH-1000XM5 | 5.2 |

**Attacker's Device**

| Model | Operation System | System | Debian version | Kernel version | BlueZ version | Bluetooth Manufacturer | Bluetooth Version |
|-------|------------------|--------|----------------|----------------|---------------|------------------------|-------------------|
| Raspberry Pi 4 Model B | Raspberry Pi OS | 32bit | 11 bullseye | 6.1 | 5.55 | Cypress Semiconductor | 5.0 |

## .4.2 PoC Setup

Pair the WH-1000XM5 and Surface Laptop 4 in advance.

## .4.3 PoC Procedure

1. Spoof the Bluetooth address of the Raspberry Pi and the Bluetooth name of its adapter to match those of the Surface Laptop 4.
2. Set the Bluetooth adapter state of the Raspberry Pi to `Discoverable`.
3. Leave the WH-1000XM5 idle for a while or manually turn off its power.
4. Turn off the Surface Laptop 4.
5. Turn on the WH-1000XM5 (NOTE: Be careful not to press the power button for more than 5 seconds to avoid entering pairing mode).

If you follow these steps in order, the WH-1000XM5 will pair and connect to the Raspberry Pi despite not being in pairing mode. I have attached the Bluetooth packets observed on the Raspberry Pi side when reproducing this vulnerability (refer to `WH-1000XM5_vuln_poc.pcapng`). Please note that the Raspberry Pi has **never previously paired** with the WH-1000XM5.

**NOTE:**
To show that the reproduction of this vulnerability is realistic, I explain why the WH-1000XM5 was tur

</details>

---
*Analysed by Claude on 2026-05-24*
