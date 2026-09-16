"""Shell-lane H01 shard processor: processes next-undone shards within a time
budget. Cooperative with the kernel worker via the shared done-list.
Usage: python3 h01_shell_lane.py <budget_seconds>"""
import json, os, sys, time, subprocess, urllib.request
from collections import Counter

sys.path.append('/home/kimi/.local/lib/python3.12/site-packages')
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 170
T0 = time.time()
OUT = '/mnt/agents/output/simh1_work'
TMP = '/tmp/h01sh'
os.makedirs(TMP, exist_ok=True)
os.makedirs(OUT + '/parts', exist_ok=True)

try:
    import fastavro
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', '-q', 'install', '--no-index',
                    '--find-links', '/mnt/agents/output/simh1_work/wheels',
                    'fastavro'], capture_output=True)
    import fastavro

shards = json.load(open(OUT + '/h01_shard_list.json'))
cells = json.load(open(OUT + '/h01_cell_data.json'))
typed = set(int(c['agglo_seg']) for c in cells)
done_path = OUT + '/h01_done.json'

def get_done():
    return set(json.load(open(done_path))) if os.path.exists(done_path) else set()

def mark_done(tag):
    d = get_done(); d.add(tag)
    json.dump(sorted(d), open(done_path, 'w'))

done0 = len(get_done())
processed = []
for name, size in shards:
    tag = name.rsplit('/', 1)[-1]
    if time.time() - T0 > BUDGET:
        break
    if tag in get_done():
        continue
    local = TMP + '/work.avro'
    ok = False
    for attempt in range(2):
        try:
            urllib.request.urlretrieve(
                'https://h01-release.storage.googleapis.com/' + name, local)
            ok = os.path.getsize(local) == size
            if ok:
                break
        except Exception:
            pass
    if not ok:
        continue
    pairs = Counter(); posttot = Counter()
    with open(local, 'rb') as f:
        for rec in fastavro.reader(f):
            t = rec['type']
            post = rec['post_synaptic_partner']['neuron_id']
            if post in typed:
                posttot[(post, t)] += 1
                pre = rec['pre_synaptic_site']['neuron_id']
                if pre in typed:
                    pairs[(pre, post, t)] += 1
    if not os.path.exists(OUT + '/parts/pairs_' + tag + '.csv'):
        agg = {}
        for (pre, post, t), n in pairs.items():
            a = agg.setdefault((pre, post), [0, 0]); a[t - 1] += n
        with open(OUT + '/parts/pairs_' + tag + '.csv', 'w') as f:
            f.write('pre,post,t1,t2\n')
            for (pre, post), (a, b) in agg.items():
                f.write(f'{pre},{post},{a},{b}\n')
        agg2 = {}
        for (post, t), n in posttot.items():
            a = agg2.setdefault(post, [0, 0]); a[t - 1] += n
        with open(OUT + '/parts/posttot_' + tag + '.csv', 'w') as f:
            f.write('post,t1,t2\n')
            for post, (a, b) in agg2.items():
                f.write(f'{post},{a},{b}\n')
    mark_done(tag)
    os.remove(local)
    processed.append(tag)
print(f'SHELL_LANE: processed {len(processed)} shards {processed[:5]} '
      f'| done now {len(get_done())}/166 (was {done0}) | {time.time()-T0:.0f}s')
