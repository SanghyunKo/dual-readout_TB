import ROOT
import pydrcTB
import matplotlib.pyplot as plt
import argparse
from tqdm import tqdm

parser=argparse.ArgumentParser()
parser.add_argument("--in_root",type=str,default="test_Fast.root",help="input root file name")
parser.add_argument("--save_name",type=str,default="../Pictures/fast",help="plot will be saved as save_name")

parser.add_argument("--draw_root",type=bool,default=True,help="Draw with ROOT else pyplot")
parser.add_argument("--mod",type=str,default="fast",help="fast or wave")
parser.add_argument("--mapping",type=str,default="mapping_data_MCPPMT_positiveSignal.csv",help="mapping file")
parser.add_argument("--pedestal",type=str,default="ped_236.csv",help="pedestal file")

args=parser.parse_args()
draw_root=args.draw_root
mod=args.mod


# open root file and get Tree
file = ROOT.TFile(args.in_root)
atree = file.Get("events")

# load mapping and pedestal
utility = pydrcTB.TButility()
utility.loading(args.mapping)
utility.loadped(args.pedestal)
channelsize = 32

# initialize empty list
list_adc=[]
list_sipm_scint_adc=[]
list_sipm_ceren_adc=[]
list_pmt_scint_adc=[]
list_pmt_ceren_adc=[]
info=[]
print("Read entry")
for ievt in tqdm(range(atree.GetEntries())):
    # load each entry
    atree.GetEntry(ievt)
    anevt = getattr(atree,"TBevt")

    # initilize value - important
    adc = 0.
    sipm_scint_adc = 0.
    sipm_ceren_adc = 0.
    pmt_scint_adc = 0.
    pmt_ceren_adc = 0.

    # check data of each entry
    for imid in range(anevt.size()):
        for ich in range(channelsize):
            # TODO cannot convert ROOT TBcid & boost::python TBcid automatically
            cidboost = pydrcTB.TBcid( imid+1, ich+1 ) # mid 1 - 15, ch 1 - 32
            cidroot  = ROOT.TBcid( imid+1, ich+1 )

            adet = utility.find(cidboost)# mapping information

            if (not adet.isNull() and adet.isModule()):
                adata = anevt.data( cidroot )
                adc += adata.adc()
                if(adet.isSiPM()):
                    if(not adet.isCeren()):# Scintilation channel
                        sipm_scint_adc += adata.adc()
                    else:# Cerenkov channel
                        sipm_ceren_adc += adata.adc()
                else:# PMT,MCP-PMT
                    if(not adet.isCeren()):# Scintilation channel
                        pmt_scint_adc += adata.adc()
                    else:# Cerenkov channel
                        pmt_ceren_adc += adata.adc()
                info.append([adet.column(),adet.isSiPM(),adet.plate(),adet.isCeren(),adet.module(),adet.tower()])
    #if(adc!=0):print(adc)
    # store value to list
    list_adc.append(adc)
    list_sipm_scint_adc.append(sipm_scint_adc)
    list_sipm_ceren_adc.append(sipm_ceren_adc)
    list_pmt_scint_adc.append(pmt_scint_adc)
    list_pmt_ceren_adc.append(pmt_ceren_adc)

print("Entry ended")

# divide canvas 2*2
ncols=2
nrows=2
# canvas pixel width height
canvas_width=1600
canvas_height=1600
# number of historgram bins
num_bin=100
xlabel="ADC sum"
ylabel="Number of entries"
count=[0,0,0,0]
range_min=min(list_adc)
range_max=max(list_adc)
if(draw_root):
  # histogram
  hist1=ROOT.TH1F("hist1","SiPM Scintilation channel",num_bin,range_min,range_max)
  hist2=ROOT.TH1F("hist2","SiPM Cerenkov channel",num_bin,range_min,range_max)
  hist3=ROOT.TH1F("hist3","PMT Scintilation channel",num_bin,range_min,range_max)
  hist4=ROOT.TH1F("hist4","PMT Cerenkov channel",num_bin,range_min,range_max)
  hist1.GetXaxis().SetTitle(xlabel) 
  hist2.GetXaxis().SetTitle(xlabel) 
  hist3.GetXaxis().SetTitle(xlabel) 
  hist4.GetXaxis().SetTitle(xlabel) 
  hist1.GetYaxis().SetTitle(ylabel) 
  hist2.GetYaxis().SetTitle(ylabel) 
  hist3.GetYaxis().SetTitle(ylabel) 
  hist4.GetYaxis().SetTitle(ylabel) 
  # fill data to histogram
  for sipm_scint_adc in list_sipm_scint_adc:
      hist1.Fill(sipm_scint_adc)
      count[0]+=1
  for sipm_ceren_adc in list_sipm_ceren_adc:
      hist2.Fill(sipm_ceren_adc)
      count[1]+=1
  for pmt_scint_adc in list_pmt_scint_adc:
      hist3.Fill(pmt_scint_adc)
      count[2]+=1
  for pmt_ceren_adc in list_pmt_ceren_adc:
      hist4.Fill(pmt_ceren_adc)
      count[3]+=1
  # draw histogram on canvas
  c1=ROOT.TCanvas("c1","plots",canvas_width,canvas_height)
  c1.Divide(ncols,nrows)
  c1.cd(1)# left top
  hist1.Draw()
  c1.cd(2)# right top
  hist2.Draw()
  c1.cd(3)# left bottom
  hist3.Draw()
  c1.cd(4)# right bottom
  hist4.Draw()
  # save canvas as image file
  c1.SaveAs("{}.png".format(args.save_name))
else:
  px = 1/plt.rcParams['figure.dpi']
  fig,ax=plt.subplots(2,2,figsize=(10,10))
  fig,ax=plt.subplots(nrows,ncols,figsize=(canvas_width*px,canvas_height*px))
  ax[0][0].hist(list_sipm_scint_adc,bins=num_bin,histtype="step",range=(range_min,range_max))
  ax[0][0].set_title("SiPM Scintilation channel")
  ax[0][1].hist(list_sipm_ceren_adc,bins=num_bin,histtype="step",range=(range_min,range_max))
  ax[0][1].set_title("SiPM Cerenkov channel")
  ax[1][0].hist(list_pmt_scint_adc,bins=num_bin,histtype="step",range=(range_min,range_max))
  ax[1][0].set_title("PMT Scintilation channel")
  ax[1][1].hist(list_pmt_ceren_adc,bins=num_bin,histtype="step",range=(range_min,range_max))
  ax[1][1].set_title("PMT Cerenkov channel")
  for i in range(nrows):
    for j in range(ncols):
      ax[i][j].set_xlabel(xlabel)
      ax[i][j].set_ylabel(ylabel)
  #print(ax.shape)
  fig.savefig("{}.png".format(args.save_name))
  pass
print(count)
