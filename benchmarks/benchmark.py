from __future__ import annotations
import csv,json,statistics,time,argparse,platform,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
from adgl.engine import Engine
from adgl import __version__
ROOT=Path(__file__).resolve().parents[1]; RESULTS=ROOT/'benchmarks'/'results'

def policy_with_rules(total_rules):
    rules=[]
    if total_rules>=1: rules.append({'id':'exclude-draft','select':{'status':'draft'},'do':[{'exclude':{}}]})
    if total_rules>=2: rules.append({'id':'quarantine-unknown','select':{'provenance_status':'unknown'},'do':[{'quarantine':{}}]})
    for i in range(max(0,total_rules-len(rules))):
        rules.append({'id':f'r{i}','select':{'category':f'c{i%10}'},'do':[{'prioritize':{'rank':i}}]})
    assert len(rules)==total_rules
    return {'adgl':{'version':'0.3'},'policy':{'id':f'bench-{total_rules}','version':1},'case':{'id':'benchmark','purpose':'performance'},'rules':rules,'decision':{'default':'PERMITTED'},'audit':{'required':True}}

def data_with_objects(n):
    return {'objects':[{'id':f'o{i}','type':'record','category':f'c{i%10}','status':'draft' if i%23==0 else 'approved','provenance_status':'unknown' if i%31==0 else 'verified','authority':'organizational','applicability':'applicable'} for i in range(n)]}

def percentile(vals,p):
    xs=sorted(vals); k=(len(xs)-1)*p/100; f=int(k); c=min(f+1,len(xs)-1)
    return xs[f] if f==c else xs[f]*(c-k)+xs[c]*(k-f)

def measure(engine,data,iterations,warmup=3):
    for _ in range(warmup): engine.run(data)
    vals=[]
    for _ in range(iterations):
        t=time.perf_counter_ns(); engine.run(data); vals.append((time.perf_counter_ns()-t)/1e6)
    q1,q3=percentile(vals,25),percentile(vals,75)
    return {'iterations':iterations,'mean_ms':statistics.fmean(vals),'stdev_ms':statistics.stdev(vals) if len(vals)>1 else 0.0,'p50_ms':percentile(vals,50),'p95_ms':percentile(vals,95),'q1_ms':q1,'q3_ms':q3,'iqr_ms':q3-q1,'min_ms':min(vals),'max_ms':max(vals)}

def env_meta():
    cpu='unknown'; mem='unknown'
    try:
        for line in Path('/proc/cpuinfo').read_text().splitlines():
            if line.lower().startswith('model name'): cpu=line.split(':',1)[1].strip(); break
    except Exception: pass
    try:
        for line in Path('/proc/meminfo').read_text().splitlines():
            if line.startswith('MemTotal:'): mem=line.split(':',1)[1].strip(); break
    except Exception: pass
    try: commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()
    except Exception: commit='uncommitted-artifact'
    return {'timestamp_utc':datetime.now(timezone.utc).isoformat(),'toolkit_version':__version__,'spec_version':'0.3.0','python_version':platform.python_version(),'platform':platform.platform(),'machine':platform.machine(),'logical_cpu_count':os.cpu_count(),'cpu_model':cpu,'memory_total':mem,'git_commit':commit}

def worker(objects,rules,iterations):
    return {'objects':objects,'rules':rules,**measure(Engine(policy_with_rules(rules)),data_with_objects(objects),iterations)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--iterations',type=int,default=50); ap.add_argument('--worker',action='store_true'); ap.add_argument('--objects',type=int); ap.add_argument('--rules',type=int); ap.add_argument('--worker-iterations',type=int)
    args=ap.parse_args()
    if args.worker:
        print(json.dumps(worker(args.objects,args.rules,args.worker_iterations)))
        return
    RESULTS.mkdir(parents=True,exist_ok=True)
    workloads=[]
    for n in [10,100,1000,5000]: workloads.append(('objects',n,10,args.iterations if n<5000 else max(12,args.iterations//2)))
    for r in [0,5,25,100,150]: workloads.append(('rules',1000,r,args.iterations if r<150 else max(12,args.iterations//2)))
    rows=[]
    for dim,n,r,it in workloads:
        out=subprocess.check_output([sys.executable,str(Path(__file__).resolve()),'--worker','--objects',str(n),'--rules',str(r),'--worker-iterations',str(it)],cwd=ROOT,env={**os.environ,'PYTHONPATH':str(ROOT)},text=True)
        m=json.loads(out); rows.append({'dimension':dim,**m}); print(dim,n,r,it,round(m['p50_ms'],3),round(m['p95_ms'],3),flush=True)
    fields=list(rows[0].keys())
    with (RESULTS/'benchmark_results.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    payload={'environment':env_meta(),'method':{'warmup_runs_per_workload':3,'default_measured_runs':args.iterations,'large_workload_runs':max(12,args.iterations//2),'percentiles_reported':['p50','p95'],'dispersion':['standard deviation','IQR'],'isolation':'each workload executed in a fresh Python subprocess','scope':'governance engine only; excludes retrieval, network, model inference, token generation, connector I/O and external persistence'},'results':rows}
    (RESULTS/'benchmark_results.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    (RESULTS/'environment.json').write_text(json.dumps(payload['environment'],indent=2),encoding='utf-8')
    print(json.dumps(payload,indent=2))
if __name__=='__main__': main()
