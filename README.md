# PFAS trace

PFAS are released into the environment through a few key industrial processes and pose a serious health risk to the 
public.

It is difficult to convey the extent of the problem on an individual level. Therefore this project aims to find an 
abstract correlation between the PFAS measurements and the surrounding industries.

## Research Question

Can proximity to different industrial sectors explain spatial variation in PFAS concentrations and PFAS composition in 
French environmental measurements?

## Data description

Early 2023, the [Forever Pollution Project](https://foreverpollution.eu/) showed that nearly 23,000 sites all over Europe are contaminated by the 
forever chemicals PFAS. This unique collaborative cross-border and cross-field investigation by 16 European newsrooms 
revealed an additional 21,500 presumptive contamination sites due to current or past industrial activity. PFAS
contamination spreads all over Europe.

In January 2024, the [Centre national de la recherche scientifique](https://www.cnrs.fr/) (CNRS) compiled a large dataset based on the Forever 
Pollution Project’s data containing all available PFAS measurements across Europe. This dataset was visualized using a
map in the [PFAS Data Hub](https://pdh.cnrs.fr/) (PDH) project. The creation of the dataset is documented on the 
[PDH data processing page](https://pdh.cnrs.fr/en/data_doc/).

This data source can be retrieved and used for scientific purposes.

# Setup
First, copy ``/.env.template`` to ``/.env``
Then adjust the values in it according to the documentation inside

# Infrastructure
The infrastructure is managed using docker compose. Spin it up for the first time using [make](https://www.gnu.org/software/make/):

```bash
make build
```

_or alternatively copy the command from the @docker line below_ `build:` _in the file `./Makefile`_

After building once, the infrastructure can be run using 

```bash
make up
```

Stopping the containers while keeping the data volumes can be done with this command:

```bash
make down
```

## MLflow
[MLflow](https://mlflow.org/) is an experiment tracking tool for model development. PFAS trace uses it locally (for now)
to track the results and progress of different models.
To persist experiments, the data is stored in a [PostgreSQL](https://www.postgresql.org/) database locally in a docker 
container.

# License
proprietary (for now)