import ROOT
import pydrcTB
import matplotlib.pyplot as plt
from tqdm import tqdm

# open root file and get Tree
in_file="test_Fast.root"
file = ROOT.TFile(in_file)
atree = file.Get("events")

# load mapping and pedestal
utility = pydrcTB.TButility()
utility.loading("mapping_data_MCPPMT_positiveSignal.csv")
utility.loadped("ped_236.csv")
channelsize = 32

# initialize empty list
list_adc=[]
list_sipm_scint_adc=[]
list_sipm_ceren_adc=[]
list_pmt_scint_adc=[]
list_pmt_ceren_adc=[]
#draw_root=False
draw_root=True

print("Read entry")
for ievt in range(atree.GetEntries()):
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

if(draw_root):
  range_min=min(list_adc)
  range_max=max(list_adc)
  # histogram
  hist1=ROOT.TH1F("hist1","SiPM Scintilation channel",num_bin,range_min,range_max)
  hist2=ROOT.TH1F("hist2","SiPM Cerenkov channel",num_bin,range_min,range_max)
  hist3=ROOT.TH1F("hist3","PMT Scintilation channel",num_bin,range_min,range_max)
  hist4=ROOT.TH1F("hist4","PMT Cerenkov channel",num_bin,range_min,range_max)
  hist1.GetXaxis().SetTitle("ADC sum") 
  hist2.GetXaxis().SetTitle("ADC sum") 
  hist3.GetXaxis().SetTitle("ADC sum") 
  hist4.GetXaxis().SetTitle("ADC sum") 
  hist1.GetYaxis().SetTitle("number of entries") 
  hist2.GetYaxis().SetTitle("number of entries") 
  hist3.GetYaxis().SetTitle("number of entries") 
  hist4.GetYaxis().SetTitle("number of entries") 
  # fill data to histogram
  for sipm_scint_adc in list_sipm_scint_adc:
      hist1.Fill(sipm_scint_adc)
  for sipm_ceren_adc in list_sipm_ceren_adc:
      hist2.Fill(sipm_ceren_adc)
  for pmt_scint_adc in list_pmt_scint_adc:
      hist3.Fill(pmt_scint_adc)
  for pmt_ceren_adc in list_pmt_ceren_adc:
      hist4.Fill(pmt_ceren_adc)
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
  c1.SaveAs("../Pictures/adc_root.png")
else:
  px = 1/plt.rcParams['figure.dpi']
  fig,ax=plt.subplots(nrows,ncols,figsize=(canvas_width*px,canvas_height*px))
  ax[0].hist(list_adc,bins=num_bin,histtype="step")
  ax[0].set_title("ADC sum")
  ax[0].set_xlabel("ADC value")
  ax[0].set_ylabel("number of entries")
  fig.savefig("../Pictures/adc_py.png")
print(list_sipm_scint_adc[:5])
print(list_sipm_ceren_adc[:5])
print(list_pmt_scint_adc[:5])
print(list_pmt_ceren_adc[:5])
