"""Original layered spell audio, mono spatial sounds with short controlled tails."""
import json, subprocess, wave
import numpy as np
from scipy.signal import butter, sosfilt

def build(rp,out):
    rate=44100;rng=np.random.default_rng(193)
    durations={'slash':.48,'shunpo':.38,'charge':1.05,'release':1.3,'transform':1.6,'mugetsu':2.2,'cero':1.1,'impact':.65}
    sounds={}
    for name,dur in durations.items():
        t=np.arange(int(rate*dur))/rate;u=t/dur
        noise=rng.normal(0,1,len(t))
        low=sosfilt(butter(2,420,fs=rate,output='sos'),noise)
        high=noise-sosfilt(butter(2,1900,fs=rate,output='sos'),noise)
        if name=='charge':
            phase=2*np.pi*(65*t+220*t*t/dur)
            env=np.sin(np.minimum(u/.9,1)*np.pi/2)**1.6*(1-u**9)
            s=env*(.35*np.sin(phase)+.14*np.sin(phase*2.005)+.05*high+.3*low)
        elif name in ['release','transform','mugetsu','impact']:
            env=(1-np.exp(-t*170))*np.exp(-t*(3.7 if name=='impact' else 2.6))
            phase=2*np.pi*(38*t+45*(1-np.exp(-t*10))/10)
            s=env*(.5*np.sin(phase)+.45*low+.10*high)
            s+=.08*np.sin(2*np.pi*146*t)*np.exp(-t*2)*np.sin(np.pi*u)
        elif name=='cero':
            phase=2*np.pi*(190*t-60*t*t/dur)
            env=(1-np.exp(-t*75))*np.exp(-t*3)
            s=env*(.32*np.sin(phase)+.18*np.sin(phase*1.51)+.1*high+.36*low)
        else:
            env=np.sin(np.pi*u)**2*np.exp(-u*2)
            phase=2*np.pi*(1200*t-900*t*t/(2*dur))
            s=env*(.18*np.sin(phase)+.65*high+.6*low)
        # A brief reflection, kept quieter than the dry sound for multiplayer.
        delay=int(rate*.071)
        dry=s.copy();s[delay:]+=.19*dry[:-delay]
        s[:200]*=np.linspace(0,1,200);s[-1400:]*=np.linspace(1,0,1400)
        s=.79*s/max(float(np.max(np.abs(s))),1e-6)
        wav=out/(name+'.wav')
        with wave.open(str(wav),'wb') as w:
            w.setparams((1,2,rate,0,'NONE','not compressed'));w.writeframes((s*32767).astype('<i2').tobytes())
        target=rp/f'assets/ichigo/sounds/{name}.ogg'
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(wav),'-c:a','libvorbis','-q:a','5',str(target)],check=True)
        wav.unlink()
        sounds[name]={'subtitle':f'ichigo.subtitle.{name}','sounds':[{'name':f'ichigo:{name}','volume':.8}]}
    (rp/'assets/ichigo/sounds.json').write_text(json.dumps(sounds,indent=2))
    lang=rp/'assets/ichigo/lang';lang.mkdir(exist_ok=True)
    (lang/'en_us.json').write_text(json.dumps({f'ichigo.subtitle.{k}':'Ichigo: '+k.capitalize() for k in durations}))
