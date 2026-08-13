from __future__ import annotations
import time,statistics,json,platform,os
from adgl import __version__ as TOOLKIT_VERSION, SPEC_VERSION
from pathlib import Path
from adgl.pipeline import PipelineEngine

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'benchmarks'/'results'/'pipeline_results.json'

def base_policy(disposition):
    consequence={'default':disposition}
    if disposition=='DECIDE': consequence={'rules':[{'when':{'analysis.result.risk':'high'},'disposition':'DECIDE','decision_owner':'reviewer'}]}
    if disposition=='ACT': consequence={'rules':[{'when':{'analysis.result.eligible':True},'disposition':'ACT','action':{'type':'api.write'},'executor':'api'}]}
    return {'knowledge_policy':{'adgl':{'version':'0.3'},'policy':{'id':f'pipe-{disposition}','version':1},'case':{'id':'pipeline-benchmark'},'rules':[{'id':'q','select':{'status':'draft'},'do':[{'quarantine':{}}]}],'decision':{'default':'PERMITTED'},'audit':{'required':True}},'analysis':{'method':'CLASSIFY','allowed_methods':['CLASSIFY'],'min_evidence':1},'consequence':consequence}

def data(n,disp):
    d={'objects':[{'id':f'o{i}','status':'approved','provenance_status':'verified'} for i in range(n)],'analysis_result':{'confidence':0.98,'uses_inferred_missing':False}}
    if disp=='DECIDE': d['analysis_result']['risk']='high'
    if disp=='ACT':
        d['analysis_result']['eligible']=True; d['capability_grant']={'id':'g','actions':['api.write'],'case_id':'pipeline-benchmark'}
    return d

def pct(vals,p):
    xs=sorted(vals); k=(len(xs)-1)*p/100; f=int(k); c=min(f+1,len(xs)-1); return xs[f] if f==c else xs[f]*(c-k)+xs[c]*(k-f)

def main():
    rows=[]
    for disp in ['INFORM','DECIDE','ACT']:
        e=PipelineEngine(base_policy(disp)); d=data(1000,disp)
        for _ in range(3): e.run(d)
        vals=[]
        for _ in range(20):
            t=time.perf_counter_ns(); e.run(d); vals.append((time.perf_counter_ns()-t)/1e6)
        q1,q3=pct(vals,25),pct(vals,75)
        rows.append({'disposition':disp,'objects':1000,'iterations':20,'median_ms':pct(vals,50),'q1_ms':q1,'q3_ms':q3,'iqr_ms':q3-q1,'mean_ms':statistics.fmean(vals)})
    payload={'environment':{'toolkit_version':TOOLKIT_VERSION,'spec_version':SPEC_VERSION,'python':platform.python_version(),'platform':platform.platform(),'cpu_count':os.cpu_count()},'scope':'three-stage reference pipeline; excludes model inference, retrieval, connector I/O and external action execution','results':rows}
    OUT.write_text(json.dumps(payload,indent=2),encoding='utf-8'); print(json.dumps(payload,indent=2))
if __name__=='__main__': main()
