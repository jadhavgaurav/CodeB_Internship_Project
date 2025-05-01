import re
import requests
import tldextract
import pandas as pd
import numpy as np
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

# API Keys from .env
OPENPAGERANK_API_KEY = os.getenv("OPEN_PAGERANK_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")


def extract_features_from_url(url):
    parsed = urlparse(url)
    hostname = parsed.hostname or ''
    path = parsed.path or ''

    ext = tldextract.extract(url)
    domain = ext.domain
    subdomain = ext.subdomain

    digits_in_host = sum(c.isdigit() for c in hostname)
    digits_in_url = sum(c.isdigit() for c in url)

    longest_words_raw = max([len(w) for w in re.split(r'\W+', url) if w] or [0])
    domain_in_title = get_domain_in_title(url, domain)
    ratio_digits_host = digits_in_host / len(hostname) if hostname else 0
    nb_dots = url.count(".")
    shortest_word_host = min([len(w) for w in hostname.split(".") if w] or [0])
    google_index = get_google_index_status(url)
    ratio_digits_url = digits_in_url / len(url) if url else 0
    avg_word_path = np.mean([len(w) for w in re.split(r'\W+', path) if w]) if path else 0
    phish_hints = int(any(k in url.lower() for k in ["login", "update", "secure", "ebayisapi", "webscr"]))
    nb_www = url.count("www")
    nb_qm = url.count("?")
    length_words_raw = sum(len(w) for w in re.split(r'\W+', url) if w)
    ratio_intHyperlinks = get_ratio_int_hyperlinks(url)
    page_rank = get_page_rank_from_openpagerank(hostname)

    features = {
        'shortest_word_host': shortest_word_host,
        'nb_www': nb_www,
        'phish_hints': phish_hints,
        'ratio_digits_host': ratio_digits_host,
        'google_index': google_index,
        'longest_words_raw': longest_words_raw,
        'ratio_digits_url': ratio_digits_url,
        'length_words_raw': length_words_raw,
        'avg_word_path': avg_word_path,
        'nb_qm': nb_qm,
        'nb_dots': nb_dots,
        'page_rank': page_rank,
        'domain_in_title': domain_in_title,
        'ratio_intHyperlinks': ratio_intHyperlinks
    }

    return pd.DataFrame([features])


def get_page_rank_from_openpagerank(domain):
    try:
        response = requests.get(
            "https://openpagerank.com/api/v1.0/getPageRank",
            headers={"API-OPR": OPENPAGERANK_API_KEY},
            params={"domains[]": domain},
            timeout=5
        )
        data = response.json()
        return data['response'][0].get('page_rank_integer', 0)
    except Exception as e:
        print("PageRank fetch failed:", e)
        return 0


def get_ratio_int_hyperlinks(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_links = soup.find_all('a', href=True)
        internal = [a for a in all_links if urlparse(a['href']).netloc in urlparse(url).netloc]
        return len(internal) / len(all_links) if all_links else 1.0
    except Exception as e:
        print("Internal hyperlink ratio error:", e)
        return 1.0


def get_domain_in_title(url, domain):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.lower() if soup.title else ''
        return int(domain.lower() in title)
    except:
        return 0


def get_google_index_status(url):
    try:
        query = f"site:{url}"
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": GOOGLE_API_KEY,
                "cx": GOOGLE_CSE_ID,
                "q": query
            },
            timeout=5
        )
        result = response.json()
        return 1 if "items" in result and len(result["items"]) > 0 else 0
    except Exception as e:
        print("Google index check failed:", e)
        return 1
