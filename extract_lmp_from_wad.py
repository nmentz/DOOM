#/bin/python3

import struct
import sys
import os

def extract_lumps(wad_path, lumps_to_extract):
    with open(wad_path, 'rb') as f:
        header = f.read(12)
        if len(header) < 12:
            print("Invalid WAD file.")
            return

        wad_type, num_lumps, dir_offset = struct.unpack('<4sII', header)
        f.seek(dir_offset)

        lumps = []
        for _ in range(num_lumps):
            entry = f.read(16)
            filepos, size, name_bytes = struct.unpack('<II8s', entry)
            name = name_bytes.decode('ascii').rstrip('\0')
            lumps.append((name, filepos, size))

        for lump_name in lumps_to_extract:
            found = False
            for name, filepos, size in lumps:
                if name.upper() == lump_name.upper():
                    found = True
                    f.seek(filepos)
                    data = f.read(size)
                    filename = lump_name.lower() + '.lmp'
                    with open(filename, 'wb') as out:
                        out.write(data)
                    print(f"Extracted {lump_name} to {filename}")
                    break
            if not found:
                print(f"Lump {lump_name} not found in WAD.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_lumps.py DOOM.WAD")
        sys.exit(1)

    wad_file = sys.argv[1]
    lumps = ['PNAMES', 'TEXTURE1', 'TEXTURE2']  # lumps you want extracted

    extract_lumps(wad_file, lumps)
