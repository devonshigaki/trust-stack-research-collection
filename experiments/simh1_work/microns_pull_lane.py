
import sys, json, os, time, threading, warnings, queue
sys.path.append("/home/kimi/.local/lib/python3.12/site-packages")
import numpy as np
from collections import Counter
from caveclient.auth import AuthClient
from caveclient.materializationengine import MaterializationClient

S = "/mnt/agents/output/simh1_work"
os.makedirs(S+"/mparts", exist_ok=True)
samp = json.load(open(S+"/microns_sample_seed45.json"))
sample = samp["sample"]; version = samp["version"]
m = json.load(open(S+"/microns_celltypes.json"))
typed = set(int(k) for k in m["cls"].keys())

done_path = S+"/microns_done.json"
def get_done(): return set(json.load(open(done_path))) if os.path.exists(done_path) else set()
def mark_done(b):
    d = get_done(); d.add(b); json.dump(sorted(d), open(done_path,"w"))
def st(**kw):
    try:
        d = json.load(open(S+"/microns_status.json")) if os.path.exists(S+"/microns_status.json") else {}
        d.update(kw); json.dump(d, open(S+"/microns_status.json","w"))
    except Exception: pass

B = 100
batches = [sample[i:i+B] for i in range(0, len(sample), B)]
q = queue.Queue()
for bi, b in enumerate(batches):
    if bi not in get_done(): q.put((bi, b))
st(total_batches=len(batches), pending=q.qsize())

def worker(wid):
    auth = AuthClient(token="31b36cc83e079c03fc7c44f939231425")
    mc = MaterializationClient(server_address="https://minnie.microns-daf.com",
                               datastack_name="minnie65_public", auth_client=auth, version=version)
    while True:
        try: bi, batch = q.get_nowait()
        except queue.Empty: return
        t0 = time.time()
        try:
            with warnings.catch_warnings(record=True) as wlist:
                warnings.simplefilter("always")
                df = mc.query_table("synapses_pni_2",
                                    filter_in_dict={"post_pt_root_id": [int(x) for x in batch]},
                                    select_columns=["pre_pt_root_id","post_pt_root_id"])
            trunc = any("Limited query" in str(w.message) for w in wlist)
            if trunc:
                st(truncated_batch=bi, rows=len(df)); q.put((bi, batch)); time.sleep(5); continue
            pairs = Counter()
            for p_, q_ in zip(df["pre_pt_root_id"].to_numpy(), df["post_pt_root_id"].to_numpy()):
                if p_ in typed: pairs[(int(p_), int(q_))] += 1
            with open(S+f"/mparts/batch_{bi:04d}.csv","w") as f:
                f.write("pre,post,n\n")
                for (p_,q_),n in pairs.items(): f.write(f"{p_},{q_},{n}\n")
            mark_done(bi)
            st(last_batch=bi, done=len(get_done()), rows=len(df), wall=round(time.time()-t0,1))
        except Exception as e:
            st(err_batch=bi, err=repr(e)[:120]); q.put((bi, batch)); time.sleep(15)

ths = [threading.Thread(target=worker, args=(i,), daemon=True) for i in range(4)]
[t.start() for t in ths]
[t.join() for t in ths]
st(finished=time.time())
