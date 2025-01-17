# Assignment
# PubMed Papers Fetcher

A Python-based tool to fetch research papers from PubMed using the Biopython library. This tool allows you to search for papers using a query, export the results to a CSV file, and include detailed information about the search results.

## Features
- Search PubMed for research papers with a specified query.
- Export the search results to a CSV file.
- Include additional details in the output file with the `--detailed` option.

To run the program run following command:
poetry build
to test the dev:
poetry run get-papers-list "diabetes therapy" -f results.csv -d
