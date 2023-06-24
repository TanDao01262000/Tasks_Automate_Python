import re


# clear all urls and non-readable characters in the text
def clean_string(content):
    final_text = re.sub(r"\[.*?\]", "", content)
    final_text = re.sub(r"\r\n|\n|\r", "", final_text)  
    final_text = re.sub(r"\t", "", final_text) 
    final_text = re.sub(r"\uf8ff.", "", final_text) 

    return final_text




