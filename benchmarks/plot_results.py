from pathlib import Path
import csv
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((ROOT/'benchmarks/results/benchmark_results.csv').open()))

def draw(dim,label,filename):
    rr=[r for r in rows if r['dimension']==dim]
    x=[int(r['objects'] if dim=='objects' else r['rules']) for r in rr]
    med=[float(r['p50_ms']) for r in rr]
    q1=[float(r['q1_ms']) for r in rr]
    q3=[float(r['q3_ms']) for r in rr]
    fig,ax=plt.subplots(figsize=(6.2,3.5))
    ax.plot(x,med,marker='o',label='Median')
    ax.fill_between(x,q1,q3,alpha=.2,label='IQR')
    ax.set_xlabel(label); ax.set_ylabel('Evaluation time (ms)')
    ax.set_title(f'ADGL reference runtime: {dim} scaling')
    ax.grid(True,alpha=.25); ax.legend(); fig.tight_layout()
    fig.savefig(ROOT/'benchmarks/results'/filename,dpi=180)
    plt.close(fig)

draw('objects','Candidate knowledge objects','object_scaling.png')
draw('rules','Policy rules','rule_scaling.png')
