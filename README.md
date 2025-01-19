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

![image](https://github.com/user-attachments/assets/217ee9f6-2e9e-42fa-a98e-37dd2213b072)
