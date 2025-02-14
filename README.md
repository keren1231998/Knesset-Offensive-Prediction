# Reasearch Question:
How accurately can machine learning models predict harmful language in Knesset protocols before it occurs? 

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
2. The second filter detects formal parliamentary order calls and interrupts.  
3. For the order calls, the script retains the surrounding conversational context within a radius of three interactions.  

# Step 4: Classification Using DictaLM

This step involves using the DictaLM 2.0 model to classify potentially harmful or disrespectful language in Knesset protocols. The classification process is implemented in two main scripts that handle different aspects of language classification.

## Dependencies

```bash
pip install transformers torch pandas tqdm
```

## Models and Resources

- Model: `dicta-il/dictalm2.0-instruct`
- Hardware Requirements: CUDA-capable GPU
- Input: Preprocessed CSV files containing Knesset protocol conversations

## Classification Types

### 1. Disrespectful Language Classification

The first script (`Classifier/dicta_call_2_order_cut_radius.py`) identifies disrespectful language in conversations by:
- Analyzing conversations around formal order calls
- Examining a window of ±3 interactions around each order call
- Classifying responses as respectful or disrespectful

### 2. Offensive Language Classification

The second script (`Classifier/dicta_script_offensive.py`) specifically focuses on detecting offensive language by:
- Processing batches of conversations
- Using a specialized lexicon of offensive words
- Handling special cases like the word "נוכל" (can be either offensive or neutral based on context)

## Implementation Details

### Model Initialization
```python
model = AutoModelForCausalLM.from_pretrained(
    "dicta-il/dictalm2.0-instruct", 
    torch_dtype=torch.bfloat16, 
    device_map="cuda"
)
tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictalm2.0-instruct")
```

### Classification Process

1. **Input Processing**
   - Reads CSV files containing conversations
   - Identifies conversations marked for analysis
   - Prepares prompts with examples and context

2. **Model Querying**
   - Uses chat template format for queries
   - Implements specific prompts for different classification types
   - Handles batch processing with memory management

3. **Output Processing**
   - Classifies responses as binary (yes/no)
   - Saves results in separate CSV files
   - Updates original dataframe with classification results
