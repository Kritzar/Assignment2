import argparse
import csv
from work.paper_fetcher import fetch_papers

def main():
    
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

    args = parser.parse_args()
    query = args.query
    output_file = args.file
    debug = args.debug

    if debug:
        print(f"Fetching papers for query: {query}")

    papers = fetch_papers(query)

    if output_file:
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"],
            )
            writer.writeheader()
            writer.writerows(papers)
        if debug:
            print(f"Results saved to {output_file}")
    else:
        for paper in papers:
            print(paper)


if __name__ == "__main__":
    main()
