# L3MON CTF - Shamir's Secret Sharing Challenge

**Challenge Name:** Shamir's Legacy   
**Category:** Miscellaneous 


---

## Challenge Description

Players receive **TWO files**:
- `challenge.docx` - A biographical document about Adi Shamir containing 3 embedded images
- `prime.txt` - The prime modulus 

The document tells the story of Adi Shamir and his famous secret sharing scheme. Hidden within the 3 images are secret shares that must be extracted using advanced steganography techniques.

**Challenge Features:**
- Multi-layer steganography across 3 images (PNG tEXt chunks, LSB diagonal, JPEG APP15 marker)
- XOR obfuscation on hidden data with varying keys
- Requires extracting shares from different steganography techniques
- Reconstruct the flag using Shamir's Secret Sharing and Lagrange interpolation with the provided prime


## Step 1: Initial Reconnaissance

### Extract the DOCX

```bash
unzip challenge.docx -d extracted/
tree extracted/
```

Key findings:
- `extracted/word/document.xml` - The document content (Shamir's story)
- `extracted/word/media/image1.png` - First embedded image (2.8 MB)
- `extracted/word/media/image2.png` - Second embedded image (360 KB)
- `extracted/word/media/image3.jpg` - Third embedded image (89 KB)

### Read the Story

The document contains Adi Shamir's biography explaining:
- His work on RSA
- Secret Sharing scheme from 1979
- **HINT**: "The foundation of his scheme lies in careful selection of parameters. Each secret requires its own **prime foundation**, carefully chosen to exceed the secret's magnitude..."

---

## Step 2: Extract Share #1 (PNG tEXt Chunks - XOR Obfuscated)

### Check with exiftool

```bash
exiftool extracted/word/media/image1.png
```

**Discovery:**
```
Share data: vpnb{wrusq... (gibberish)
Font data: OOOOOOOO__K... (gibberish)
```

These are **XOR obfuscated**!

### Method 1: Manual Decryption

```python
import struct

def extract_text_chunks(png_path):
    with open(png_path, 'rb') as f:
        png_bytes = f.read()
    
    pos = 8  # Skip PNG signature
    chunks = []
    
    while pos + 8 <= len(png_bytes):
        length = struct.unpack(">I", png_bytes[pos:pos+4])[0]
        ctype = png_bytes[pos+4:pos+8]
        data = png_bytes[pos+8:pos+8+length]
        
        if ctype == b'tEXt':
            null_pos = data.find(b'\x00')
            keyword = data[:null_pos].decode('latin1')
            obfuscated = data[null_pos+1:]
            chunks.append((keyword, obfuscated))
        
        pos += 12 + length
        if ctype == b'IEND':
            break
    
    return chunks

# Extract and decode
chunks = extract_text_chunks('extracted/word/media/image1.png')

for keyword, obfuscated in chunks:
    if keyword == "share_data":
        # XOR key: 0x42
        decoded = bytes([b ^ 0x42 for b in obfuscated])
        print(f"Share #1: {decoded.decode('utf-8')}")
        # Output: 42, 95071391775040725714472895997...
    
    elif keyword == "font_data":
        # XOR key: 0x7F  
        decoded = bytes([b ^ 0x7F for b in obfuscated])
        print(f"Hex dump (contains seed): {decoded.decode('utf-8')}")
```

**Result:** Share #1 = `42, 9507139177504072571447289599726908531367584283056273310520177755758286638360580116559845348284032644967882245479647087586272920`

---

## Step 3: Extract Share #2 (LSB Diagonal Steganography)

**Note:** exiftool shows nothing! This is hidden in the image pixels.

```python
from PIL import Image

def extract_lsb_diagonal(img_path):
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    pixels = img.load()
    
    bits = []
    # Diagonal traversal
    for s in range(w + h - 1):
        for x in range(max(0, s - h + 1), min(w - 1, s) + 1):
            y = s - x
            r, g, b = pixels[x, y]
            bits.append(r & 1)  # LSB of red channel
            
            # Check for null terminator
            if len(bits) % 8 == 0 and len(bits) >= 8:
                byte_val = 0
                for i in range(8):
                    byte_val = (byte_val << 1) | bits[len(bits) - 8 + i]
                if byte_val == 0:
                    # Decode
                    bytes_list = []
                    for i in range(0, len(bits) - 8, 8):
                        byte_val = 0
                        for j in range(8):
                            byte_val = (byte_val << 1) | bits[i + j]
                        bytes_list.append(byte_val)
                    return bytes(bytes_list).decode('utf-8')
    return None

share2 = extract_lsb_diagonal('extracted/word/media/image2.png')
print(f"Share #2: {share2}")
```

**Result:** Share #2 = `137, 7075142950985422074193749379579131369062455688114899226843113713875002436488457954018076625079514207346137631202271274369492946`

---

## Step 4: Extract Share #3 (JPEG APP15 Marker)


### Manual JPEG Parsing Required

```python
import struct

def extract_jpeg_app15(img_path):
    with open(img_path, 'rb') as f:
        data = f.read()
    
    if data[0:2] != b'\xff\xd8':
        raise ValueError("Not a JPEG")
    
    pos = 2
    while pos < len(data):
        if data[pos] != 0xFF:
            break
        
        marker = data[pos:pos+2]
        pos += 2
        
        if marker == b'\xff\xef':  # APP15 marker!
            length = struct.unpack('>H', data[pos:pos+2])[0]
            pos += 2
            payload = data[pos:pos+length-2]
            
            # Remove padding (first 4 and last 4 bytes)
            payload = payload[4:-4]
            
            # XOR decrypt with derived key
            # Key formula: (x * 17 + 0x3A) & 0xFF
            # Try x-values: 42, 137, 256
            for test_x in [42, 137, 256]:
                xor_key = (test_x * 17 + 0x3A) & 0xFF
                decoded = bytes([(b ^ xor_key) for b in payload])
                try:
                    text = decoded.decode('utf-8')
                    if ',' in text:
                        print(f"[+] Share #3: {text}")
                        return text
                except:
                    pass
        
        # Skip other markers
        elif marker in [b'\xff\xd9', b'\xff\xda']:
            break
        elif marker[0] == 0xFF and marker[1] >= 0xC0:
            length = struct.unpack('>H', data[pos:pos+2])[0]
            pos += length
    
    return None

share3 = extract_jpeg_app15('extracted/word/media/image3.jpg')
```

**Result:** Share #3 = `256, 5123472247687472084899541141441494297111533344191476020045296189783964948542163631973856995172409125213123329020574301961614826`

**Key Points:**
- APP15 (0xFFEF) marker is rarely used
- exiftool doesn't parse it
- XOR key derived from x-value: `(256 * 17 + 0x3A) & 0xFF = 0x1A`

---

## Step 5: Read the Prime Modulus

The prime modulus `P` is provided in `prime.txt`:

```bash
cat prime.txt
```

**Output:**
```
17333139023735693365036917262418326746495446687549718551962992699243709777980762791378268870027118545725208398624418232341399251
```

This large prime number is required for the Shamir's Secret Sharing reconstruction. Save this value as you'll need it for the Lagrange interpolation.

---

## Step 6: Reconstruct the Flag

Now that we have P and any 2 shares, use Lagrange interpolation:

```python
from sympy import mod_inverse

def reconstruct_secret(x1, y1, x2, y2, P):
    # Lagrange interpolation at x=0
    numerator = (y1 * x2 - y2 * x1) % P
    denominator = (x2 - x1) % P
    
    secret_int = (numerator * mod_inverse(denominator, P)) % P
    
    # Convert to flag
    hex_str = hex(secret_int)[2:]
    if len(hex_str) % 2:
        hex_str = "0" + hex_str
    
    flag = bytes.fromhex(hex_str).decode('utf-8')
    return flag

flag = reconstruct_secret(42, y1, 137, y2, P)
print(f"FLAG: {flag}")
```

---

## Step 7: Submit the Flag

**FLAG:** `L3m0nCTF{y3ll0w_l3m0ns_t4st3_b3tt3r_w1th_th3_r1ght_f0nts}`

