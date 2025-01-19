
# Function to check if any calls_to_order word exists in the conversation
def contains_cut(conversation):
    """
    Check if any calls_to_order word exists in the conversation and return 1 if found, else 0.
    """
    list_2=["- -"]
    if isinstance(conversation, str):  
        return 1 if any(word in conversation for word in list_2) else 0
    return 0  #


calls_to_order = ['אני קורא אותך לסדר', 'אני קוראת אותך לסדר', 'זאת אזהרה אחרונה',
                'קריאה לסדר', 'קריאת ראשונה לסדר', 'אני מזהיר אותך', 'קורא אותך',
                'קוראת אותך', 'קורא לך לסדר', 'קוראת לך לסדר']

# Function to check if any calls_to_order word exists in the conversation
def contains_calls_to_order(conversation, calls_to_order):
    """
    Check if any calls_to_order word exists in the conversation and return 1 if found, else 0.
    """
    if isinstance(conversation, str):  
        return 1 if any(word in conversation for word in calls_to_order) else 0
    return 0  
