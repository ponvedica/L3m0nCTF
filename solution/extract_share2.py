#!/usr/bin/env python3
"""
Extract Share from LSB diagonal steganography
Format: "x, y" (comma-space separated)
"""
from PIL import Image

def extract_lsb_diagonal(img_path):
    """Extract data from LSB using diagonal traversal"""
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    pixels = img.load()
    
    bits = []
    for s in range(w + h - 1):
        for x in range(max(0, s - h + 1), min(w - 1, s) + 1):
            y = s - x
            r, g, b = pixels[x, y]
            bits.append(r & 1)
            
            # Check for null terminator every 8 bits
            if len(bits) % 8 == 0 and len(bits) >= 8:
                byte_val = 0
                for i in range(8):
                    byte_val = (byte_val << 1) | bits[len(bits) - 8 + i]
                if byte_val == 0:
                    # Found null terminator
                    bytes_list = []
                    for i in range(0, len(bits) - 8, 8):
                        byte_val = 0
                        for j in range(8):
                            byte_val = (byte_val << 1) | bits[i + j]
                        bytes_list.append(byte_val)
                    try:
                        return bytes(bytes_list).decode('utf-8')
                    except:
                        pass
    return None

if __name__ == "__main__":
    import sys
    
    img_path = sys.argv[1] if len(sys.argv) > 1 else "out/word/media/image2.png"
    
    print(f"[*] Extracting from: {img_path}")
    print(f"[*] Using LSB diagonal traversal...")
    
    share = extract_lsb_diagonal(img_path)
    
    if share:
        print(f"\n[+] Share: {share}")
    else:
        print("[-] Failed to extract data")
