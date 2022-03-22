import pathlib
import requests
import pandas as pd

from typing import Sequence
from urllib.parse import urlencode


def _get_ccf_class(venue: str) -> str:
    ccf_catalog = pathlib.Path(__file__).parent.joinpath('data').joinpath('ccf_catalog.csv')
    df = pd.read_csv(ccf_catalog)
    if len(series := df.loc[df.get('abbr').str.lower() == venue.lower(), 'class']) > 0:
        return series.item()
    elif len(series := df.loc[df.get('url').str.contains(f'/{venue.lower()}/'), 'class']) > 0:
        return series.item()
    return 'N/A'


def search(queries: Sequence, verbose: int = 0) -> Sequence:
    url = 'http://dblp.org/search/publ/api'
    results = []
    for query in queries:
        entry = {
            'Query': query,
            'Title': 'N/A',
            'Year': 'N/A',
            'Venue': 'N/A',
            'CCF Class': 'N/A',
            'DOI': 'N/A',
            'URL': 'N/A',
            'BibTeX': 'N/A'
        }
        options = {
            'q': query,
            'format': 'json',
            'h': 1
        }
        r = requests.get(f'{url}?{urlencode(options)}').json()
        hit = r.get('result').get('hits').get('hit')
        if hit is not None:
            info = hit[0].get('info')
            entry['Title'] = info.get('title')
            entry['Year'] = info.get('year')
            entry['Venue'] = info.get('venue')
            entry['CCF Class'] = _get_ccf_class(entry.get('Venue'))
            entry['DOI'] = info.get('doi')
            entry['URL'] = info.get('ee')
            entry['BibTeX'] = f'{info.get("url")}?view=bibtex'
        results.append(entry)
        if verbose > 0:
            print(f'DBLP: {entry}')
    return results

# reault = search(['The Undergraduate Games Corpus: A Dataset for Machine Perception of Interactive Media'])
# print(reault)