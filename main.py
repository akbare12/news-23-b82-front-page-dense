#!/usr/bin/env python3
"""news-23 b82 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import binascii
import hashlib
import os
import struct
import sys

MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(here)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if not os.path.isfile(src):
        return fail("entry.png not found next to main.py")

    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        return fail("entry.png exceeds 1 MiB")
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("entry.png is not a PNG")
    # Parse IHDR manually (stdlib struct only).
    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("missing IHDR chunk")
    w, h, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (w, h) != (1024, 1024):
        return fail("entry.png must be 1024x1024, got %dx%d" % (w, h))
    if depth != 8 or ctype not in (2, 6):
        return fail("unexpected bit depth / colour type")
    ihdr_crc = binascii.crc32(data[12:29]) & 0xFFFFFFFF
    stored_crc = struct.unpack(">I", data[29:33])[0]
    if ihdr_crc != stored_crc:
        return fail("IHDR CRC mismatch")
    # Walk every chunk: verify each CRC, require an IDAT, and require the
    # last chunk to be a well-formed 12-byte IEND trailer.
    pos = 8
    seen_idat = False
    last_type = None
    while pos + 8 <= len(data):
        clen, ctype_b = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 8 + clen + 4
        if end > len(data):
            return fail("truncated chunk at offset %d" % pos)
        if binascii.crc32(data[pos + 4:end - 4]) & 0xFFFFFFFF != struct.unpack(">I", data[end - 4:end])[0]:
            return fail("chunk CRC mismatch at offset %d" % pos)
        if ctype_b == b"IDAT":
            if clen == 0:
                return fail("empty IDAT chunk")
            seen_idat = True
        last_type = ctype_b
        pos = end
    if not seen_idat:
        return fail("no IDAT chunk found")
    if last_type != b"IEND" or pos != len(data):
        return fail("PNG does not end with a well-formed IEND chunk")

    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        return fail("output differs from source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
