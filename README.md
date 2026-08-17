# Restaurant Order Fulfillment Process Mining with PM4Py

A process-mining portfolio project that reconstructs a restaurant order-fulfillment workflow from event-log data, discovers process models, quantifies timing variability, and identifies operational bottlenecks.

This repository is based on a **Business Analytics group project at the University of Bayreuth** by **Muhammad Jabran** and **Nusrat Jahan Iba**. The repository presentation and modular Python implementation were prepared for portfolio use while preserving the original analysis and results.

## Project overview

The original event log contains:

- **45,379 events**
- **7,549 orders (cases)**
- **8 activities**
- **8 staff resources**
- a date range from 2016 to 2120

Following the assignment rule, the analysis filters the log to the year **2030**. That produces **68 cases and 371 events**. To focus on normal successful fulfillment, cases that did not reach `Order_is_served` are removed, leaving:

- **44 completed orders**
- **299 events**

The workflow includes order arrival, ingredient checking, food preparation, oven preheating, cooking, spicing, and serving.

## Analytical workflow

1. Load an XES event log with PM4Py
2. Validate the required event-log fields
3. Convert timestamps to a consistent datetime representation
4. Filter the log to the selected year
5. Keep completed cases that reached `Order_is_served`
6. Convert the filtered DataFrame to a PM4Py event log
7. Discover a Petri net using the inductive miner
8. Discover a BPMN process model
9. Build frequency and performance directly-follows graphs
10. Build a temporal profile and quantify mean/standard-deviation timing
11. Export structured results and process visualizations

## Key findings

The analysis identifies **Food prepared → Food cooked** as the clearest direct bottleneck:

| Process step | Mean duration | Std. deviation |
|---|---:|---:|
| Food prepared → Food cooked | **143.4 h** | **69.4 h** |
| Food spiced → Order served | **112.3 h** | **67.8 h** |
| Order arrives → Ingredients checked | **42.3 h** | **23.6 h** |
| Oven preheated → Food cooked | **34.5 h** | **27.1 h** |

The mean end-to-end time from `Order_arrives` to `Order_is_served` is **296.8 hours** in the filtered simulated log.

The large variability around the preparation-to-cooking transition is important: the issue is not only speed but also **predictability**. In a real operational setting, that would motivate investigation of capacity, scheduling, equipment availability, or other causes.

> The dataset is simulated. Multi-day restaurant processing times are not realistic and should be interpreted as a demonstration of process-mining methodology rather than a literal operational finding.

## Process models

The analysis generates four process views when the script is run with the event log and Graphviz available:

- Petri net
- BPMN process model
- Frequency directly-follows graph
- Performance directly-follows graph

These models are also discussed in the original notebook and the portfolio-safe executive summary.

## Why this project is useful in a technical portfolio

Although this is a process-mining project rather than an LCA, it demonstrates skills that transfer directly to analytical engineering and sustainability-tool development:

- structuring and validating event-based data
- modular Python analysis
- traceable filtering and assumptions
- reproducible calculations
- process and bottleneck discovery
- handling incomplete or imperfect operational data
- separating evidence from interpretation
- translating quantitative results into actionable recommendations

The same analytical mindset is useful in sustainability and Ecodesign workflows where material, manufacturing, logistics, or lifecycle data must be structured, checked, traced, and interpreted consistently.

## Repository structure

```text
.
├── README.md
├── process_mining_analysis.py
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/
│   └── README.md
├── notebooks/
│   └── Process_Mining.ipynb
├── outputs/
│   └── README.md
├── report/
│   └── Executive_Summary.md
├── tests/
│   └── test_process_mining_analysis.py
└── .github/workflows/
    └── python-tests.yml
```

## Run the project

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Place the event log at:

```text
data/event_log.xes
```

Then run:

```bash
python process_mining_analysis.py --input data/event_log.xes --year 2030
```

The script saves process-model figures and structured outputs into `figures/` and `outputs/`.

PM4Py process visualizations also require a working **Graphviz** installation on the operating system.

## Reproducibility and design choices

The portfolio script separates loading, validation, filtering, discovery, temporal analysis, and export into functions rather than keeping the entire analysis in one notebook flow.

Important analytical choices are explicit parameters:

- analysis year
- completion activity
- input file
- output directory

The script also records a machine-readable summary so assumptions and major results can be checked later.

## Notebook and executive summary

- [`notebooks/Process_Mining.ipynb`](notebooks/Process_Mining.ipynb) — cleaned notebook containing the PM4Py analysis workflow.
- [`report/Executive_Summary.md`](report/Executive_Summary.md) — portfolio-safe executive summary based on the original group-project report.

## Tools

- Python
- pandas
- PM4Py
- Graphviz
- Jupyter / Google Colab
- pytest
- GitHub Actions

## Authors

**Muhammad Jabran**  
M.Sc. Food System Sciences, University of Bayreuth

**Nusrat Jahan Iba**  
Group-project co-author

## License

The portfolio code in this repository is released under the MIT License. The original event-log dataset is not included and remains subject to its original source/licensing conditions.
