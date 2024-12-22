
# E-commerce Crawler

A **Scrapy-based** solution to discover and list **product URLs** across multiple e-commerce domains. Handles deep site hierarchies, dynamic content (e.g., AJAX, Load More Button), and parallel crawling.

## Key Features

-   **Multiple Domains**: Easily scale to hundreds of domains.
-   **URL Discovery**: Identifies product pages using patterns like `/product/`, `/item/`, `/p/`.
-   **Scalability & Performance**: Parallel/asynchronous crawling for large sites.
-   **Robustness**: Covers edge cases (infinite scrolling, dynamic loading).
-   **Unified Output**: Aggregates unique product URLs per domain into a single JSON file.

## Usage

1.  **Install Dependencies** 
`pip install -r requirements.txt`
2. **Configure Spiders**
-   Add/update start URLs or domain lists in `spiders/*.py`.
-   Adjust URL patterns if needed.
3. **Run All Spiders in Parallel**
`python run_all_spiders.py`
- This collects product URLs in `output.ndjson`, then creates a **`combined_output.json`** mapping each domain to its discovered product URLs.

## Project Structure


    ├─ ecommerce_crawler/
    │  ├─ __init__.py
    │  ├─ items.py
    │  ├─ pipelines.py       # NDJSON pipeline
    │  ├─ settings.py        # Scrapy settings (parallelism, etc.)
    │  ├─ run_all_spiders.py # Orchestrates parallel crawls & unifies output
    │  └─ spiders/
    │     ├─ base_ecommerce_spider.py
    │     ├─ ajax_ecommerce_spider.py
    │     ├─ load_more_spider.py
    │     └─ ... (others)
    ├─ requirements.txt
    ├─ README.md
    ├─ output.ndjson         # Newline Delimited JSON file containing each spider results
    ├─ combined_output.json  # Combined result of all spiders in JSON format

## Output

-   **combined_output.json**
    -   A single JSON mapping each domain to its list of **unique** product URLs.
