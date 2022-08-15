import ROOT
import pydrcTB
import matplotlib.pyplot as plt
import argparse
from tqdm import tqdm
from array import array

parser=argparse.ArgumentParser()
parser.add_argument("--in_root",type=str,default="test_Wave.root",help="input root file name")
parser.add_argument("--wave_case",type=str,default="1_2_3,3_2_1,5_6_7",help="pedestal file")
parser.add_argument("--save_name",type=str,default="../Pictures/wave",help="plot will be saved as save_name")

parser.add_argument("--draw_root",type=bool,default=True,help="Draw with ROOT else pyplot")
parser.add_argument("--mod",type=str,default="wave",help="fast or wave")
parser.add_argument("--mapping",type=str,default="mapping_data_MCPPMT_positiveSignal.csv",help="mapping file")
parser.add_argument("--pedestal",type=str,default="ped_236.csv",help="pedestal file")
#parser.add_argument("--wave_case",type=str,default="",help="pedestal file")

args=parser.parse_args()
draw_root=args.draw_root
mod=args.mod
wave_case=[]
for label in args.wave_case.replace(" ","").split(","):
  case=[int(i) for i in label.split("_")]
  wave_case.append(case)

# open root file and get Tree
file = ROOT.TFile(args.in_root)
atree = file.Get("events")

# load mapping and pedestal
utility = pydrcTB.TButility()
utility.loading(args.mapping)
utility.loadped(args.pedestal)
channelsize = 32

# initialize empty list
list_wave=[]
list_label=[]
list_title=[]
log=""
#for ievt in tqdm(range(atree.GetEntries())):
for case in wave_case:
    ievt,imid,ich=case
    atree.GetEntry(ievt)
    anevt = getattr(atree,"TBevt")

    # initilize value - important
    adc = 0.

    # check data of each entry
    cidboost = pydrcTB.TBcid( imid+1, ich+1 ) # mid 1 - 15, ch 1 - 32
    cidroot  = ROOT.TBcid( imid+1, ich+1 )
    adet = utility.find(cidboost)# mapping information

    if (not adet.isNull() and adet.isModule()):
        adata = anevt.data( cidroot )
        list_wave.append(list(adata.waveform()))
        list_label.append(f"{ievt}_{imid}_{ich}")

        title=f"Module {imid} Ch. {ich}"
        if(adet.isSiPM()):
            title+=" SiPM"
        else:
            title+=" PMT"
        if(adet.isCeren()):
            title+=" Cerenkov"
        else:
            title+=" Schintilation"
        list_title.append(title)

# divide canvas 2*2
ncols=1
nrows=1
# canvas pixel width height
canvas_width=1600
canvas_height=1600
# number of historgram bins
num_bin=100

if(draw_root):
    # histogram
    c1=ROOT.TCanvas("c1","plots",canvas_width,canvas_height)
    c1.SetLeftMargin(0.15)
    x=array('i')
    y=array('i')
    for i in range(len(list_wave)):
      c1.Clear()
      wave=list_wave[i]
      for j in range(1024):
        x.append(j)
        y.append(wave[j])
      graph1=ROOT.TGraph(1024,x,y)
      #graph1=ROOT.TGraph("graph1","Waveform",1024,x,y)
      graph1.SetTitle(list_title[i]) 
      graph1.GetXaxis().SetTitle("wave x") 
      graph1.GetYaxis().SetTitle("wave y") 
      #graph1.GetXaxis().SetRangeUser(0,1024)
      graph1.GetXaxis().SetLimits(0,1024)
      c1.cd()
      graph1.Draw()
      # save canvas as image file
      c1.SaveAs("{}_{}.png".format(args.save_name,list_label[i]))
      del graph1
else:
  px = 1/plt.rcParams['figure.dpi']
  fig=plt.figure(figsize=(canvas_width*px,canvas_height*px))
  x=[]
  y=[]
  for i in range(len(wave_case)):
    plt.clf()
    wave=list_wave[i]
    for j in range(1024):
      x.append(j)
      y.append(wave[j])
    plt.hist(wave)
    plt.title(list_title[i])
    plt.xlabel("wave x")
    plt.set_ylabel("wave y")
    plt.set_xlim([0,1024])
    plt.text(0,0,"text")
    fig.savefig("{}_{}.png".format(args.save_name,list_label[i]))
