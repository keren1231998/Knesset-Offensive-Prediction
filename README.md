This repository contains a pipeline for analyzing Knesset protocols, focusing on identifying and processing parliamentary discourse.

## Pipeline Steps

### Step 1: Protocol Collection (`get_protocols.py`)
First, we collect and filter the relevant protocols from the Knesset's official repository:

```
python get_protocols.py
```

This script:
- Scrapes protocols from the oknesset.org website
- Filters protocols containing calls to order or harmful language
- Saves filtered protocols to the `text/` directory
- Handles Hebrew text encoding (UTF-8-sig)

### Step 2: Protocol Preprocessing (`preprocessing.py`)
After collecting the protocols, we preprocess them to ensure data quality and consistency:

```bash
python preprocessing.py
```

This script:
- Unifies committee names using Levenshtein distance
- Splits long conversations into manageable segments
- Processes speaker information using DICTA-BERT NER
- Saves preprocessed data to specified output path
