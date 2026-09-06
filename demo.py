import csv, json
from pathlib import Path
from model import Cell, Inputs

def run(jam=False):
    c=Cell(); rows=[]
    for k in range(300):
        rows.append(c.step(Inputs(start=k in (0,150),part_present=True,
            jam=jam and 25<=k<35,reset=jam and k==60)))
    return rows

if __name__=='__main__':
    out=Path('results'); out.mkdir(exist_ok=True)
    summary={}
    for name,jam in [('nominal',False),('jam_recovery',True)]:
        rows=run(jam)
        with (out/(name+'.csv')).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
        summary[name]={'completed_parts':rows[-1]['count'],
            'fault_scans':sum(r['state']=='FAULT' for r in rows),
            'final_state':rows[-1]['state']}
    summary['evidence']='Synthetic discrete-time model; not PLC or drive measurements'
    (out/'metrics.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
