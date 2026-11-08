import os
import sys
import time

import requests

CHUNK = 90_000_000


def dl(url, out, total):
    part = out + ".part"
    # determine resume point from completed chunks marker file
    marker = out + ".prog"
    done = int(open(marker).read()) if os.path.exists(marker) else 0
    mode = "ab" if done else "wb"
    f = open(part, mode)
    f.truncate(done)
    while done < total:
        end = min(done + CHUNK - 1, total - 1)
        for attempt in range(30):
            try:
                r = requests.get(url, headers={"Range": f"bytes={done}-{end}"},
                                 timeout=(20, 300), stream=True)
                if r.status_code != 206:
                    raise IOError(f"status {r.status_code}")
                buf = b"".join(r.iter_content(1 << 20))
                if len(buf) != end - done + 1:
                    raise IOError(f"short read {len(buf)}")
                break
            except Exception as e:
                print(f"retry {attempt} at {done}: {e}", flush=True)
                time.sleep(min(2 ** attempt, 60))
        else:
            print("FAILED", out)
            sys.exit(1)
        f.write(buf)
        done = end + 1
        with open(marker, "w") as m:
            m.write(str(done))
        print(f"{out}: {done}/{total}", flush=True)
    f.close()
    os.rename(part, out)
    os.remove(marker)
    print("DONE", out, os.path.getsize(out), flush=True)


if __name__ == "__main__":
    dl(sys.argv[1], sys.argv[2], int(sys.argv[3]))
