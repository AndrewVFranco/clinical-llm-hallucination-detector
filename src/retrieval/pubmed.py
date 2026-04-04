import requests
from src.core.config import settings

def search_pubmed(query: str, max_results: int = 10) -> list[dict]:
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    esearch_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "api_key": settings.NCBI_API_KEY
    }

    try:
        response = requests.get(f"{base_url}esearch.fcgi", params=esearch_params)
        response.raise_for_status()
        pmids = response.json()["esearchresult"]["idlist"]

        pmids = ",".join(pmids)

        efetch_params = {
            "db": "pubmed",
            "id": pmids,
            "retmode": "XML",
            "api_key": settings.NCBI_API_KEY
        }

        raw_data = requests.get(f"{base_url}efetch.fcgi", params=efetch_params)
        raw_data.raise_for_status()

        return raw_data.text
    except Exception as e:
        print(f"Error: {e}")

