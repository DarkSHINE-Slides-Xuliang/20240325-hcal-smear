import ROOT
import numpy as np
import plotly.graph_objs as go
from tools.plot import plot_style, add_histo1d


# Read Root File
rdf = ROOT.RDataFrame("dp","dp_ana_1e6.root")
rdf = (rdf
       .Define("HCAL_E_Max_Cell_truth", "HCAL_E_Max_Cell.at(0)")
       .Define("HCAL_E_Max_Cell_smear", "HCAL_E_Max_Cell.at(1)")
       .Define("HCAL_E_total_truth", "HCAL_E_total.at(0)")
       .Define("HCAL_E_total_smear", "HCAL_E_total.at(1)")
       )
varnames = ["HCAL_E_Max_Cell_truth", "HCAL_E_Max_Cell_smear"]
var_name_map = {
        "HCAL_E_Max_Cell_truth": "Truth",
        "HCAL_E_Max_Cell_smear": "Smeared",
         }

xmin=0
xmax=10
nbin=100
dx=(xmax-xmin)/nbin

fig = go.Figure()
for varname in varnames:
    histo = rdf.Filter("HCAL_E_Max_Cell_truth>0").Histo1D((varname, varname, nbin+2, xmin-1.5 * dx, xmax + 0.5*dx), varname)
    if histo.Integral("width") > 0:
           histo.Scale(1/histo.Integral("width"))
    # Plot Root
    add_histo1d(fig, histo, name=var_name_map[varname])

plot_style(fig,
           xaxes_title="HCAL E<sub>Max Cell</sub> [MeV]",
           yaxes_title="Events Normalized",
           xaxes_range=[xmin-0.5*dx, xmax+0.5*dx],
           yaxes_range=[-0.1, 2],
           #yaxes_range=[-0.1, 2.5],
           #yaxes_type='log',
           darkshine_label3="HCAL E<sub>Max Cell</sub> > 0 MeV",
           #darkshine_label3="Truth E<sub>Cell</sub> < 10  MeV",
           )


# Show the plot
fig.show()
fig.write_json(f"../public/plot/{varnames}.json")
fig.write_image(f"../public/plot/{varnames}.pdf")

