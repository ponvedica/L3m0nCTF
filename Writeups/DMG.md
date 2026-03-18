# Dimethylglyoxime CTF Challenge

## Challenge Overview

**Name:** Dimethylglyoxime  
**Category:** Miscellaneous
**File:** `Dimethylglyoxime.dmg`

---

## Challenge Description

**README_FIRST.txt:**
```
Dimethylglyoxime

A disk encrypted, secrets deep inside, 
No hints, no mercy, nowhere left to hide,  
Three layers wait, with ciphers old and new,
We'll see who can break it, who can find the truth.

When something's broken, time tells all,
Seven segments light the way through the wall. 
Add what's counted to what's displayed,
The pieces merge where foundations are laid.

When timestamps break and numbers show,
Combine their secrets, let them flow. 
Seven segments hold a key,
Add the moments, you'll be free.

In the end, all are broken.
```

The poetic description contains subtle hints about combining timestamps with the 7-segment display.

---

## Solution

### Step 0: Discover DMG Password

The DMG is encrypted and cannot be mounted without a password. The password is hidden in extended attributes of `README_FIRST.txt`.

```bash
# Check extended attributes on README_FIRST.txt
xattr -l README_FIRST.txt
```

**Output (12 attributes!):**
```
com.apple.provenance: 
user.author: vedica
user.backup_key: QmFja3VwXzIwMjRfRGF0YQ==
user.checksum: md5:a3f8c9e2b1d4567890abcdef
user.created_date: 2024-03-15T14:22:00Z
user.encryption_type: AES-256-CBC
user.file_id: 0xdeadbeef-2024-forensics
user.hint: ZmFrZV9wYXNzd29yZF9oYWhh
user.legacy_password: VjBsdW0zX09sZF9LM3k=
user.recovery_hint: TG9vazRLM3lJbkJyMGszbl9GaWwz
user.signature: SHA256:a8f9c2e5b6d3417890abcdef12345678
user.version: v2.4.1-stable
user.volume_key: QnIwa2ozbl9WMGx1bTNfMjAyNA==
```

**Challenge:** There are 5 base64-encoded attributes! Players must decode each one to find the real password:

```bash
# Decode all base64 attributes
echo "QmFja3VwXzIwMjRfRGF0YQ==" | base64 -d
# Output: Backup_2024_Data (FAKE)

echo "ZmFrZV9wYXNzd29yZF9oYWhh" | base64 -d
# Output: fake_password_haha (FAKE)

echo "VjBsdW0zX09sZF9LM3k=" | base64 -d
# Output: V0lum3_Old_K3y (FAKE)

echo "TG9vazRLM3lJbkJyMGszbl9GaWwz" | base64 -d
# Output: Look4KeyInBr0k3n_Fil3 (FAKE)

echo "QnIwa2ozbl9WMGx1bTNfMjAyNA==" | base64 -d
# Output: Br0k3n_V0lum3_2024 (REAL!)
```

**DMG Password:** `Br0k3n_V0lum3_2024`

---

### Step 1: Mount the DMG

```bash
hdiutil attach Dimethylglyoxime.dmg -passphrase "Br0k3n_V0lum3_2024"
cd "/Volumes/broken_v2 6"
ls -la
```

**Files found:**
```
.Trash-1000/
.broken/
.flag
.sys/
.system_logs/
config.dat
data/
output/
secrets/
texture_001.jpg
```

---

### Step 2: Explore Hidden Folders

Two hidden forensics folders exist:

#### `.broken/` folder:
```bash
ls -la .broken/
```
```
fsck.bin
repair.log
volume_check.dat
```

#### `.system_logs/` folder:
```bash
ls -la .system_logs/
```
```
.crash_report
install.log
kern.log
```

**Note:** These files contain realistic looking logs but are red herrings. The real clues are in file metadata (timestamps, extended attributes, file slack).

---

### Step 3: Extract Timestamps (Password Part 2)

Check modification times of key files:

```bash
stat -f "%Sm" -t "%H:%M:%S" texture_001.jpg
# Output: 12:00:00 → Extract: 12

stat -f "%Sm" -t "%H:%M:%S" config.dat
# Output: 00:19:00 → Extract: 19

stat -f "%Sm" -t "%H:%M:%S" .sys/.cache_0x7f
# Output: 00:00:10 → Extract: 10
```

**Combined:** `121910`

---

### Step 4: Extract Hidden Image from texture_001.jpg

`texture_001.jpg` appears to be a normal decoy texture, but it contains a hidden embedded file.

**Important:** The DMG volume is read-only, so copy the file to a writable location first:

```bash
cp texture_001.jpg ~/texture_001.jpg
cd ~
```

Use `binwalk` to detect embedded files:

```bash
binwalk texture_001.jpg
```

**Output:**
```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image, total size: 502796 bytes
502796        0x7AC0C         PNG image, total size: 44553 bytes
```

Extract the embedded files:

```bash
binwalk -e texture_001.jpg
cd _texture_001.jpg.extracted/
ls
```

You'll find:
- `0` - The JPEG decoy image
- `7AC0C` - The extracted 7-segment PNG display

---

### Step 5: Analyze the 7-Segment Display

Open the extracted PNG file. It shows a 7-segment LED display. The key insight: look at the **OFF/gray segments**, not the lit (red) segments.

The gray/broken segments spell: **BROKEN**

---

### Step 6: Assemble Password 1

Combine findings:
- Part 1: `BROKEN_` (from 7-segment display)
- Part 3: `121910` (from timestamps)

**Password 1:** `BROKEN_121910`

---

### Step 7: Decrypt Layer 1 (AES-256-CBC)

```bash
openssl enc -aes-256-cbc -d -pbkdf2 -pass pass:BROKEN_121910 -in .sys/.cache_0x7f
```

**Output:** `p4rt1_m4c_`

---

### Step 8: Find Password 2 (Decabit Code Cipher)

Check `.Trash-1000/core.dump`:

```bash
cat .Trash-1000/core.dump
# Output: ///
```

No direct hints! Check extended attributes:

```bash
xattr -l .Trash-1000/core.dump
```

**Output:**
```
user.decabit: -+++---++-++-++---+--+--+-+++-++--+--++-+-++-+--+-++-++---+-+-+---+++-++-++---+-+---+++-+--+-+++--+--+-++++---+-+++---+--+-+--+++--+--++-++-
```

Use dcode.fr to decode the decabit code.

**Password 2:** `R3c0v3r3d_D4ta`


### Step 9: Decrypt Layer 2 (ChaCha20)

```bash
openssl enc -chacha20 -d -pbkdf2 -pass pass:R3c0v3r3d_D4ta -in data/.blob
```

**Output:** `f0r3ns1cs_`

---

### Step 10: Find Password 3 (Binary/Hex Analysis)

Check `data/enc_0xff` - it's an encrypted binary file:

```bash
file data/enc_0xff
# Output: data: openssl enc'd data with salted password
```

Perform hex dump analysis to find hidden data:

```bash
xxd data/enc_0xff
```

**Output:**
```
00000000: 5361 6c74 6564 5f5f 7105 b5f6 8439 ea79  Salted__q....9.y
00000010: bde4 ce9a f3fd 2ac1 004b 4559 3a46 316e  ......*..KEY:F1n
00000020: 346c 5f46 6c34 675f 4b33 79              4l_Fl4g_K3y
```

Look for ASCII strings in the hex dump. At offset `0x18`, after the encrypted data, there's a marker:
- `KEY:` followed by the password in plaintext

**Password 3:** `F1n4l_Fl4g_K3y`

---

### Step 11: Decrypt Layer 3 (3DES-CBC)

```bash
openssl enc -des-ede3-cbc -d -pbkdf2 -pass pass:F1n4l_Fl4g_K3y -in data/enc_0xff
```

**Output:** `8060D90002000000:error:1C80006B:Provider routines:ossl_cipher_generic_block_final:wrong final block length:providers/implementations/ciphers/ciphercommon.c:962:
m4st3r}9??V?t?\Q?wyO??%`

**Password 4:** `m4st3r}`

---

### Step 12: Assemble Flag Parts

```
Part 1: p4rt1_m4c_
Part 2: f0r3ns1cs_
Part 3: m4st3r}
```

**Assembled:** `flag{p4rt1_m4c_f0r3ns1cs_m4st3r}`

---

### Step 13: The Final Flag (ROT13)

Players must realize (through trial and error or deep analysis) to apply ROT13:

```bash
echo "flag{p4rt1_m4c_f0r3ns1cs_m4st3r}" | tr 'a-zA-Z' 'n-za-mN-ZA-M'
```

**FINAL FLAG:** `flag{c4eg1_z4p_s0e3af1pf_z4fg3e}`

---
