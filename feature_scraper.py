import re
import requests
import tldextract
import pandas as pd
import numpy as np
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

load_dotenv()

# Load API Key from .env
OPENPAGERANK_API_KEY = os.getenv("OPEN_PAGERANK_API_KEY")

def extract_features_from_url(url):
    parsed = urlparse(url)
    hostname = parsed.hostname or ''
    path = parsed.path or ''

    ext = tldextract.extract(url)
    domain = ext.domain
    suffix = ext.suffix
    subdomain = ext.subdomain

    digits_in_host = sum(c.isdigit() for c in hostname)
    digits_in_url = sum(c.isdigit() for c in url)

    # Feature 1: longest_words_raw
    longest_words_raw = max([len(w) for w in re.split(r'\W+', url) if w] or [0])

    # Feature 2: domain_in_title (hardcoded 0 since HTML is not fetched here)
    domain_in_title = 0

    # Feature 3: ratio_digits_host
    ratio_digits_host = digits_in_host / len(hostname) if hostname else 0

    # Feature 4: nb_dots
    nb_dots = url.count(".")

    # Feature 5: shortest_word_host
    shortest_word_host = min([len(w) for w in hostname.split(".") if w] or [0])

    # Feature 6: google_index (default 1 since Google API is paid)
    google_index = 1

    # Feature 7: ratio_digits_url
    ratio_digits_url = digits_in_url / len(url) if url else 0

    # Feature 8: avg_word_path
    path_words = re.split(r'\W+', path)
    avg_word_path = np.mean([len(w) for w in path_words if w]) if path_words else 0

    # Feature 9: phish_hints (based on heuristic keywords)
    phish_hints = int(any(keyword in url.lower() for keyword in ["login", "update", "secure", "ebayisapi", "webscr"]))

    # Feature 10: nb_www
    nb_www = url.count("www")

    # Feature 11: nb_qm
    nb_qm = url.count("?")

    # Feature 12: length_words_raw
    length_words_raw = sum(len(w) for w in re.split(r'\W+', url) if w)

    # Feature 13: ratio_intHyperlinks (assumed default)
    ratio_intHyperlinks = 1.0

    # Feature 14: page_rank
    page_rank = get_page_rank_from_openpagerank(hostname)

    # Construct feature vector
    features = {
        'longest_words_raw': longest_words_raw,
        'domain_in_title': domain_in_title,
        'ratio_digits_host': ratio_digits_host,
        'nb_dots': nb_dots,
        'shortest_word_host': shortest_word_host,
        'google_index': google_index,
        'ratio_digits_url': ratio_digits_url,
        'avg_word_path': avg_word_path,
        'phish_hints': phish_hints,
        'nb_www': nb_www,
        'nb_qm': nb_qm,
        'length_words_raw': length_words_raw,
        'ratio_intHyperlinks': ratio_intHyperlinks,
        'page_rank': page_rank
    }

    return pd.DataFrame([features])

def get_page_rank_from_openpagerank(domain):
    try:
        response = requests.get(
            "https://openpagerank.com/api/v1.0/getPageRank",
            headers={"API-OPR": OPENPAGERANK_API_KEY},
            params={"domains[]": domain}
        )
        data = response.json()
        return data['response'][0].get('page_rank_integer', 0)
    except Exception as e:
        print("PageRank fetch failed:", e)
        return 0

input_url = input("Enter a URL to extract features from: ")
if not input_url.startswith("http"):
    input_url = "http://" + input_url
    
feature_df = extract_features_from_url(input_url)
print(feature_df)