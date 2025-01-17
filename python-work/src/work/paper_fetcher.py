from typing import List, Dict, Optional
from Bio import Entrez
import csv
import re


Entrez.email = "innocentsoul199@gmail.com" 

def fetch_papers(query: str, max_results: int = 50) -> List[Dict]:
    
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    #handle = Entrez.esearch(db="nucleotide", retmax=10, term="opuntia[ORGN] accD", idtype="acc")
    record = Entrez.read(handle)
    handle.close()

    pubmed_ids = record["IdList"]
    results = []
    for pubmed_id in pubmed_ids:
        details = fetch_paper_details(pubmed_id)
        if details:
            results.append(details)
    return results


def fetch_paper_details(pubmed_id: str) -> dict:
    

    handle = Entrez.efetch(db="pubmed", id=pubmed_id, rettype="medline", retmode="xml")
    record = Entrez.read(handle)
    handle.close()
    # for key, val in record.items():
    #     print(key)
    #     print(val) 
    #     print("\n")
    if not record["PubmedArticle"]:
        return {} 
    title = record["PubmedArticle"][0]["MedlineCitation"]["Article"]["ArticleTitle"]
    pub_date = record["PubmedArticle"][0]["MedlineCitation"]["Article"]["ArticleDate"]
    authors = record["PubmedArticle"][0]["MedlineCitation"]["Article"].get("AuthorList", [])

    non_academic_authors = []
    company_affiliations = []
    corresponding_email = None

    for author in authors:
        if "AffiliationInfo" in author and author["AffiliationInfo"]:
            # Safely access AffiliationInfo and Affiliation
            affiliation = author["AffiliationInfo"][0].get("Affiliation", "")
            if is_non_academic(affiliation):
                non_academic_authors.append(author.get("LastName", ""))
                company_affiliations.append(extract_company_name(affiliation))
                if corresponding_email is None:  # Save the first email 
                    corresponding_email = extract_email(affiliation)

    pub_date_str = f"{pub_date[0]['Year']}-{pub_date[0]['Month']}-{pub_date[0]['Day']}" if pub_date else "Unknown"

    return {
        "PubmedID": pubmed_id,
        "Title": title,
        "Publication Date": pub_date_str,
        "Non-academic Author(s)": ", ".join(non_academic_authors),
        "Company Affiliation(s)": ", ".join(company_affiliations),
        "Corresponding Author Email": corresponding_email or "N/A",
    }




def is_non_academic(affiliation: str) -> bool:
    """Check if the affiliation belongs to a non-academic institution."""
    return bool(re.search(r"Inc\.|Ltd\.|Pharma|Biotech|Company|Corp\.", affiliation))


def extract_company_name(affiliation: str) -> Optional[str]:
    """Extract company name from affiliation text."""
    match = re.search(r"(?:Inc\.|Ltd\.|Pharma|Biotech|Company|Corp\.)(.*?)(?=,|$)", affiliation)
    return match.group(0).strip() if match else None


def extract_email(affiliation: str) -> Optional[str]:
    """Extract email address from affiliation text."""
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", affiliation)
    return match.group(0) if match else None
