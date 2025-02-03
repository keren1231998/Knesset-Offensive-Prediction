# Reasearch Question:
How party affiliation affects the tone of discourse and interactions between Knesset members in debates?

## Pipeline Steps

### Step 1: Protocol Collection (`get_protocols.ipynb`)
First, we collect and filter the relevant protocols from the Knesset's official repository:

This script:
- Scrapes protocols from the oknesset.org website
- Filters relevant protocols 
- Saves filtered protocols to the `text/` directory

### Step 2: Protocol Preprocessing (`preprocessing.ipynb`)
After collecting the protocols, we preprocess them to ensure data quality and consistency:
credit to https://github.com/nogaschw/Call-to-order/tree/main

This script:

![image](https://github.com/user-attachments/assets/0821ad0d-2b0d-4fad-93ac-3a453f96b50b)

### Step 3: Data Heuristic for Offensive Language  
The script applies a data heuristic with three distinct patterns to identify relevant interactions within Knesset protocols.  
1. The first filter flags suspected offensive language using a Hebrew lexicon [Chaya Liebeskind et al., 2023].  
2. The second filter detects formal parliamentary order calls.  
3. For the order calls, the script retains the surrounding conversational context within a radius of three interactions.  

## Step 4: Classification
![image](https://github.com/user-attachments/assets/aca54f6a-5375-467b-b800-602adea2b1d6)
