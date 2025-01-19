def get_urls():
    """
    Scrapes and retrieves URLs of text files containing Knesset protocols from the oknesset website.
    
    This function performs a recursive crawl of the oknesset website's directory structure,
    collecting URLs of all .txt files containing committee meeting protocols.
    
    Returns:
        list[str]: A list of complete URLs pointing to .txt files containing Knesset protocols.
    """
    url = 'https://production.oknesset.org/pipelines/data/committees/meeting_protocols_text/files/'
    folder_urls = [url]
    urls = []

    while(len(folder_urls) > 0):
        curr_url = folder_urls.pop(0)
        response = requests.get(curr_url, allow_redirects=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            all_links = soup.find_all('a')
            file_names = [link.text for link in all_links if link.text]
            file_names = [file_name for file_name in file_names if file_name != '..']
            for file_name in file_names:
                if file_name.endswith('/') and file_name != '../':
                    folder_urls.append(curr_url + file_name)
                elif file_name.endswith('.txt'):
                    urls.append(curr_url + file_name)
        else:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
    return urls

def filter_by_call_to_order(text):
    """
    Analyzes text for presence of harmful language or procedural interventions like calls to order.
    
    This function checks if the input text contains any words or phrases from a predefined list
    of offensive words in Hebrew and procedural interventions commonly used in the Knesset.
    
    The detection covers several categories:
    - Offensive and derogatory terms in Hebrew
    - Procedural phrases (e.g., "קריאה לסדר" - call to order)
    - Disruption markers (e.g., "- - -" indicating interruptions)
    
    Args:
        text (str): The text content to analyze, expected to be in Hebrew
    
    Returns:
        bool: True if harmful language or procedural interventions are detected, False otherwise
    """
    offensive_words = [
        "אהצבועה", "אובססיבית", "איכס", "אינעל", "שמוק", "דביל", "בולבול", 
        # ... [rest of the offensive words list]
    ]
    for word in offensive_words:
        if word in text:
            return True
    return False

def get_text(url, dir='text'):
    """
    Retrieves, processes, and conditionally saves Knesset protocol text files.
    
    This function downloads protocol text from a given URL, processes it for consistency,
    and saves it to a file if it contains harmful language or calls to order.
    
    Args:
        url (str): Complete URL to the protocol text file
        dir (str, optional): Directory where filtered protocols should be saved.
            Defaults to 'text'.
    """
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = 'utf-8-sig'
        if not os.path.exists(dir):
            os.makedirs(dir)
        text = response.text
        text = text.replace('"', '"').replace('"', '"').replace('״', '"')
        if filter_by_call_to_order(text):
            text = re.split('\n', text)
            with open(f'{dir}/{url.split("/")[-1]}', 'x', encoding='utf-8-sig') as file:
                file.write('\n'.join(text))
        else:
            print(f"Not found offensive words in {url}.")
    else:
        print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
        return None
