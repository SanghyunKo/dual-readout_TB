import pydrcTB
import os

#mod="Wave"
mod="Fast"
run_num=1
dat_num=117

if(mod=="Fast"):
    dat_label="cal_fast"
if(mod=="Wave"):
    dat_label="cal_wave"

base_dir=f"../public/Run_{run_num}_{mod}/"
mid_dirs=os.listdir(base_dir)
filenames=[]

for mid_d in mid_dirs:
    mid=mid_d.split("_")[-1]
    dat_name=f"{dat_label}_{mid}_{dat_num}.dat"
    dat_path=base_dir+mid_d+"/"+dat_name
    if(os.path.isfile(dat_path)):
      filenames.append(dat_path)
    else:
      print(dat_path,"not found")

if(filenames!=[]):
    reader = pydrcTB.TBread()
    print("ntuplizing..")
    if(mod=="Fast"):
        reader.ntuplizeFastmode(filenames,f"test_{mod}.root")
    if(mod=="Wave"):
        reader.ntuplizeWaveform(filenames,f"test_{mod}.root")
    #filenames size
else:
    print("no .dat file found")

