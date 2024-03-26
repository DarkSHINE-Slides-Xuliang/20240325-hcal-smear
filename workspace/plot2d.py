import ROOT
import numpy as np
import plotly.graph_objs as go
from tools.plot import plot_style, add_histo1d
from weasyprint import HTML


var_label = {
        'HCAL_E_Cell_truth': 'Truth HCAL E<sub>Cell</sub> [MeV]',
        'HCAL_E_Cell_smear': 'Smeared HCAL E<sub>Cell</sub> [MeV]',
        'HCAL_E_Cell_truth_': 'Truth HCAL E<sub>Cell</sub> [MeV]',
        'HCAL_E_Cell_smear_': 'Smeared HCAL E<sub>Cell</sub> [MeV]',
        }

#ROOT.gInterpreter.Declare(r"""
#std::pair<ROOT::VecOps::RVec<Double_t>,ROOT::VecOps::RVec<Double_t>> get_HCAL_E_Cell_truth_gep(const ROOT::VecOps::RVec<Double_t>& vtruth, const ROOT::VecOps::RVec<Double_t>& vsmear, Double_t cutE = 0) {
#       std::pair<ROOT::VecOps::RVec<Double_t>,ROOT::VecOps::RVec<Double_t>> truth_smear = {};
#       for (int i = 0; i < vtruth.size(); i++) {
#              if (vtruth.at(i) <= cutE)
#                     continue;
#              truth_smear.first.emplace_back(vtruth.at(i));
#              truth_smear.second.emplace_back(vsmear.at(i));
#       }
#       return truth_smear;
#}
#""")


# Read Root File
rdf = ROOT.RDataFrame("dp","dp_ana_1e6.root")
rdf = (rdf
#       .Define("HCAL_E_Cell_truth_", "get_HCAL_E_Cell_truth_gep(HCAL_E_Cell_truth, HCAL_E_Cell_smear, 1).first")
#       .Define("HCAL_E_Cell_smear_", "get_HCAL_E_Cell_truth_gep(HCAL_E_Cell_truth, HCAL_E_Cell_smear, 1).second")
       )
variable_x = "HCAL_E_Cell_truth"
variable_y = "HCAL_E_Cell_smear"

histo = rdf.Histo2D((f"{variable_x}_vs_{variable_y}", "2D Histogram", 21, -0.5, 20.5, 200, 0, 20), variable_x, variable_y)

# Convert ROOT histogram to numpy
n_bins_x, n_bins_y = histo.GetNbinsX(), histo.GetNbinsY()
x_edges = np.array([histo.GetXaxis().GetBinLowEdge(i) for i in range(1, n_bins_x + 1)])
y_edges = np.array([histo.GetYaxis().GetBinLowEdge(i) for i in range(1, n_bins_y + 1)])
hist_values = np.array([[histo.GetBinContent(i, j) for i in range(1, n_bins_x + 1)] for j in range(1, n_bins_y + 1)])

# Normalize the histogram by each x-bin
column_sums = hist_values.sum(axis=0)
hist_values = 10* hist_values / column_sums

# Create plotly figure
x_centers = (x_edges[1:] + x_edges[:-1]) / 2
y_centers = (y_edges[1:] + y_edges[:-1]) / 2

# Plot Root
fig = go.Figure()
fig.add_trace(
    go.Heatmap(
        x=x_centers,
        y=y_centers,
        z=hist_values,
        colorscale='Blues',
        zmin=0,
        zmax=1,
        )
)

# Reference lines
fig.add_trace(
        go.Scatter(
            x=[0] + [i-0.5 for i in range(22) for _ in range(3) if i != 0 and i != 21] + [21],
            y=[item for i in range(22) for item in (i, i, None)],
            mode='lines',
            )
        )

plot_style(fig,
           fig_height=700,
           xaxes_title=var_label[variable_x],
           yaxes_title=var_label[variable_y],
           darkshine_label3='Normalized by column',
           # xaxes_range=[-1, 3],
           # yaxes_range=[-0.1, 1.3],
           # yaxes_range=[-0.1, 2.5],
           )

fig.update_layout(
        showlegend=False
        )
fig.update_yaxes(
        range=[0,20]
        )
# Show the plot
fig.show()
fig.write_json(f"../public/plot/{variable_x}_{variable_y}.json")
#fig.write_image(f"../public/plot/{variable_x}_{variable_y}.pdf")
# Convert the figure to HTML
fig_html = fig.to_html()

# Use WeasyPrint to convert HTML to PDF
HTML(string=fig_html).write_pdf("{variable_x}_{variable_y}.pdf")
