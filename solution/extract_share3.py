#!/usr/bin/env python3
"""
Extract Share from JPEG APP15 marker (heavily obfuscated)
Players must manually parse JPEG structure to find this!
"""
import struct

def extract_jpeg_app15(img_path):
    """Extract data from custom APP15 marker in JPEG"""
    with open(img_path, 'rb') as f:
        data = f.read()
    
    # Check JPEG signature
    if data[0:2] != b'\xff\xd8':
        raise ValueError("Not a JPEG file")
    
    pos = 2
    while pos < len(data):
        # Read marker
        if data[pos] != 0xFF:
            break
        
        marker = data[pos:pos+2]
        pos += 2
        
        if marker == b'\xff\xef':  # APP15
            # Read length
            length = struct.unpack('>H', data[pos:pos+2])[0]
            pos += 2
            
            # Read payload
            payload = data[pos:pos+length-2]
            
            print(f"[*] Found APP15 marker!")
            print(f"[*] Length: {length}")
            print(f"[*] Raw payload (hex): {payload.hex()}")
            
            # Remove padding (first 4 and last 4 bytes)
            if len(payload) >= 8:
                payload = payload[4:-4]
                print(f"[*] After removing padding: {payload.hex()}")
            
            # Try different XOR keys
            print(f"\n[*] Trying XOR decryption...")
            for test_x in [42, 137, 256]:
                xor_key = (test_x * 17 + 0x3A) & 0xFF
                decoded = bytes([(b ^ xor_key) for b in payload])
                try:
                    text = decoded.decode('utf-8')
                    if ',' in text and text.replace(',', '').replace(' ', '').replace('-', '').isdigit():
                        print(f"\n[+] SUCCESS with x={test_x}, XOR key=0x{xor_key:02x}")
                        print(f"[+] Share: {text}")
                        return text
                except:
                    pass
            
            print("[-] Could not decode with known keys")
            return None
        
        # Skip other markers
        elif marker in [b'\xff\xd9', b'\xff\xda']:  # EOI or SOS
            break
        elif marker[0] == 0xFF and marker[1] >= 0xC0:
            # Marker with length
            length = struct.unpack('>H', data[pos:pos+2])[0]
            pos += length
    
    print("[-] No APP15 marker found")
    return None

if __name__ == "__main__":
    import sys
    
    img_path = sys.argv[1] if len(sys.argv) > 1 else "out/word/media/image3.jpg"
    
    print(f"[*] Analyzing JPEG: {img_path}")
    print(f"[*] Looking for hidden APP15 marker...")
    print()
    
    share = extract_jpeg_app15(img_path)
    
    if share:
        print(f"\n{'='*60}")
        print(f"SHARE RECOVERED: {share}")
        print(f"{'='*60}")
