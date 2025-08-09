import re
from typing import List  # Bu satırı ekleyin

def parse_locations(gpt_response: str) -> List[str]:
    """GPT yanıtından lokasyonları çıkarır"""
    pattern = r'\d+\.\s*(.*?)(?=\n|$)'
    return re.findall(pattern, gpt_response)