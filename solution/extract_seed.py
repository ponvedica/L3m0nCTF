#!/usr/bin/env python3
"""
Extract hidden font_data from PNG (contains hex dump with seed)
This is a secret extraction - players must find this second tEXt chunk!
"""
import struct
import zlib
import re

def parse_png_chunks(png_path):
    """Parse PNG file and extract chunks"""
    with open(png_path, 'rb') as f:
        png_bytes = f.read()
    
    sig = png_bytes[:8]
    if sig != b'\x89PNG\r\n\x1a\n':
        raise ValueError("Not a PNG file")
    
    pos = 8
    chunks = []
    while pos + 8 <= len(png_bytes):
        length = struct.unpack(">I", png_bytes[pos:pos+4])[0]
        ctype = png_bytes[pos+4:pos+8]
        data = png_bytes[pos+8:pos+8+length]
        chunks.append((ctype, data))
        pos = pos + 12 + length
        if ctype == b'IEND':
            break
    return chunks

def extract_all_text_chunks(png_path):
    """Extract ALL tEXt chunks from PNG"""
    chunks = parse_png_chunks(png_path)
    
    text_chunks = []
    for ctype, data in chunks:
        if ctype == b'tEXt':
            # Split keyword and payload
            null_pos = data.find(b'\x00')
            if null_pos == -1:
                continue
            keyword = data[:null_pos].decode('latin1')
            obfuscated = data[null_pos+1:]
            text_chunks.append((keyword, obfuscated))
    
    return text_chunks

def recover_seed_from_font_data(hex_dump_text):
    """Recover seed from the font table hex dump"""
    # Extract the hex bytes from the dump
    lines = hex_dump_text.strip().split('\n')
    all_bytes = []
    
    for line in lines:
        # Parse hex dump format: "00000000  4f 54 54 4f ..."
        parts = line.split('  ')
        if len(parts) < 2:
            continue
        hex_part = parts[1].split('  ')[0]  # Get just the hex, not ASCII
        hex_bytes = hex_part.split()
        for hb in hex_bytes:
            try:
                all_bytes.append(int(hb, 16))
            except ValueError:
                pass
    
    bytes_data = bytes(all_bytes)
    
    # The seed is encoded in the table checksums
    # See builder.py create_font_record_hexdump for encoding scheme
    def find_marker(marker_bytes):
        idx = bytes_data.find(marker_bytes)
        if idx == -1:
            return None
        # Marker + 12 bytes = 4th uint32
        pos = idx + len(marker_bytes) + 12
        if pos + 4 > len(bytes_data):
            return None
        val = int.from_bytes(bytes_data[pos:pos+4], 'big')
        return val
    
    markers = {
        'cmap': b'\\xDE\\xAD\\xBE\\xEF',
        'glyf': b'\\xCA\\xFE\\xBA\\xBE',
        'head': b'\\xFA\\xCE\\xFE\\xED',
        'hhea': b'\\x12\\x34\\x56\\x78'
    }
    
    vals = {}
    for name, m in markers.items():
        v = find_marker(m)
        vals[name] = v
        print(f"  {name} -> {v}")
    
    # Brute force seed reconstruction
    for seed in range(0, 20000):
        low10000 = seed % 10000
        high16 = (seed >> 16) % 10000
        low8_head = (seed >> 8) & 0xFF
        low8_hhea = seed & 0xFF
        
        ok = True
        if vals['cmap'] is not None and vals['cmap'] != low10000:
            ok = False
        if vals['glyf'] is not None and vals['glyf'] != high16:
            ok = False
        if vals['head'] is not None and vals['head'] != low8_head:
            ok = False
        if vals['hhea'] is not None and vals['hhea'] != low8_hhea:
            ok = False
        
        if ok:
            return seed
    
    return None

if __name__ == "__main__":
    import sys
    
    png_path = sys.argv[1] if len(sys.argv) > 1 else "out/word/media/image1.png"
    
    print(f"[*] Extracting ALL tEXt chunks from: {png_path}")
    text_chunks = extract_all_text_chunks(png_path)
    
    print(f"[*] Found {len(text_chunks)} tEXt chunk(s)")
    print()
    
    for keyword, obfuscated in text_chunks:
        print(f"[*] Chunk keyword: '{keyword}'")
        
        if keyword == "font_data":
            # This is the hidden seed data - XOR key 0x7F
            print("  [!] This is the HIDDEN font_data chunk!")
            deobf = bytes([b ^ 0x7F for b in obfuscated])
            hex_dump = deobf.decode('utf-8')
            print("  [*] Deobfuscated hex dump:")
            print()
            for line in hex_dump.split('\n')[:6]:  # Show first few lines
                print(f"      {line}")
            print()
            
            print("  [*] Recovering seed from font table...")
            seed = recover_seed_from_font_data(hex_dump)
            if seed:
                print(f"\n  [+] SEED RECOVERED: {seed}")
            else:
                print("  [-] Failed to recover seed")
        else:
            # Try standard XOR key 0x42
            deobf = bytes([b ^ 0x42 for b in obfuscated])
            print(f"  [*] Data (XOR 0x42): {deobf.decode('utf-8', errors='ignore')}")
        
        print()
