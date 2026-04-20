from src.retrieval.fda import search_drug_label, extract_sections
import sys

def main():
    drug_name = "warfarin"
    search_results = search_drug_label(drug_name)
    results = extract_sections(search_results, drug_name)
    print(results)

if __name__ == "__main__":
    sys.exit(main())