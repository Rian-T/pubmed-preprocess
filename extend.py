import os
from tqdm import tqdm

# LangChain imports remain the same
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

folder_path = "extended_clinical_cases"
os.makedirs(folder_path, exist_ok=True)

llm = ChatOllama(model="gemma2")
prompt = ChatPromptTemplate.from_template(
    "Generate a realistic non-anonymized fictional French clinical case written in the style typical of a physician. "
    "Start from this, but feel free to invent and extend details such as full names, values and physical attributes, ensuring they are plausible: "
    "{topic}"
)
chain = prompt | llm | StrOutputParser()

# Determine the number of lines (clinical cases) to process for progress tracking
with open("clinical_cases.txt", "r") as f:
    total_cases = sum(1 for _ in f)

# Re-open the file to process it
with open("clinical_cases.txt", "r") as f:
    for i, line in enumerate(
        tqdm(f, total=total_cases, desc="Processing clinical cases")
    ):
        extended_case = chain.invoke({"topic": line.strip()})
        file_path = os.path.join(folder_path, f"clinical_case_{i}.txt")
        with open(file_path, "w") as case_file:
            case_file.write(extended_case)
