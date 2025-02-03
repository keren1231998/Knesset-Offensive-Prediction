import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from datetime import datetime
import logging
import gc  # Add this import
from tqdm import tqdm

device = "cuda"

model = AutoModelForCausalLM.from_pretrained("dicta-il/dictalm2.0-instruct", torch_dtype=torch.bfloat16, device_map=device)
tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictalm2.0-instruct")
batch_num = 4
batch_path = f"/home/itayraz/nlp_course/cutt&&call_offensive/offensive/batch_{batch_num}_offensive.csv"
df = pd.read_csv(batch_path)



print("_"*50)
print(f'batch name: {batch_path}')
print("_"*50)

example = """
דוגמאות:
המילים: גנב
המשפט: אם בא בעל מניות וגנב ממפעל 25 מיליון שקלים. האם המדינה צריכה לתת את התשובה על זה? אני נותן דוגמה אבסטרקטית..
תשובה: לא, המילה גנב לא נאמרת באופן פוגעני

המילים: מפגרים
המשפט: "כלב שמירה זה מונח בסדר... כאן אנחנו מפגרים אחרי למעלה מ-40 מדינות..."
שאלה: האם המילים נאמרו באופן פוגעני?
תשובה: לא

המילים: גנב
המשפט: אתה גנב וכולכם פה גונבים את המידה
תשובה: כן, המילה גנב נאמרה באופן פוגעני

המילים: תסתום
המשפט: צריך לסתום את החומה כדי שלא יכנסו
תשובה: לא, המילה תסתום לא נאמרה בפירוש פוגעני

המילים: תסתום
המשפט: תסתום את הפה עכשיו. חצוף שכמוך. אתה בא לאיים עליי כל הזמן? אתה חושב שאני מפחד ממך?
תשובה: כן, המילה תסתום נאמרה בפירוש פוגעני

המילים: נוכל 
המשפט: אנחנו נוכל לבנות פה הרבה דברים אך לא הכל 
תשובה: לא, המילה נוכל לא נאמרה בפירוש בפוגעני אלא כפועל 

שימו לב שההקשר הוא המכריע: ייתכן שיש למילה שתי משמעויות ("נוכל" כפועל לעומת "נוכל" ככינוי גנאי). ההחלטה מתקבלת לפי כוונת דובר המשפט – האם היא פוגענית/מעליבה או ניטרלית/תיאורית?
"""

example_nohel = """
דוגמאות:

המשפט: "אל תאמין למילה שלו, הוא נוכל מהיום שנולד"
תשובה: כן, המילה נוכל משמשת כמילת גנאי לתיאור אדם לא אמין


המשפט: "נוכל לבקר אותך מחר אם מתאים לך"
תשובה: לא, המילה נוכל מציינת אפשרות או יכולת לעשות פעולה

המשפט:"גופים אלה ייבחרו על-ידי הנוער במהלך החודש הקרוב, ביניהם נוכל למצוא את התיכון, תנועת הנוער או היחידה הצבאית"
תשובה: לא, המילה נוכל מציינת אפשרות או יכולת לעשות פעולה


"בניתוח משפט הכולל את המילה 'נוכל', בדוק את ההקשר הדקדוקי והסמנטי:

1. אם המילה 'נוכל' מופיעה כשם עצם ומתארת אדם (למשל: 'הוא נוכל'), סביר שזו מילת גנאי.

2. אם המילה 'נוכל' מופיעה כפועל בעתיד בגוף ראשון רבים (אנחנו) ומתארת יכולת או אפשרות לבצע פעולה (למשל: 'נוכל ללכת'), זו אינה מילת גנאי.

3. סמנים נוספים למילת גנאי:
   - מופיעה בהקשר של אזהרה ('תיזהר ממנו, הוא נוכל')
   - מלווה בתיאורים שליליים ('נוכל מרושע', 'נוכל ורמאי')
   - משמשת ככינוי גנאי ישיר ('נוכל שכמוך')

4. סמנים לשימוש חיובי:
   - מופיעה לפני פועל בשם הפועל ('נוכל ללכת', 'נוכל לבוא')
   - מתארת אפשרות או יכולת לבצע פעולה
   - משמשת בהקשר של תכנון או הצעה חיובית"
"""

# Function to query the model
def query_model(words, lines,example):
    # Construct the chat template
    messages = [
        {"role": "user", "content": example},  # Example context
        {"role": "assistant", "content": "הבנתי. דוגמה ברורה."},  # Assistant acknowledges the example
        {
            "role": "user",
            "content": f'המילים: "{words}"\nהמשפט: "{lines}"\nשאלה: האם המילים נאמרו בטקסט באופן פוגעני?\nתשובה: רק כן או לא.'
        },
    ]
    
    encoded = tokenizer.apply_chat_template(messages, return_tensors="pt").to(device)

    # Generate the response
    generated_ids = model.generate(encoded, max_new_tokens=50, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
    return decoded

# Function to query the model
def query_model_nohel(words, lines,example):
    # Construct the chat template
    messages = [
        {"role": "user", "content": example},  # Example context
        {"role": "assistant", "content": "הבנתי. דוגמה ברורה."},  # Assistant acknowledges the example
        {
            "role": "user",
            "content": f'המשפט: "{lines}"\nשאלה: האם המילה נוכל נאמרה באופן לא מכבד?\nתשובה: רק כן או לא.'
        },
    ]
    
    encoded = tokenizer.apply_chat_template(messages, return_tensors="pt").to(device)

    # Generate the response
    generated_ids = model.generate(encoded, max_new_tokens=50, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
    return decoded

yes_responses = []
no_responses = []


# Counter for iterations
iteration_counter = 0

total_rows = len(df)

# Initialize progress bar with tqdm
progress_bar = tqdm(total=total_rows, desc="Processing rows", unit="row")

processed_rows = 0

for index, row in df.iterrows():
    iteration_counter += 1  # Increment counter
    if row['contain_offensive_words'] == 0:
        progress_bar.update(1)  # Update progress bar even if skipping
        continue  # Skip this row

    processed_rows += 1
    words = row['offensive_words']
    lines = row['conversation']
    file_name = row['session_id']
    
    if "נוכל" in words: 
        example = example_nohel
        prompt = f'המשפט: "{lines}"\nשאלה: האם המילה נוכל נאמרה באופן לא מכבד?\nתשובה: רק כן או לא.'
    else:
        prompt = f'המילים: "{words}"\nהמשפט: "{lines}"\nשאלה: האם המילים נאמרו בטקסט באופן פוגעני?\nתשובה: רק כן או לא.'
    
    assist = "הבנתי. דוגמה ברורה."
    combine = example + assist + prompt
    combine = combine.strip().split()
    
    try:
        if "נוכל" in words: 
            response = query_model_nohel(words, lines, example).strip()  # Strip any whitespace from the response
        else:
            response = query_model(words, lines, example).strip()  # Strip any whitespace from the response
            
        indx = len(combine)
        first_word = response.split()[indx+5:indx+9]  # Extract the first few words
        print("First word is: " + " ".join(first_word))
        
        filtered_response = [item for item in response.split() if item not in ["[INST]", "[/INST]"]]
        filtered_response = filtered_response[len(combine):]
        response_string = " ".join(filtered_response)
        
        row_with_response = {
            'file_name': file_name,
            'words': words,
            'lines': lines,
            'response': response_string  
        }
        
        # Classify based on the first word
        if "כן" in first_word:  # If the first word is "כן"
            print("Yes example: " + words)
            yes_responses.append(row_with_response)
            df.at[index, 'dicta_answer'] = 1  # Add 1 to the new column for Yes
        elif "לא" in first_word:  # If the first word is "לא"
            print("No example: " + words)
            no_responses.append(row_with_response)
            df.at[index, 'dicta_answer'] = 0  # Add 0 to the new column for No
        else:
            print(f"Unclear response for row {index}: {response}")
            df.at[index, 'dicta_answer'] = None  # Handle errors gracefully
    except Exception as e:
        print(f"Error processing row {index}: {e}")
        df.at[index, 'dicta_answer'] = None  # Handle errors gracefully

    # Clear cache and force garbage collection every 100 iterations
    if iteration_counter % 100 == 0:
        torch.cuda.empty_cache()
        gc.collect()
    
    # Update progress bar
    progress_bar.update(1)

# Close the progress bar
progress_bar.close()

# Convert the results into separate DataFrames
yes_df = pd.DataFrame(yes_responses)
no_df = pd.DataFrame(no_responses)

# Save the results to separate CSV files with desired columns
yes_df.to_csv(f"/home/itayraz/nlp_course/cutt&&call_offensive/offensive_response/yes_offe_batch{batch_num}.csv", columns=['file_name', 'words', 'lines', 'response'], index=False)
no_df.to_csv(f"/home/itayraz/nlp_course/cutt&&call_offensive/offensive_response/no_ffe_batch{batch_num}.csv", columns=['file_name', 'words', 'lines', 'response'], index=False)
df.to_csv(f"/home/itayraz/nlp_course/cutt&&call_offensive/offensive_response/updated_original_df_offe_batch{batch_num}_df.csv", index=False)

print("Processing completed. Results saved.")