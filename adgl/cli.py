import argparse,json,sys,yaml
from pathlib import Path
from .compiler import compile_policy,PolicyError,load_policy
from .engine import Engine
from .pipeline import PipelineEngine
from .validation import validate_pipeline_policy,RuntimeValidationError
from .conformance import run_conformance

def _reject_nonfinite(value):
    raise RuntimeValidationError(f"input JSON contains non-finite numeric constant: {value}")

def _load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'), parse_constant=_reject_nonfinite)

def main(argv=None):
    ap=argparse.ArgumentParser(prog='adgl');sp=ap.add_subparsers(dest='cmd',required=True)
    v=sp.add_parser('validate');v.add_argument('policy')
    r=sp.add_parser('run');r.add_argument('policy');r.add_argument('--input',required=True);r.add_argument('--out')
    p=sp.add_parser('pipeline');p.add_argument('policy');p.add_argument('--input',required=True);p.add_argument('--out')
    sp.add_parser('conformance')
    a=ap.parse_args(argv)
    try:
        if a.cmd=='validate':
            raw=load_policy(a.policy)
            if isinstance(raw,dict) and 'knowledge_policy' in raw:
                validate_pipeline_policy(raw)
                print('VALID PIPELINE POLICY')
                print(json.dumps({'knowledge_policy': compile_policy(raw['knowledge_policy']), 'analysis':raw.get('analysis',{}), 'consequence':raw.get('consequence',{})},indent=2))
            else:
                print('VALID')
                print(json.dumps(compile_policy(raw),indent=2))
        elif a.cmd=='run':
            result=Engine(a.policy).run(_load_json(a.input));text=json.dumps(result,indent=2,allow_nan=False)
            if a.out:Path(a.out).write_text(text,encoding='utf-8')
            print(text)
        elif a.cmd=='pipeline':
            raw=load_policy(a.policy); validate_pipeline_policy(raw)
            result=PipelineEngine(raw).run(_load_json(a.input)); text=json.dumps(result,indent=2,allow_nan=False)
            if a.out:Path(a.out).write_text(text,encoding='utf-8')
            print(text)
        else:sys.exit(0 if run_conformance() else 1)
    except PolicyError as e:
        print('INVALID POLICY'); print(e); sys.exit(2)
    except RuntimeValidationError as e:
        print('INVALID INPUT OR POLICY'); print(e); sys.exit(2)
if __name__=='__main__':main()
