## Knesset Protocol Analysis Pipeline
A comprehensive framework for analyzing Israeli parliamentary discourse through Knesset protocols, with a focus on detecting procedural disruptions and harmful language patterns.
## Overview
This pipeline processes Knesset protocols through multiple stages, from data collection to advanced language analysis. It leverages both rule-based heuristics and machine learning approaches to identify various forms of parliamentary disruptions and problematic discourse.

## Pipeline Steps

### Step 1: Protocol Collection (`get_protocols.ipynb`)
First, we collect and filter the relevant protocols from the Knesset's official repository:

This script:
- Scrapes protocols from the oknesset.org website
- Filters protocols 
- Saves filtered protocols to the `text/` directory

### Step 2: Protocol Preprocessing (`preprocessing.ipynb`)
After collecting the protocols, we preprocess them to ensure data quality and consistency:
credit to https://github.com/nogaschw/Call-to-order/tree/main

This script:

![image](https://github.com/user-attachments/assets/0821ad0d-2b0d-4fad-93ac-3a453f96b50b)

### Step 3: Data Heuristics
The heuristic analysis consists of two main components:

#### 3.1 Protocol Filtering (`filter_heuristics.ipynb`)
Implements filtering based on:
- Call to Order Detection (קריאה לסדר)
- Interruption Analysis (- - -)


#### 3.2 Offensive Language Detection (`offensive_words_detector.ipynb`)
Provides comprehensive offensive language analysis:
- Outputs enhanced dataset with offensive language annotations

### Step 4: Classification
#### 4.1 DictaLM Analysis (Call_Cut_Dicta.ipynb)
- Utilizes DictaLM 2.0 Hebrew language model
Processes two types of classifications:
1. Procedural disruptions (with window=3 radius)
2. Harmful language instances
