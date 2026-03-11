"""
docs.py — Documentation render functions for the JUNC Info expander.
"""
import streamlit as st


def render_junc_guide():
    st.markdown("""
### What JUNC Does
JUNC optimises the signal phasing at a signalised intersection. It uses
Integer Linear Programming (Wardrop equilibrium via PuLP/CBC) to minimise
delay across all movements, then generates three output reports:

| Output file | Contents |
|---|---|
| `diagram.pptx / .png` | Turn-movement flow diagram |
| `table.pptx / .png` | Phase table with green times and LOS |
| `id.pptx / .png` | Junction ID sheet |
| `OUTPUT.xlsx` | Raw optimisation results |

---
### Input Data
Fill the form on the right-hand side of the screen:

**Volumes tab** — hourly vehicle counts (veh/h) for each combination of:
- Direction: North / South / East / West
- Movement: R (right turn) · T (through) · L (left turn)
- Period: AM peak · PM peak

**Lanes tab** — number of lanes and lane type (R / RT / T / TL / L / RTL / RL)
per direction.

**Restrictions tab** — opposing-movement conflicts that must be phased
separately.

**Settings tab** — junction name, cycle time, PHF, saturation flow, etc.

---
### Running the Optimisation
1. Fill in (or import) the form.
2. Click **▶ Run Analysis** in the sidebar.
3. When the spinner disappears, download the four output files from the
   sidebar download buttons.

To re-use data from a previous session, upload a filled `volume_calculator.xlsx`
via **📥 Import Excel** in the sidebar.

---
### Additional Analysis
Below the main layout you will find three independent analysis expanders.

| Expander | Requires pipeline run? |
|---|---|
| Queue Length (Poisson) | Yes — uses optimised green times |
| HCM Delay & LOS | No — enter green times manually |
| HCM 95th Percentile Queue | No — enter green times manually |

Each expander shows results inline and offers a download button for an Excel
report.
""")


def render_queue_poisson_docs():
    st.markdown("""
### Queue Length — Poisson Method

**Intuition**
Traffic arrives at a stop line randomly. Over many cycles the average number
of vehicles arriving per cycle is `m`. We model the arrival count as a Poisson
random variable with mean `m` and find the 95th-percentile count `n`. Multiply
by average vehicle length to get the 95th-percentile queue in metres.

---
### Parameters
| Symbol | Meaning |
|---|---|
| `v` | Hourly flow (veh/h) |
| `C` | Cycle time (s) |
| `PHF` | Peak-hour factor |
| `p` | Percentile (default 0.95) |
| `l` | Average vehicle length + gap (m) |
| `green` | Effective green time for the movement (s) |

---
### Formulas
""")
    st.markdown("**Average vehicles per cycle**")
    st.latex(r"m = \left\lceil \frac{v}{3600/C \cdot \mathrm{PHF}} \right\rceil")

    st.markdown("**95th-percentile vehicle count**  \n"
                "Find the smallest integer `n` such that the Poisson CDF reaches `p`:")
    st.latex(r"n = \min\!\left\{n \in \mathbb{N}_0 : "
             r"\sum_{k=0}^{n} \frac{e^{-m}\,m^k}{k!} \geq p\right\}")

    st.markdown("**Queue length in metres**")
    st.latex(r"L = n \times l")

    st.markdown("**Adjusted queue length** (when *Discard green time* is enabled)  \n"
                "Only the red portion of the cycle contributes to queue build-up:")
    st.latex(
        r"L_{\mathrm{adj}} = L \times "
        r"\frac{C_{\mathrm{red}} - g_{\mathrm{movement}}}{C_{\mathrm{red}}}"
    )
    st.markdown(
        "where `C_red` is the total red capacity "
        "(`Σ phase_times + basic_lost_capacity`)."
    )


def render_hcm_delay_docs():
    st.markdown("""
### HCM Signal Delay & LOS

**Intuition**
Every vehicle at a signalised intersection experiences two types of delay:

1. **Uniform delay** — the predictable wait caused by red phases, assuming
   demand never exceeds capacity.
2. **Overflow delay** — the extra wait that builds up when demand is close to
   or exceeds capacity (degree of saturation `X ≥ 1`).

The sum (adjusted by a progression factor) is the average control delay per
vehicle. HCM 6th edition maps this to Level of Service grades A–F.

---
### Parameters
| Symbol | Meaning |
|---|---|
| `v` | Hourly flow (veh/h) |
| `s` | Saturation flow rate (veh/h per lane) |
| `lanes` | Number of lanes |
| `g` | Effective green time (s) |
| `C` | Cycle time (s) |
| `T` | Analysis period (h), typically 0.25 |
| `k` | Overflow delay calibration factor (0.5 for pre-timed) |
| `I` | Upstream filtering factor (1.0 isolated) |
| `PF` | Progression factor (1.0 random arrivals) |

---
### Formulas (HCM 6th ed., Chapter 19)
""")
    st.markdown("**Capacity**")
    st.latex(r"c = s \cdot \mathrm{lanes} \cdot \frac{g}{C}")

    st.markdown("**Degree of saturation**")
    st.latex(r"X = \frac{v}{c}")

    st.markdown("**Uniform delay**")
    st.latex(
        r"d_1 = \frac{0.5\,C\!\left(1 - g/C\right)^2}"
        r"{1 - \min(1,X)\cdot g/C}"
    )

    st.markdown("**Overflow delay**")
    st.latex(
        r"d_2 = 900T\!\left[(X-1) + \sqrt{(X-1)^2 + \frac{8kIX}{cT}}\,\right]"
    )

    st.markdown("**Total control delay** (s/veh)")
    st.latex(r"d = d_1 \cdot PF + d_2")

    st.markdown("""
---
### Level of Service Thresholds

| LOS | Delay (s/veh) |
|:---:|---|
| A | ≤ 10 |
| B | ≤ 20 |
| C | ≤ 35 |
| D | ≤ 55 |
| E | ≤ 80 |
| F | > 80 |
""")


def render_hcm_queue95_docs():
    st.markdown("""
### HCM 95th Percentile Queue

**Intuition**
Using the same capacity model as the HCM delay calculation, we estimate the
average number of vehicles queued at the start of green (uniform component)
and the additional vehicles that overflow from one cycle to the next (overflow
component). Treating the queue as Poisson-distributed, we inflate the average
to the 95th percentile.

---
### Parameters
Same as the HCM Delay section (`v`, `s`, `lanes`, `g`, `C`, `T`, `k`, `I`)
plus:

| Symbol | Meaning |
|---|---|
| `l` | Average vehicle length + gap (m) |

---
### Formulas
""")
    st.markdown("**Capacity and degree of saturation** — same as HCM Delay:**")
    st.latex(r"c = s \cdot \mathrm{lanes} \cdot \frac{g}{C}, \qquad X = \frac{v}{c}")

    st.markdown("**Uniform queue component** (vehicles)")
    st.latex(
        r"N_{q1} = \frac{c \cdot (C/3600) \cdot (1 - g/C)^2}"
        r"{1 - \min(1,X)\cdot g/C}"
    )

    st.markdown("**Overflow queue component** (vehicles)")
    st.latex(
        r"N_{q2} = \frac{900T\!\left[(X-1)+\sqrt{(X-1)^2+\dfrac{8kIX}{cT}}\,\right]\cdot c}{3600}"
    )

    st.markdown("**Average queue**")
    st.latex(r"N_q = \max\!\left(0,\; N_{q1} + N_{q2}\right)")

    st.markdown("**95th-percentile queue** (vehicles, Poisson approximation)")
    st.latex(r"Q_{95} = N_q + 1.65\,\sqrt{N_q}")

    st.markdown("**95th-percentile queue** (metres)")
    st.latex(r"Q_{95,m} = Q_{95} \times l")
