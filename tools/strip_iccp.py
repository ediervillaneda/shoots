"""
One-time tool: strip incorrect iCCP (ICC color profile) chunks from PNG assets.
Eliminates the "libpng warning: iCCP: known incorrect sRGB profile" at runtime.
No third-party dependencies — uses only Python stdlib.

Usage:
    python tools/strip_iccp.py
"""

import os
import struct

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def strip_iccp(path: str) -> bool:
    with open(path, "rb") as f:
        data = f.read()

    if not data.startswith(PNG_SIGNATURE):
        return False

    pos = 8
    chunks: list[bytes] = []
    removed = False

    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        chunk_type = data[pos + 4 : pos + 8]
        end = pos + 12 + length

        if chunk_type == b"iCCP":
            removed = True
        else:
            chunks.append(data[pos:end])

        pos = end

    if not removed:
        return False

    with open(path, "wb") as f:
        f.write(PNG_SIGNATURE)
        for chunk in chunks:
            f.write(chunk)

    return True


def main() -> None:
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    fixed = 0
    for root, _dirs, files in os.walk(assets_dir):
        for fname in files:
            if fname.lower().endswith(".png"):
                path = os.path.join(root, fname)
                if strip_iccp(path):
                    fixed += 1
                    print(f"  fixed: {os.path.relpath(path)}")
    print(f"\n{fixed} files fixed.")


if __name__ == "__main__":
    main()
