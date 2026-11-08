#!/usr/bin/env python3
"""Walk an uncompressed tar on GCS via HTTP Range requests (512B headers,
skip payloads), extract GTEx v8 Brain_* significant-pairs files to /tmp."""
import urllib.request, io, os, sys, time

BASE = "https://storage.googleapis.com/download/storage/v1/b/adult-gtex/o/"
def url(name):
    return BASE + urllib.parse.quote(name, safe="") + "?alt=media"

import urllib.parse

def fetch_range(u, start, end):
    req = urllib.request.Request(u, headers={"Range": f"bytes={start}-{end}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def parse_size(h):
    return int(h[124:136].split(b"\0")[0].strip() or b"0", 8)

def scan(tar_name, patterns, outdir, max_files=60):
    u = url(tar_name)
    off = 0; found = []
    while True:
        h = fetch_range(u, off, off + 511)
        if len(h) < 512 or h[0] == 0:
            break
        name = h[0:100].split(b"\0")[0].decode()
        prefix = h[345:500].split(b"\0")[0].decode()
        if prefix: name = prefix + "/" + name
        size = parse_size(h)
        typeflag = h[156:157]
        data_off = off + 512
        if typeflag in (b"0", b"\0") and any(p in name for p in patterns):
            found.append((name, data_off, size))
            print(f"MATCH {name} size={size} off={data_off}", flush=True)
        off = data_off + ((size + 511) // 512) * 512
        if len(found) >= max_files:
            break
    return u, found

def extract(u, entries, outdir):
    for name, off, size in entries:
        fn = os.path.join(outdir, name.replace("/", "__"))
        if os.path.exists(fn) and os.path.getsize(fn) == size:
            print("skip existing", fn); continue
        print(f"downloading {name} ({size/1e6:.1f} MB)", flush=True)
        data = fetch_range(u, off, off + size - 1)
        with open(fn, "wb") as f:
            f.write(data)
        print(f"  wrote {fn} {len(data)} bytes", flush=True)
        time.sleep(1)

if __name__ == "__main__":
    which = sys.argv[1]
    os.makedirs("/tmp/gtex_v8", exist_ok=True)
    if which == "eqtl":
        u, entries = scan("bulk-qtl/v8/single-tissue-cis-qtl/GTEx_Analysis_v8_eQTL.tar",
                          ["Brain_", ], "/tmp/gtex_v8")
        entries = [e for e in entries if "signif_variant_gene_pairs" in e[0]]
        extract(u, entries, "/tmp/gtex_v8")
    else:
        u, entries = scan("bulk-qtl/v8/single-tissue-cis-qtl/GTEx_Analysis_v8_sQTL.tar",
                          ["Brain_", ], "/tmp/gtex_v8")
        extract(u, entries, "/tmp/gtex_v8")
    print("DONE")
