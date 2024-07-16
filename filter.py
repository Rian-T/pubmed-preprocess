import re
from datasets import load_dataset

def is_clinical_case(text):
    pattern = re.compile(r"^(cas\s*\d+:\s*)?(mme|monsieur|mr|madame|il s'agit d'une patiente)\b", re.IGNORECASE)
    return bool(pattern.search(text))

def main():
    dataset = load_dataset("rntc/pubmed_preprocess", split="fr", streaming=True)
    # Use a list comprehension to filter clinical cases directly
    clinical_cases = [data for data in dataset if is_clinical_case(data["text"].split(".")[0])]
    
    # Write all clinical cases to the file in one go
    with open("clinical_cases.txt", "w") as f:
        f.writelines([case["text"] + "\n" for case in clinical_cases])

if __name__ == '__main__':
    main()