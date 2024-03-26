---
theme: ./
layout: cover
class: text-left
transition: slide-left
mdc: true
backgroud: '/ATLAS/ATLAS-Logo.png'
authors:  # First author should be the presenter
  - Xuliang Zhu: ["TDLI"]
  - Tong Sun: ["TDLI"]
  - Rui Yuan: ["TDLI"] 

meeting: "Dark SHINE Simulation and Analysis Meeting"
preTitle: "DAna HCAL Smearing etc."
---

<br>

<img id="ATLAS" src="/DarkSHINE/DarkSHINE-Logo.png"> </img>

<style scoped>
#ATLAS {
  width: 160px;
  position: absolute;
  right: 3%;
  bottom: 4%;
  /* background-color: #2B90B6;
  background-image: linear-gradient(45deg, #4EC5D4 15%, #146b8c 50%); */
}
</style>

---
layout: pageBar
hideInToc: true
---

# Minutes

<br>

### 4GeV Sample

| Type | $m_{A'}$ (MeV) | Event Number | Directory |
| --- | --- | --- | --- |
| Inclusive | - |  $1\times 10^{7}$ | <small>`/lustre/collider/hepmc/DarkSHINE_Production/Baseline_1/4GeV/4GeV_noOptical_Oct18_ana_1.root`</small> |
| Signal | 1, 10, 100, 1000 | $1\times 10^{5}$ per $m_{A'}$ | <font color="orange">Running</font> |

Using environment and geometry setup from tag `baseline1`, with 1.5T uniform magnetic field.

Signal LUT: `/home/suntong/lustre/makeLUT/lhe_to_LUT/build/signal_4GeV_LUT.root`

---
layout: pageBar
hideInToc: true
---


# Outline

<br>

<div class="flex justify-center items-center" style="height: 50vh;">

### <Toc />

</div>

---
layout: pageBar
---

# HCAL Smearing Stratagy

<br>

The smearing of HCAL/SideHCAL is done in reconstruction level. For each HCAL/SideHCAL Cell, the energy of hits are summed, then Landau ditribution is used to do the smearing.

$$
\sigma = A\sqrt{E} + BE + C
$$

Currently, constant $\sigma$ is used.

| | $A (\sqrt{\text{MeV}})$ | $B$ | $C (\text{MeV})$ |
| --- | --- | --- | --- |
| HCAL 513 | 0 | 0 | 0.1953 |

---
layout: pageBar
---

# Validation: HCAL Cell Energy

<br>

Fig. 1: Distribution of Smeared HCAL E<sub>Cell</sub> vs Truth HCAL E<sub>Cell</sub>. ( Normalized for each bin of truth HCAL E<sub>Cell</sub>). Same $\sigma$ for all cell energy.

Fig. 2: Smeared HCAL $\Delta{E}$ vs Landau distribution. Match with each other.


<div grid="~ cols-[450px_1fr] gap-20">

<Transform :scale="0.6">
<PlotlyGraph filePath="plot/HCAL_E_Cell_truth_HCAL_E_Cell_smear.json" tickFontSize="18" graphWidth="800"/>
</Transform>

<Transform :scale="0.7">
<PlotlyGraph filePath="plot/delta_HCAL_E_Cell_gt1_gt1.json" tickFontSize="18" graphWidth="800"/>
</Transform>

</div>

---
layout: pageBar
---

# HCAL E Max Cell after smearing

<div grid="~ cols-[650px_1fr] gap-20">

<Transform :scale="0.85">
<PlotlyGraph filePath="plot/['HCAL_E_Max_Cell_truth', 'HCAL_E_Max_Cell_smear'].json" tickFontSize="18" graphWidth="800"/>
</Transform>

<div>

<br><br>

Peak is larger for <font color="red">smeared HCAL E<sub>Max Cell</sub> (0.6 MeV)</font>.

The background rejection is larger if use constant $\sigma$.

</div>

</div>

---
layout: pageBar
---

# TO-DO List

<br>

- ### DAna:
    - #### Acts performance, Uniform magnetic filed & Truth seeding (~ 2days)
    - #### Acts performance, Non-uniform magnetic filed & Truth seeding (~ +2days)
- ### Baseline 1.6: Filter efficiency

---
layout: center
class: "text-center"
hideInToc: true
---

# Thanks

---
layout: pageBar
---
