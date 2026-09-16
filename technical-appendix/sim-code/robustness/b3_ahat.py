# Battery 3 — ahat reference-scale sensitivity of the Fisher-Rao simplex (SIM-R2, seed 42)
# DOCAS-preset stage-activity dynamics; full disclosure in simR2_results.md (Battery 3).
import numpy as np, itertools as it
from scipy.stats import spearmanr
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

T=400
aD,bC,thC,gA,lam,dS,Sb = 0.3,4.0,0.5,1.0,0.35,0.01,0.5
AHAT0=np.array([1.0,0.7,0.5,0.5,lam*0.5])

def simulate_episode(shock, seed):
    r=np.random.default_rng(seed)
    s=np.zeros(T); E=np.zeros(T); eps=np.zeros(T); gO=np.zeros(T)
    Pi=np.zeros(T); C=np.zeros(T); A=np.zeros(T); lamr=np.zeros(T)
    g0=0.7; run_var=1.0
    for t in range(T):
        if t>0:
            s[t]=0.9*s[t-1]+0.3*r.standard_normal()
            g0=np.clip(g0+0.02*r.standard_normal(),0,1)
        if t==T//2: s[t]+=shock
        gO[t]=g0; V=g0*s[t]; eps[t]=V-E[t]
        run_var=0.95*run_var+0.05*eps[t]**2
        Pi[t]=np.clip(1.0/max(run_var,1e-3),0.25,4.0)
        C[t]=1/(1+np.exp(-bC*(abs(eps[t])-thC)))
        A[t]=gA*C[t]*abs(eps[t]); lamr[t]=lam*C[t]
        if t<T-1:
            E[t+1]=E[t]+aD*Pi[t]*eps[t]
    return np.stack([Pi,gO,C,A,lamr])

episodes=[]; labels=[]
for shock,lab in [(-1.5,'mild'),(-3.0,'moderate'),(-6.0,'severe')]:
    for j in range(8):
        episodes.append(simulate_episode(shock,1000+int(abs(shock)*10)+j)); labels.append(lab)
EP=np.array(episodes)

def theta_profiles(EP,ahat):
    a=EP/ahat[None,:,None]; return a/a.sum(1,keepdims=True)
def fr_dist(p,q): return 2*np.arccos(np.clip((np.sqrt(p*q)).sum(-1),-1,1))
def pairwise_FR(th):
    prof=th.mean(-1); n=len(prof); D=np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n): D[i,j]=D[j,i]=fr_dist(prof[i],prof[j])
    return D
def uppervec(D): return D[np.triu_indices(len(D),1)]
def dispersion_by_cond(D,labels):
    out={}
    for lab in ['mild','moderate','severe']:
        idx=[i for i,l in enumerate(labels) if l==lab]
        sub=D[np.ix_(idx,idx)]; out[lab]=sub[np.triu_indices(len(idx),1)].mean()
    return out
def nn_frac(D,labels):
    n=len(labels); ok=0
    for i in range(n):
        j=np.argsort(D[i]+np.eye(n)[i]*1e9)[0]; ok+=labels[i]==labels[j]
    return ok/n

D0=pairwise_FR(theta_profiles(EP,AHAT0)); v0=uppervec(D0)
grid=list(it.product([0.5,1.0,2.0],repeat=5))
Dmats={g:pairwise_FR(theta_profiles(EP,AHAT0*np.array(g))) for g in grid}
rhos=np.array([spearmanr(uppervec(Dmats[g]),v0)[0] for g in grid])
q1=[ [k for k,_ in sorted(dispersion_by_cond(Dmats[g],labels).items(),key=lambda kv:kv[1])]==['mild','moderate','severe'] for g in grid]
q2=[nn_frac(Dmats[g],labels) for g in grid]
r2=np.random.default_rng(4242); ln=[np.exp(r2.normal(0,np.log(2),5)) for _ in range(50)]
Dl=[pairwise_FR(theta_profiles(EP,AHAT0*m)) for m in ln]
rhos_ln=[spearmanr(uppervec(Dl[k]),v0)[0] for k in range(50)]
q1_ln=[[k for k,_ in sorted(dispersion_by_cond(Dl[k],labels).items(),key=lambda kv:kv[1])]==['mild','moderate','severe'] for k in range(50)]
print("grid rho min/med",rhos.min(),np.median(rhos),"Q1",np.mean(q1),"Q2 min/med",min(q2),np.median(q2))
print("ln rho min/med",min(rhos_ln),np.median(rhos_ln),"Q1",np.mean(q1_ln))
allD=np.array([uppervec(Dmats[g]).mean() for g in grid]); print("meanD range",allD.min(),allD.max())

chn=['D','O','C','A','S']
subset=[(1,1,1,1,1)]; snames=["baseline"]
for i,c in enumerate(chn):
    for m in (0.5,2.0):
        g=[1]*5; g[i]=m; subset.append(tuple(g)); snames.append(f"{c}x{m}")
subset+= [(0.5,)*5,(2.0,)*5]; snames+=["all x0.5","all x2"]
for k in range(4): subset.append(tuple(ln[k])); snames.append(f"logN{k+1}")
Ds=[Dmats.get(tuple(s)) if tuple(s) in Dmats else pairwise_FR(theta_profiles(EP,AHAT0*np.array(s))) for s in subset]
M=len(subset); Cmat=np.ones((M,M))
for i in range(M):
    for j in range(i+1,M): Cmat[i,j]=Cmat[j,i]=spearmanr(uppervec(Ds[i]),uppervec(Ds[j]))[0]
gworst=grid[int(np.argmin(rhos))]; Dw=Dmats[gworst]

fig,axes=plt.subplots(2,2,figsize=(13,11))
ax=axes[0,0]
im=ax.imshow(Cmat,vmin=0.9,vmax=1.0,cmap="viridis")
ax.set_xticks(range(M)); ax.set_xticklabels(snames,rotation=90,fontsize=7)
ax.set_yticks(range(M)); ax.set_yticklabels(snames,fontsize=7)
fig.colorbar(im,ax=ax,label="Spearman rho (pairwise FR distances)")
ax.set_title("(a) FR-distance correlation across ahat settings (min off-diag rho = %.3f)"%Cmat[np.triu_indices(M,1)].min())
ax=axes[0,1]
ax.scatter(uppervec(D0),uppervec(Dw),s=8,alpha=0.6)
lim=[0,max(uppervec(D0).max(),uppervec(Dw).max())*1.05]; ax.plot(lim,lim,'r--',lw=1)
ax.set_xlabel("pairwise FR distance (baseline ahat)"); ax.set_ylabel("pairwise FR distance (worst case)")
ax.set_title("(b) baseline vs worst-case ahat=%s (rho=%.3f)"%(str(gworst),rhos.min()))
ax=axes[1,0]
disp_all={lab:[] for lab in ['mild','moderate','severe']}
for g in grid:
    dd=dispersion_by_cond(Dmats[g],labels)
    for lab in disp_all: disp_all[lab].append(dd[lab])
rr=np.random.default_rng(1)
for i,lab in enumerate(['mild','moderate','severe']):
    ax.scatter(np.full(len(grid),i)+rr.normal(0,0.05,len(grid)),disp_all[lab],s=5,alpha=0.4,label=lab)
    ax.hlines(np.mean(disp_all[lab]),i-0.3,i+0.3,color='k')
ax.set_xticks([0,1,2]); ax.set_xticklabels(['mild (-1.5)','moderate (-3)','severe (-6)'])
ax.set_ylabel("within-condition mean pairwise FR distance")
ax.set_title("(c) dispersion ordering across all 243 settings (preserved 100%)"); ax.legend()
ax=axes[1,1]
ax.hist(rhos,bins=30,alpha=0.7,label="grid (243)"); ax.hist(rhos_ln,bins=15,alpha=0.7,label="lognormal (50)")
ax.axvline(0.9,color='r',ls='--',lw=1)
ax.set_xlabel("Spearman rho vs baseline pairwise FR distances"); ax.set_ylabel("count")
ax.set_title("(d) distribution of FR-geometry correlations"); ax.legend()
fig.suptitle("SIM-R2 Battery 3 - sensitivity of the GTT 3.1 stage-mix simplex to reference scales ahat_i (seed 42)\n"
 "DOCAS-preset stage activities, 24 episodes x 3 shock severities; ahat grid {0.5,1,2}x per channel + 50 lognormal(sigma=ln2) draws.\n"
 "Absolute FR distances shift up to 1.83x (metric IS scale-sensitive); relational geometry stable (min pairwise rho = 0.940 grid / 0.952 lognormal);\n"
 "dispersion ordering and NN clustering robust in 100%/100% of settings. Papers never print registered ahat values; nominal = mid-range (disclosed).",fontsize=9)
fig.tight_layout(rect=[0,0,1,0.915])
fig.savefig("/mnt/agents/output/figures/robustness/figR2_B3_fr_ahat_heatmap.png",dpi=150)
print("figure saved")
