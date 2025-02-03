# -*- coding: utf-8 -*-
"""dicta_call_2_order_radius.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/104kimeFUBaNoqcOuHjGbtcTZDtRcECsA
"""

import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

device = "cuda"

model = AutoModelForCausalLM.from_pretrained("dicta-il/dictalm2.0-instruct", torch_dtype=torch.bfloat16, device_map=device)
tokenizer = AutoTokenizer.from_pretrained("dicta-il/dictalm2.0-instruct")

df = pd.read_csv(r"/home/itayraz/nlp_course/dicta_responses/my_data_update_cutcall.csv")

def process_conversations(df, tokenizer, model, device, output_path):
    """
    Process conversations from a DataFrame to classify responses as respectful or disrespectful.

    Args:
        df (pd.DataFrame): Input DataFrame containing conversations
        tokenizer: The tokenizer object
        model: The language model
        device: The computing device (CPU/GPU)
        output_path (str): Path to save output files
    """
    example = """
    דוגמאות:

    המשפט: טוב טוב דבר כבר לעניין
    שאלה: האם המשפט נאמר באופן לא מכבד?
    תשובה: כן, המשפט נאמר באופן אשר לא מכבד את האדם שמדובר עליו

    המשפט: "נו, כמה זמן אני צריך לחכות לך?"
    שאלה: האם המשפט נאמר באופן לא מכבד?
    תשובה: כן, המשפט נאמר באופן אשר לא מכבד את האדם שמדובר עליו.

    המשפט: "בוא נתמקד, אין לי סבלנות לקטנות האלה."
    שאלה: האם המשפט נאמר באופן לא מכבד?
    תשובה: כן, המשפט נאמר באופן אשר לא מכבד את האדם שמדובר עליו.

    המשפט: "אתה גולש מהנושא, תנסה להישאר ענייני."
    שאלה: האם המשפט נאמר באופן לא מכבד?
    תשובה: כן, המשפט נאמר באופן אשר לא מכבד את האדם שמדובר עליו.

    המשפט: "מתי תבין שהגישה שלך לא מובילה לשום דבר?"
    שאלה: האם המשפט נאמר באופן לא מכבד?
    תשובה: כן, המשפט נאמר באופן אשר לא מכבד את האדם שמדובר עליו.

    המשפט: "האם תוכל בבקשה להסביר את הנקודה העיקרית?"
    שאלה: האם המשפט נאמר באופן לא מכבד?
    תשובה: לא, המשפט נאמר באופן מכבד ומנומס.

    המשפט: "אני מבין את הנקודה שלך, אבל חושב שכדאי שנתמקד בנושא המרכזי"
    שאלה: האם המשפט נאמר באופן לא מכבד?
    תשובה: לא, המשפט מביע כבוד לדעת האחר תוך הצעה מכבדת להתקדם.

    הנחיות לזיהוי משפט לא מכבד:
    - שימוש בטון מזלזל או סרקסטי
    - הבעת חוסר סבלנות או תסכול באופן ישיר
    - ביטול או זלזול בדעות/רעיונות של האחר
    - שימוש בציוויים ישירים ללא נימוס
    - שימוש במילים פוגעניות או משפילות
    """

    yes_responses = []
    no_responses = []

    def query_model(conversation):
        messages = [
            {"role": "user", "content": example},
            {"role": "assistant", "content": "הבנתי. דוגמה ברורה."},
            {
                "role": "user",
                "content": f'השיחה: "{conversation}"\nשאלה: האם המשפט נאמר באופן לא מכבד?\nתשובה: רק כן או לא.'
            },
        ]

        encoded = tokenizer.apply_chat_template(messages, return_tensors="pt").to(device)
        generated_ids = model.generate(encoded, max_new_tokens=50, do_sample=True)
        return tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    for index, row in df.iterrows():
        if row['contains_calls_to_order'] == 1:
            commite_num = row['session_id']
            index_2_check = [index-3, index-2, index-1, index, index+1, index+2, index+3]

            for idx in index_2_check:
                if 0 <= idx < len(df):
                    row_to_check = df.iloc[idx]
                    if row_to_check['session_id'] == commite_num:
                        conv = row_to_check['conversation']
                        try:
                            response = query_model(conv).strip()
                            prompt = f'השיחה: "{conv}"\nשאלה: האם המשפט נאמר באופן לא מכבד?\nתשובה: רק כן או לא.'
                            asist = "הבנתי. דוגמה ברורה."
                            combine = prompt + asist + example
                            combine = combine.strip().split()

                            indx = len(combine)
                            first_word = response.split()[indx+5] + response.split()[indx+6] + response.split()[indx+7] + response.split()[indx+8]

                            print_respose = response.strip().split()
                            filtered_respose = [item for item in print_respose if item not in ["[INST]", "[/INST]"]]
                            filtered_respose = filtered_respose[len(combine):]
                            response_string = " ".join(filtered_respose)

                            row_with_response = {
                                'file_name': commite_num,
                                'conv': conv,
                                'response': response_string
                            }

                            if "כן" in first_word:
                                yes_responses.append(row_with_response)
                                df.at[index, 'dicta_answer'] = 1
                            elif "לא" in first_word:
                                no_responses.append(row_with_response)
                                df.at[index, 'dicta_answer'] = 0
                            else:
                                print(f"Unclear response for row {index}: {response}")
                                df.at[index, 'dicta_answer'] = None

                        except Exception as e:
                            print(f"Error processing row {index}: {e}")
                            df.at[index, 'dicta_answer'] = None

    # Save results
    pd.DataFrame(yes_responses).to_csv(f"{output_path}_yes.csv", columns=['file_name', 'conv', 'response'], index=False)
    pd.DataFrame(no_responses).to_csv(f"{output_path}_no.csv", columns=['file_name', 'conv', 'response'], index=False)
    df.to_csv(f"{output_path}_all.csv", index=False)

    print("Processing completed. Results saved to CSV files.")

process_conversations(df, tokenizer, model, device, "output_path")