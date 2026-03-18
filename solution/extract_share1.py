"""
Extract Share from PNG tEXt chunk (XOR obfuscated)
Format: "x, y" (comma-space separated)
"""
import struct
import zlib
import os

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

def extract_text_chunk(png_path, xor_key=0x42):
    """Extract and deobfuscate tEXt chunk"""
    chunks = parse_png_chunks(png_path)
    
    for ctype, data in chunks:
        if ctype == b'tEXt':
            # Split keyword and payload
            null_pos = data.find(b'\x00')
            if null_pos == -1:
                continue
            keyword = data[:null_pos].decode('latin1')
            obfuscated = data[null_pos+1:]
            
            # XOR deobfuscate
            deobf = bytes([b ^ xor_key for b in obfuscated])
            
            print(f"[*] Found tEXt chunk: keyword='{keyword}'")
            print(f"[*] Deobfuscated data: {deobf.decode('utf-8')}")
            return deobf.decode('utf-8')
    
    return None

if __name__ == "__main__":
    import sys
    
    png_path = sys.argv[1] if len(sys.argv) > 1 else "../dist/test_forensics/word/media/image1.png"
    
    print(f"[*] Extracting from: {png_path}")
    
    if not os.path.exists(png_path):
        print(f"[-] File not found: {png_path}")
        print(f"[*] Please extract challenge.docx first:")
        print(f"    cd ../dist && unzip -o challenge.docx -d test_forensics")
        sys.exit(1)
    
    share = extract_text_chunk(png_path)
    
    if share:
        print(f"\n[+] Share: {share}")
    else:
        print("[-] No tEXt chunk found")
