# LLM Code Review Benchmark - AAS Assignment 1

This repository contains the experimental pipeline developed for benchmarking the Gemini 2.5 Flash model on secure code review tasks, using a test suite based on the OWASP Top 10 (2021) categories.

## Project Structure:

| Path            | Description |
|-------------------|----------|
| `src/`            | Python source code for the evaluation pipeline |
| `prompts/`        | Prompt templates (simple and structured strategies) |
| `dataset/`        | JSON file containing the 20 vulnerable code samples |
| `results/`        | Raw API responses and computed metrics |
| `logs/`           | Execution logs |
| `requirements.txt`| Python dependencies |
| `.gitignore`      | Specifies which files Git should ignore |

## Requirements:

- Python 3.11 or higher
- Python Virtual Environment tool (venv)
- A valid Gemini API key from Google AI Studio

## Setup and Execution

1. Clone the repository to your local machine.
2. Create and activate a Python virtual environment:
   `python3 -m venv venv`
   `source venv/bin/activate`

3. Install the required dependencies:
   `pip install -r requirements.txt`

4. Create a .env file in the project root directory with your API key:
   `GEMINI_API_KEY=your_api_key_here`

5. Run the main pipeline script:
   `python3 src/main.py`

6. After execution completes, generate the summary report:
   `python3 src/report_generator.py`

7. After generating the summary report (file: all_metrics.json), there are other scripts that can generate comparison reports:
```bash
python3 category_performance.py
````
```bash
python3 compare_results.py
````
```bash
python3 consistency_analysis.py
````
```bash
python3 difficulty_comparison.py
````
```bash
python3 error_by_category.py
````
```bash
python3 extract_failures.py
````
The raw JSON responses from the API will be stored in results/raw/, and the computed metrics will be saved to results/metrics/all_metrics.json.

## Dataset Description

The test suite comprises 20 vulnerable code snippets (10 simple and 10 complex) written in Python and JavaScript. Each case is annotated with ground truth vulnerabilities mapped to the OWASP Top 10 (2021) categories.

## Evaluation Metrics

The pipeline calculates precision, recall, and F1-score for each execution, comparing the model's detected vulnerabilities against the annotated ground truth. Error types are classified as correct, partial omission, commission, or mixed.

## Notes

- The default configuration runs each test case 5 times per prompt strategy (simple and structured).
- A delay of 5 seconds is enforced between API requests to respect rate limits.
- The free tier of the Gemini API may be insufficient for the full 200 requests; a billing-enabled project is recommended.

## License

This project was developed by Rômulo Angelo Zanco Neto, a Master's student in Information Security at the University of Coimbra, for academic purposes within the scope of the Software Artifact Analysis course.
Feel free to use and adapt it, provided you give proper attribution.