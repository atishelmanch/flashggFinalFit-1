import ROOT
from ROOT import *

import sys
import os

from optparse import OptionParser
def get_options():
  parser = OptionParser()
  # Take inputs from config file
  parser.add_option('--HHWWggLabel', dest='HHWWggLabel', default='', help="Name of HHWWggLabel ")
  parser.add_option('--procs', dest='procs', default='', help="process")
  parser.add_option('--cats', dest='cats', default='', help="cats")
  parser.add_option('--inputDir', dest='inputDir', default='./', help="Input Dir")
  return parser.parse_args()
(opt,args) = get_options()

inDir = opt.inputDir
outDir = inDir 

cats = opt.cats.split(',')

values = [-5,0,5]
higgs_mass = 125
ws_name = 'tagsDumper/cms_hgg_13TeV'
# dataset_name = '%s_%s_13TeV_%s'%(opt.procs,opt.HHWWggLabel,opt.cats)
# dataset_name = '%s_%s_13TeV_%s'%(opt.procs,opt.HHWWggLabel,"SL")
# temp_ws = TFile(inDir+'output_M125_%s_%s_%s.root'%(opt.procs,opt.HHWWggLabel,opt.cats)).Get(ws_name)
# temp_ws = TFile(inDir+'output_M125_%s_%s.root'%(opt.procs,opt.HHWWggLabel)).Get(ws_name)

for value in values:
  shift = value + higgs_mass
  for cat in cats:
    temp_ws = TFile(inDir+'output_M125_%s_%s_%s.root'%(opt.procs,opt.HHWWggLabel,cat)).Get(ws_name)
    output = TFile(outDir + 'Shifted_M'+str(shift)+'_%s_%s_%s.root'%(opt.procs,opt.HHWWggLabel,cat),'RECREATE')
    output.mkdir("tagsDumper")  
    ws_new = ROOT.RooWorkspace("cms_hgg_13TeV")    
    dataset_name = '%s_%s_13TeV_%s'%(opt.procs,opt.HHWWggLabel,cat)
    # dataset1 = (temp_ws.data(dataset_name)).Clone('%s_'%opt.procs + str(shift)+'_%s_13TeV_%s'%(opt.HHWWggLabel,opt.cats)) # includes process and category
    dataset1 = (temp_ws.data(dataset_name)).Clone('%s_'%opt.procs + str(shift)+'_%s_13TeV_%s'%(opt.HHWWggLabel,cat)) # includes process and category
    dataset1.Print()
    dataset1.changeObservableName('CMS_hgg_mass','CMS_hgg_mass_old')
    higgs_old = dataset1.get()['CMS_hgg_mass_old']
    higgs_new = RooFormulaVar( 'CMS_hgg_mass', 'CMS_hgg_mass', "(@0+%.1f)"%value,RooArgList(higgs_old) );
    dataset1.addColumn(higgs_new).setRange(105,145)
    dataset1.Print()
    # output = TFile(outDir + 'Shifted_M'+str(shift)+'_%s_%s_%s.root'%(opt.procs,opt.HHWWggLabel,opt.cats),'RECREATE')
    # output = TFile(outDir + 'Shifted_M'+str(shift)+'_%s_%s_%s.root'%(opt.procs,opt.HHWWggLabel,"SL"),'RECREATE')
    output.cd("tagsDumper")
    getattr(ws_new,'import')(dataset1,RooCmdArg())
    ws_new.Write()
    output.Close()


# values = [-5,0,5]
# higgs_mass = 125
# ws_name = 'tagsDumper/cms_hgg_13TeV'
# dataset_name = '%s_%s_13TeV_%s'%(opt.procs,opt.HHWWggLabel,opt.cats)
# temp_ws = TFile(inDir+'output_M125_%s_%s_%s.root'%(opt.procs,opt.HHWWggLabel,opt.cats)).Get(ws_name)
# for value in values:
#     shift = value + higgs_mass
#     dataset1 = (temp_ws.data(dataset_name)).Clone('%s_'%opt.procs + str(shift)+'_%s_13TeV_%s'%(opt.HHWWggLabel,opt.cats)) # includes process and category
#     dataset1.Print()
#     dataset1.changeObservableName('CMS_hgg_mass','CMS_hgg_mass_old')
#     higgs_old = dataset1.get()['CMS_hgg_mass_old']
#     higgs_new = RooFormulaVar( 'CMS_hgg_mass', 'CMS_hgg_mass', "(@0+%.1f)"%value,RooArgList(higgs_old) );
#     dataset1.addColumn(higgs_new).setRange(105,145)
#     dataset1.Print()
#     output = TFile(outDir + 'Shifted_M'+str(shift)+'_%s_%s_%s.root'%(opt.procs,opt.HHWWggLabel,opt.cats),'RECREATE')
#     output.mkdir("tagsDumper")
#     output.cd("tagsDumper")
#     ws_new = ROOT.RooWorkspace("cms_hgg_13TeV")
#     getattr(ws_new,'import')(dataset1,RooCmdArg())
#     ws_new.Write()
#     output.Close()