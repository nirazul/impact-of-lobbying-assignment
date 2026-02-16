# Readme

## Installation

1. Install conda if necessary:
   <br>
   `brew install miniconda`

2. Create conda environment:
   <br>
   `conda env create --file environment.yaml`

## Data Collection

Retrieving data is optional. It is included in the repository for convenience in the folder `notebooks/scraped`.

Data can be collected via the following notebooks:

- `notebooks/load_bodies_data.ipynb`
- `notebooks/load_interests_data.ipynb`

## Analysis

The analysis is run via the notebook `notebooks/prepare_analysis.ipynb`.
The results are saved in the folder `notebooks/results`.
The figures are saved in the folder `notebooks/figures`.