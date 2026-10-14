#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, importlib.util, json, urllib.request, io
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.graphics.tsaplots import plot_acf

EXPECTED_RAW='fd0e874c6c7766fec60bd7c4f2b697ace85e0d558bba33a9dc2fad29b8ef3801'
EXPECTED_CSV='8211344ec98cff4287496c3daeadd7217c586d18d6b2ca68fe5bb856efd7e7dc'
H=3
ROOT=Path('SmartHome_Corrected_usekW_Reruns_2026-08-20')
AR=ROOT/'ARIMA'; HW=ROOT/'HoltWinters'
for d in (ROOT,AR,HW): d.mkdir(parents=True,exist_ok=True)

# Use the repository's provenance-checked reconstruction first; fall back to a public HomeC copy.
def reconstruct():
    p=Path('datasets/smart-home-energy/preprocess_smart_home.py')
    spec=importlib.util.spec_from_file_location('smartprep',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    try:
        rows, raw_sha, used=m.fetch_and_aggregate()
        return rows,raw_sha,used
    except Exception as first:
        source='https://raw.githubusercontent.com/MihaiNastase/MongoDB-IoT-Application/main/DataSetup/Data/Home.csv'
        vals=[]; times=[]; dg=hashlib.sha256()
        req=urllib.request.Request(source,headers={'User-Agent':'ML2PP-repro/1.0'})
        with urllib.request.urlopen(req,timeout=180) as r:
            rd=csv.DictReader(io.TextIOWrapper(r,encoding='utf-8-sig',newline=''))
            for row in rd:
                if len(vals)>=252000: break
                t=int(float(row['time'])); v=float(row['use [kW]'])
                if times and t!=times[-1]+1: raise RuntimeError(f'nonconsecutive time {times[-1]}->{t}')
                times.append(t); vals.append(v); dg.update(f'{t},{v!r}\n'.encode())
        if len(vals)!=252000: raise RuntimeError(f'fallback source returned only {len(vals)} rows') from first
        rows=[]
        for i in range(0,252000,60):
            s=0.0
            for v in vals[i:i+60]: s+=v
            ts=datetime.fromtimestamp(times[i],tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            rows.append((ts,s/60))
        return rows,dg.hexdigest(),source

rows,raw_sha,source=reconstruct()
if raw_sha!=EXPECTED_RAW: raise RuntimeError(f'raw SHA mismatch: {raw_sha}')
dataset=ROOT/'use_case_2_smart_home_energy.csv'
with dataset.open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f,lineterminator='\n'); w.writerow(['timestamp','use_kW'])
    for t,v in rows: w.writerow([t,repr(v)])
csv_sha=hashlib.sha256(dataset.read_bytes()).hexdigest()
if csv_sha!=EXPECTED_CSV: raise RuntimeError(f'dataset SHA mismatch: {csv_sha}')

df=pd.DataFrame(rows,columns=['timestamp','use_kW']); df['timestamp']=pd.to_datetime(df.timestamp,utc=True)
y=df.use_kW.astype(float).reset_index(drop=True)
stats={'rows':len(y),'start':str(df.timestamp.iloc[0]),'end':str(df.timestamp.iloc[-1]),'min':float(y.min()),'max':float(y.max()),'mean':float(y.mean()),'raw_pairs_sha256':raw_sha,'dataset_sha256':csv_sha,'source_used':source}
(ROOT/'dataset_validation.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
assert len(y)==4200 and abs(stats['min']-0.0008)<1e-9 and abs(stats['max']-4.302675)<1e-9 and abs(stats['mean']-0.775213)<1e-6
train=y.iloc[:3360].copy(); test=y.iloc[3360:].copy(); assert len(test)==840

def met(a,p):
    a=np.asarray(a,float); p=np.asarray(p,float); m=np.isfinite(a)&np.isfinite(p); a=a[m];p=p[m]; e=a-p
    mse=float(np.mean(e*e)); mae=float(np.mean(np.abs(e))); rmse=float(np.sqrt(mse)); ss=float(np.sum((a-a.mean())**2)); r2=float(1-np.sum(e*e)/ss)
    return {'N':int(len(a)),'MAE':mae,'RMSE':rmse,'MSE':mse,'R2':r2}

def save(name,d,truth,pred,extra):
    truth=np.asarray(truth); pred=np.asarray(pred); by=[]
    for h in range(H):
        mm=met(truth[:,h],pred[:,h]); by.append({'Horizon':f't+{h+1}',**mm})
        pd.DataFrame({'Actual':truth[:,h],'Forecast':pred[:,h],'Error':truth[:,h]-pred[:,h]}).to_csv(d/f'forecast_values_horizon_t_plus_{h+1:02d}.csv',index_label='Sample')
        fig,ax=plt.subplots(figsize=(12,6)); x=np.arange(len(truth)); ax.plot(x,truth[:,h],label='Actual'); ax.plot(x,pred[:,h],label='Forecast'); ax.set_title(f'{name}: forecast vs actual, t+{h+1}'); ax.set_xlabel('Held-out forecast origin'); ax.set_ylabel('use_kW'); ax.legend(); fig.tight_layout(); fig.savefig(d/f'forecast_vs_actual_horizon_t_plus_{h+1:02d}.png',dpi=200,bbox_inches='tight'); plt.close(fig)
    pd.DataFrame(by).to_csv(d/'forecast_metrics_by_horizon.csv',index=False)
    out={'model':name,'train_rows':3360,'test_rows':840,'forecast_origins':838,'horizon':3,'overall':met(truth.reshape(-1),pred.reshape(-1)),'by_horizon':by,'dataset_sha256':csv_sha,**extra}
    (d/'model_evaluation.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); return out

# ARIMA: exact rolling-origin semantics of the retained generated script.
af=ARIMA(train,order=(1,1,1),seasonal_order=(0,0,0,0),trend='n').fit(); state=af; pp=[]; tt=[]
for o in range(838):
    pp.append(np.asarray(state.forecast(steps=3),float)); tt.append(test.iloc[o:o+3].to_numpy(float))
    if o<len(test)-1: state=state.append(test.iloc[o:o+1],refit=False)
ar=save('ARIMA(1,1,1)',AR,np.vstack(tt),np.vstack(pp),{'trend':'n','protocol':'rolling-origin; fitted parameters fixed; observed test values appended without refit'})
(AR/'fitted_parameters.json').write_text(json.dumps({k:float(v) for k,v in zip(af.param_names,af.params)},indent=2),encoding='utf-8')

# Holt-Winters: exact fixed-smoothing-parameter rolling-origin semantics of retained generated script.
hm=ExponentialSmoothing(train,trend='add',damped_trend=True,seasonal='add',seasonal_periods=60,initialization_method='heuristic',use_boxcox=False)
hf=hm.fit(optimized=True,remove_bias=False); pars=dict(hf.params); hist=pd.Series(train).copy(); pp=[];tt=[]
for o in range(838):
    if o==0: st=hf
    else:
        base=hf.model; mm=ExponentialSmoothing(hist,trend=getattr(base,'trend',None),damped_trend=getattr(base,'damped_trend',False),seasonal=getattr(base,'seasonal',None),seasonal_periods=getattr(base,'seasonal_periods',None),initialization_method='estimated')
        st=mm.fit(smoothing_level=pars.get('smoothing_level'),smoothing_trend=pars.get('smoothing_trend'),smoothing_seasonal=pars.get('smoothing_seasonal'),damping_trend=pars.get('damping_trend'),optimized=False)
    pp.append(np.asarray(st.forecast(3),float)); tt.append(test.iloc[o:o+3].to_numpy(float)); hist=pd.concat([hist,test.iloc[o:o+1]])
hw=save('Holt-Winters additive damped',HW,np.vstack(tt),np.vstack(pp),{'seasonal_periods':60,'protocol':'rolling-origin; smoothing parameters fixed after initial optimization'})

fig,ax=plt.subplots(figsize=(12,5)); ax.plot(np.arange(len(y)),y.to_numpy()); ax.set_title('Corrected smart-home use_kW series'); ax.set_xlabel('Minute index'); ax.set_ylabel('use_kW'); fig.tight_layout(); fig.savefig(HW/'line_use_kW.png',dpi=200,bbox_inches='tight'); plt.close(fig)
fig,ax=plt.subplots(figsize=(12,5)); plot_acf(y,lags=120,ax=ax); ax.set_title('Autocorrelation of corrected use_kW'); fig.tight_layout(); fig.savefig(HW/'acf_use_kW.png',dpi=200,bbox_inches='tight'); plt.close(fig)

pd.DataFrame([{'Model':ar['model'],**ar['overall']},{'Model':hw['model'],**hw['overall']}]).to_csv(ROOT/'combined_overall_metrics.csv',index=False)
pd.DataFrame([{'Model':r['model'],**h} for r in (ar,hw) for h in r['by_horizon']]).to_csv(ROOT/'combined_metrics_by_horizon.csv',index=False)
tex=['% Corrected smart-home use_kW rerun','\\begin{table}[!ht]','\\centering','\\caption{Corrected smart-home forecasting performance on the held-out partition.}','\\begin{tabular}{llrrrrr}','\\toprule','Model & Horizon & $N$ & MAE & RMSE & MSE & $R^2$ \\\\','\\midrule']
for r in (ar,hw):
    for h in r['by_horizon']: tex.append(f"{r['model']} & {h['Horizon']} & {h['N']} & {h['MAE']:.6f} & {h['RMSE']:.6f} & {h['MSE']:.6f} & {h['R2']:.6f} \\\\")
tex+=['\\bottomrule','\\end{tabular}','\\end{table}']; (ROOT/'CHAPTER5_SMARTHOME_RESULTS.tex').write_text('\n'.join(tex)+'\n',encoding='utf-8')
summary=f"""# Corrected Smart-Home use_kW rerun\n\nDataset SHA-256: `{csv_sha}`  \nRaw selected-pairs SHA-256: `{raw_sha}`  \nRows: 4200; train: 3360; test: 840; complete rolling origins: 838; horizon: 3.\n\n- ARIMA overall RMSE: {ar['overall']['RMSE']:.9f}; MAE: {ar['overall']['MAE']:.9f}; R2: {ar['overall']['R2']:.9f}; N: {ar['overall']['N']}\n- Holt-Winters overall RMSE: {hw['overall']['RMSE']:.9f}; MAE: {hw['overall']['MAE']:.9f}; R2: {hw['overall']['R2']:.9f}; N: {hw['overall']['N']}\n\nEvaluation reproduces the rolling-origin semantics in the retained ML2++ generated scripts. This is a generator-faithful Python rerun, not a fresh Java/Maven compiler invocation.\n"""
(ROOT/'RUN_SUMMARY.md').write_text(summary,encoding='utf-8')
lines=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and p.name!='SHA256SUMS.txt': lines.append(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT)}')
(ROOT/'SHA256SUMS.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(summary)
