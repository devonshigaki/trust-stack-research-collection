
import sys; sys.path.append("/home/kimi/.local/lib/python3.12/site-packages")
import json, os, time, socket, threading, urllib.request, fastavro
from collections import Counter
socket.setdefaulttimeout(60)
OUT = "/mnt/agents/output/simh1_work"; TMP = "/tmp/h01"
HOSTS = ["https://h01-release.storage.googleapis.com/",
         "https://storage.googleapis.com/h01-release/"]
os.makedirs(TMP, exist_ok=True); os.makedirs(OUT+"/parts", exist_ok=True)
shards = json.load(open(OUT+"/h01_shard_list.json"))
cells = json.load(open(OUT+"/h01_cell_data.json"))
typed = set(int(c["agglo_seg"]) for c in cells)
done_path = OUT+"/h01_done.json"
status = {"errors": []}
def get_done():
    return set(json.load(open(done_path))) if os.path.exists(done_path) else set()
def mark_done(tag):
    d = get_done(); d.add(tag); json.dump(sorted(d), open(done_path,"w"))
def st(**kw):
    status.update(kw)
    try: json.dump(status, open(OUT+"/h01_worker_status.json","w"))
    except Exception: pass

def fetch_range(host, name, s, e):
    req = urllib.request.Request(host+name, headers={"Range": f"bytes={s}-{e}"})
    with urllib.request.urlopen(req) as r:
        return r.read()

def fetch(name, size, local):
    half = size//2
    for attempt in range(6):
        host = HOSTS[attempt % 2]
        try:
            b1 = fetch_range(host, name, 0, half-1)
            b2 = fetch_range(host, name, half, size-1)
            with open(local,"wb") as f: f.write(b1); f.write(b2)
            return os.path.getsize(local) == size
        except Exception as ex:
            status["errors"].append([name.rsplit("/",1)[-1], attempt, repr(ex)[:100]])
            st(backoff=min(300, 15*(2**attempt)))
            time.sleep(min(300, 15*(2**attempt)))
    return False

for name, size in shards:
    tag = name.rsplit("/",1)[-1]
    if tag in get_done(): continue
    local = TMP+"/work.avro"
    if not fetch(name, size, local):
        status["errors"].append([tag,"SKIP",""]); st(current=tag); continue
    pairs = Counter(); posttot = Counter(); rows = 0
    with open(local,"rb") as f:
        for rec in fastavro.reader(f):
            rows += 1
            t = rec["type"]
            post = rec["post_synaptic_partner"]["neuron_id"]
            if post in typed:
                posttot[(post, t)] += 1
                pre = rec["pre_synaptic_site"]["neuron_id"]
                if pre in typed: pairs[(pre, post, t)] += 1
    if os.path.exists(OUT+"/parts/pairs_"+tag+".csv"):
        mark_done(tag); os.remove(local); continue
    agg = {}
    for (pre,post,t),n in pairs.items():
        a = agg.setdefault((pre,post),[0,0]); a[t-1] += n
    with open(OUT+"/parts/pairs_"+tag+".csv","w") as f:
        f.write("pre,post,t1,t2\n")
        for (pre,post),(a,b) in agg.items(): f.write(f"{pre},{post},{a},{b}\n")
    agg2 = {}
    for (post,t),n in posttot.items():
        a = agg2.setdefault(post,[0,0]); a[t-1] += n
    with open(OUT+"/parts/posttot_"+tag+".csv","w") as f:
        f.write("post,t1,t2\n")
        for post,(a,b) in agg2.items(): f.write(f"{post},{a},{b}\n")
    mark_done(tag); os.remove(local)
    st(current=tag, done=len(get_done()), rows_last=rows)
st(finished=time.time())
