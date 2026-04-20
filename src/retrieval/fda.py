import requests


def search_drug_label(drug_name: str) -> dict:
    base_url = "https://api.fda.gov/drug/label.json"

    try:
        # Try generic name first
        response = requests.get(f'{base_url}?search=openfda.generic_name:"{drug_name}"&limit=1')
        if response.status_code == 200 and response.json().get("results"):
            return response.json()

        # Fall back to brand name
        response = requests.get(f'{base_url}?search=openfda.brand_name:"{drug_name}"&limit=1')
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"FDA lookup failed for {drug_name}: {e}")
        return None


def extract_sections(label: dict, drug_name: str) -> list[dict]:
    sections = []
    sections_to_extract = [
        "warnings",
        "contraindications",
        "adverse_reactions",
        "drug_interactions",
        "dosage_and_administration",
        "indications_and_usage"
    ]

    result = label["results"][0]

    for section in sections_to_extract:
        if section in result and result[section]:
            sections.append({
                "title": f"FDA Drug Label — {drug_name} — {section.replace('_', ' ').title()}",
                "abstract": result[section][0],
                "pmid": f"FDA-{drug_name}-{section}"
            })

    return sections