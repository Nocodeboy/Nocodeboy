# Procedural news bed, 100 BPM, A minor (Am-F-Dm-E). Placeholder for a Magnific/licensed track.
import numpy as np, soundfile as sf
SR=48000; BPM=100; B=60/BPM; DUR=51.0; N=int(SR*DUR)
t=np.arange(N)/SR
L=np.zeros(N); R=np.zeros(N)
def midi(m): return 440*2**((m-69)/12)
def lp(x,a):  # one-pole low-pass
    y=np.empty_like(x); s=0.0
    for i in range(len(x)): s+=a*(x[i]-s); y[i]=s
    return y
def saw(f,tt): return 2*((f*tt)%1)-1
chords=[[57,60,64],[53,57,60],[50,53,57],[52,56,59]]  # Am F Dm E
bar=4*B; cl=2*bar
rng=np.random.default_rng(7)
# pad
for ci in range(int(DUR/cl)+1):
    c=chords[ci%4]; s0=ci*cl; i0=int(s0*SR); i1=min(N,int((s0+cl)*SR))
    if i0>=N: break
    tt=t[i0:i1]-s0; env=np.minimum(1,tt/1.2)*np.minimum(1,(cl-tt)/0.6)
    x=sum(saw(midi(m-12)*d,tt) for m in c for d in (0.997,1.003))/6
    L[i0:i1]+=0.09*env*x; R[i0:i1]+=0.09*env*np.roll(x,37)
padL=lp(L,0.035); padR=lp(R,0.035); L=padL.copy(); R=padR.copy()
# arp 16ths
st=B/4; k=0
while k*st<DUR:
    s0=k*st; c=chords[int(s0//cl)%4]; pat=[0,1,2,1,2,0,1,2]
    m=c[pat[k%8]]+12+(12 if k%16 in (6,14) else 0)
    i0=int(s0*SR); n=int(0.14*SR); i1=min(N,i0+n); tt=np.arange(i1-i0)/SR
    x=(saw(midi(m),tt)*0.5+np.sin(2*np.pi*midi(m)*tt))*np.exp(-tt*28)
    pan=0.5+0.35*np.sin(k*0.7)
    L[i0:i1]+=0.045*x*(1-pan)*2; R[i0:i1]+=0.045*x*pan*2; k+=1
# sub pulse 8ths on root
k=0
while k*B/2<DUR:
    s0=k*B/2; c=chords[int(s0//cl)%4]; f=midi(c[0]-24)
    i0=int(s0*SR); i1=min(N,i0+int(0.28*SR)); tt=np.arange(i1-i0)/SR
    x=np.sin(2*np.pi*f*tt)*np.exp(-tt*9)*(1.0 if k%2==0 else 0.6)
    L[i0:i1]+=0.16*x; R[i0:i1]+=0.16*x; k+=1
# ticks 16ths (clock)
k=0
while k*st<DUR:
    i0=int(k*st*SR); n=int(0.03*SR); i1=min(N,i0+n)
    x=rng.standard_normal(i1-i0); x=x-lp(x,0.5); x*=np.exp(-np.arange(i1-i0)/SR*160)
    a=0.05 if k%4==0 else 0.022
    L[i0:i1]+=a*x; R[i0:i1]+=a*x*0.8; k+=1
# boom every 4 bars from the ident hit (3.2 s)
for s0 in [3.2]+list(np.arange(3.2+4*bar,DUR,4*bar)):
    i0=int(s0*SR); i1=min(N,i0+int(1.4*SR)); tt=np.arange(i1-i0)/SR
    f=60*np.exp(-tt*1.5)+32; ph=2*np.pi*np.cumsum(f)/SR
    x=np.sin(ph)*np.exp(-tt*3.2); L[i0:i1]+=0.35*x; R[i0:i1]+=0.35*x
# fade in/out
env=np.minimum(1,t/0.8)*np.minimum(1,(DUR-t)/2.5)
st=np.stack([L*env,R*env],1); st/=np.max(np.abs(st))*1.12
sf.write("Sources/music/news-bed-procedural.wav",st.astype(np.float32),SR,subtype="PCM_24")
print("ok",DUR)
