import ROOT
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from tools.plot import plot_style, add_histo1d


ROOT.gInterpreter.Declare(r"""
ROOT::VecOps::RVec<Double_t> get_delta_HCAL_E_Cell_leq(const ROOT::VecOps::RVec<Double_t>& vsmear, const ROOT::VecOps::RVec<Double_t>& vtruth, Double_t cutE) {
       ROOT::VecOps::RVec<Double_t> vdelta = {};
       for (int i = 0; i < vsmear.size(); i++) {
              if (vtruth.at(i) > cutE)
                     continue;
              vdelta.emplace_back(vsmear.at(i) - vtruth.at(i));
       }
       return vdelta;
}

ROOT::VecOps::RVec<Double_t> get_delta_HCAL_E_Cell_gt(const ROOT::VecOps::RVec<Double_t>& vsmear, const ROOT::VecOps::RVec<Double_t>& vtruth, Double_t cutE) {
       ROOT::VecOps::RVec<Double_t> vdelta = {};
       for (int i = 0; i < vsmear.size(); i++) {
              if (vtruth.at(i) <= cutE) // min E
                     continue;
              vdelta.emplace_back(vsmear.at(i) - vtruth.at(i));
       }
       return vdelta;
}
""")


# Read Root File
rdf = ROOT.RDataFrame("dp","dp_ana_1e6.root")
rdf = (rdf
       .Define("delta_HCAL_E_Cell_gt1", "get_delta_HCAL_E_Cell_gt(HCAL_E_Cell_smear,HCAL_E_Cell_truth, 1)")
       .Define("delta_HCAL_E_Cell_leq1", "get_delta_HCAL_E_Cell_leq(HCAL_E_Cell_smear,HCAL_E_Cell_truth, 1)")
       .Define("HCAL_E_total_truth", "HCAL_E_total.at(0)")
       .Define("HCAL_E_total_smear", "HCAL_E_total.at(0)")
       )
varname = "delta_HCAL_E_Cell_gt1"
histo = rdf.Histo1D((varname, varname, 100, -2 - 0.05, 8 - 0.05), varname)
if histo.Integral("width") > 0:
       histo.Scale(1/histo.Integral("width"))
# Plot Root
fig = go.Figure()
add_histo1d(fig,
            histo,
            name="DAna"
            )
plot_style(fig,
           xaxes_title="HCAL Cell ΔE<sub>smear-truth</sub> [MeV]",
           yaxes_title="Events Normalized",
           xaxes_range=[-1, 3],
           yaxes_range=[-0.1, 1.3],
           #yaxes_range=[-0.1, 2.5],
           darkshine_label3="Truth E<sub>Cell</sub> > 1  MeV",
           #darkshine_label3="Truth E<sub>Cell</sub> < 10  MeV",
           )

# Plot Function
mpv = 0  # Replace with your MPV value
sigma = 13.11*1.95/130.9  # Replace with your sigma value

x_values = np.linspace(-2, 8, 501)
y_values = [ROOT.Math.landau_pdf((x-mpv)/sigma)/sigma for x in x_values]

# Create the plot
fig.add_trace(
       go.Scatter(
           x=x_values,
           y=y_values,
           mode='lines',
           name='Landau Distribution',
           line_color=px.colors.qualitative.Plotly[1],
           )
)

# Show the plot
fig.show()
# fig.write_json(f"plot/{varname}_minE10.json")
# fig.write_image(f"plot/{varname}_minE10.pdf")
fig.write_json(f"../public/plot/{varname}_gt1.json")
fig.write_image(f"../public/plot/{varname}_gt1.pdf")

