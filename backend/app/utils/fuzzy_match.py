from fuzzywuzzy import process, fuzz

def find_closest_match(input_text: str, choices: list, threshold: int = 60) -> str:
    """Find closest match using fuzzy string matching without Levenshtein optimization"""
    if not choices:
        return input_text
        
    # Use the default scorer (fuzz.WRatio) which doesn't require Levenshtein
    match, score = process.extractOne(input_text, choices, scorer=fuzz.WRatio)
    return match if score >= threshold else input_text