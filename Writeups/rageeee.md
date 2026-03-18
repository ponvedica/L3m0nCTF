# RAGE ZIP - Challenge Solution Writeup

**Challenge Name:** The thing that can keep u awake for sometime   
**Artifact File:** `rageeee.zip` 
**Total Layers:** 30  

---

## Challenge Overview

**"The thing that can keep u awake for sometime"**
> "I tried to open the zip that I encrypted long back, but I couldn't remember the password. However, I do remember these constraints: Password requirements: alphabet - special character - alphabet - special character - alphabet - special character - number - number - number"
>
> **Hint:** "the first password starts with P and ends with 3"

Participants must first identify the pattern (`A-S-A-S-A-S-N-N-N`) to open the initial archive.

---

## Solution Roadmap

### Phase 1: The Warm-Up (Layers 1–6)
*Basic encoding and classical ciphers.*

| Layer | Archive Name | Password | hint.txt Content (Inside) | Method |
|-------|--------------|----------|---------------------------|--------|
| **01** | `rageeee copy.zip` | `p!L@y#123` | *john and bruteforce* | **Pattern Bruteforce**<br>Matches `A-S-A-S-A-S-N-N-N`<br>Starts `p` / Ends `3` |
| **02** | `okay_...zip` | `zipception_master` | `kmbqraxuca_xeehrc` | **Vigenère** (Key `LEMON`)<br>(Found in L1 `hint.txt`) |
| **03** | `trust_...rar` | `dont_break_me` | `==QZt91ahVmci9Fdu9GZ` | **Reverse + Base64** |
| **04** | `this_...7z` | `tears_of_zip` | `01110100 01100101...` | **Binary to ASCII** |
| **05** | `no_joke...zip`| `unzip_this_now` | `hamvc_guvf_abj` | **ROT13** |
| **06** | `why_...rar` | `rage_is_served` | `r_seaei_evdgsr` | **Rail Fence** (3 Rails) |



---

### Phase 2: The Cipher Gauntlet (Layers 7–12)

| Layer | Archive Name | Password | hint.txt Content | Method |
|-------|--------------|----------|------------------|--------|
| **07** | `final_...zip` | `not_for_you_pw` | `OQSYHNFUVTVYBV` | **Playfair** (Key `RAGEZIP`) |
| **08** | `please_...7z` | `tryna_get_it` | `BAABAABABAAABBabab...` | **Bacon Cipher** |
| **09** | `you_are...rar`| `almost_got_it` | `mgtat_l_ioost` | **Columnar** (Key `CHAOS`) |
| **10** | `stop_...zip` | `become_a_zipper` | `21373a3f392a1c33...` | **XOR** (Hex, Key `CRYPTO`) |
| **11** | `just_...zip` | `weirdly_specific_pw` | `WEPRGIYMSQBCIFKNQW` | **Bifid** (Period 5) |
| **12** | `this_...rar` | `do_not_trust_this` | `2a24262a3e2d363e...` | **XOR Hex** (Key `LEMON`) |

---

### Phase 3: The Checkpoint (Layers 13–15)

#### Layer 13: `believe_in_yourself.zip`
*   **Password:** `fakepass_hold`
*   **Contents:** `additional_hint.txt`
*   **Hint Text:** "Find the next 3 best moves using Stockfish"
*   **Method:** **Chess Puzzle**

#### Layer 14: `i_promise.zip`
*   **Password:** `kc4d2_bf8a3_pb2b1`
*   **Contents:** `hint.txt`
*   **Hint Text:** `wsgo_evrr_ayeps`
*   **Method:** **Beaufort Cipher** (Key `PASSWORD`)

#### Layer 15: `last_chance.rar`
*   **Password:** `time_stamp_code`
*   **Contents:** `hint.txt`
*   **Hint Text:** `wjqf_xwbqq_hrei`
*   **Method:** **Vigenère** (Decodes to `decoy_master_key`)

---

### Phase 4: The Final Stretch (Layers 16–30)

| Layer | Archive Name | Password | hint.txt Content | Method |
|-------|--------------|----------|------------------|--------|
| **16** | `no_ser...7z` | `decoy_master_key` | `ZGVjb3lfbWFzdGVyX2tleQ==` | **Base64** |
| **17** | `why_are...zip`| `rename_and_unzip` | `cmVuYW1lX2FuZF91bnppcA==` | **Base64** |
| **18** | `this_is...zip`| `hidden_dot_power` | `hidden_dot_power` | **Pigpen/Plain** |
| **19** | `im_run...zip` | `crc32_secretkey` | `pfp32_lrperfxrl` | **Porta** (Key `ZIPPER`) |
| **20** | `you_wo...zip` | `entry_comment_pw` | `irxvc_gsqqirx_ta` | **Vigenère** (Key `ENTRY`) |
| **21** | `keep_...rar` | `crc32_secretkey` | `143 162 143 63 62 137...` | **Octal** |
| **22** | `turn_...zip` | `entry_comment_pw` | `3n7ry_c0mm3n7_pw` | **Leet Speak** |
| **23** | `are_you...zip`| `morse_master_key` | `NQTRDNGRDODTKDY` | **Playfair** (Key `LAYERS`) |
| **24** | `touch...zip` | `filename_embedded_pw` | `fne_mde_wiameebdpdl` | **Rail Fence** (4) |
| **25** | `sunk_...7z` | `exif_in_image_pw` | `atap_qv_quecs_ta` | **Beaufort** (Key `EXIF`) |
| **26** | `you_ca...zip` | `hex_that_pw` | `96I0E92E0AH` | **ROT47** |
| **27** | `pride...zip` | `rot13_nextone` | `o1tnx3toeern__` | **Columnar** (Key `ROT`) |
| **28** | `this_...zip` | `archive_comment_pw` | `AABABAAABABAA...` | **Bacon** |
| **29** | `almost...7z` | `final_password` | `final_password` | **Given/Steg** |
| **30** | `huh_bro...zip`| *(None)* | *(None)* | **Open** |





---

## The Flag

After extracting the final layer (`huh_bro_whyyy.zip`), we reveal `final_flag.txt`:


```text
L3m0nCTF{CONGRATULATIONS_YOU_ACTUALLY_SURVIVED_ALL_30_LAYERS_OF_COMPRESSED_CHAOS_AND_OBFUSCATED_PASSWORDS_THIS_FLAG_IS_INTENTIONALLY_ABSURDLY_LONG_TO_MAKE_YOU_QUESTION_WHETHER_IT_WAS_WORTH_THE_HOURS_YOU_SPENT_LEARNING_ABOUT_BZIP2_AND_LZMA_AND_ZSTANDARD_AND_BROTLI_AND_LZ4_AND_SEVEN_ZIP_AND_RAR_ARCHIVES_AND_BASE64_ENCODING_AND_ROT13_AND_XOR_CIPHERS_AND_HEXDUMP_AND_MORSE_CODE_AND_PNG_METADATA_AND_SPLIT_FILES_BUT_HEY_YOU_EARNED_THIS_YOU_STUBBORN_MAGNIFICENT_PERSON_NOW_GO_TOUCH_GRASS_DRINK_WATER_AND_TELL_YOUR_FRIENDS_YOU_CONQUERED_THE_ULTIMATE_RAGEZIP_CHALLENGE_AND_SURVIVED_TO_TELL_THE_TALE_YOU_ARE_BOTH_A_HERO_AND_A_FOOL_AND_WE_SALUTE_YOU}
```

---
