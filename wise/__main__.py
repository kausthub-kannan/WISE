import argparse
import os

from wise.agents.QAagent import QAagent
from wise.crawler.scrapper import GoogleFormScrapper
import logging
import json
import getpass

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    parser = argparse.ArgumentParser(description="Wise CLI")
    parser.add_argument("prompt", type=str, help="User data (prompt)")
    parser.add_argument("url", type=str, default="", help="URL to be give to the agent")
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data",
        help="Path to the data directory for context",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default="output.json",
        help="Path to the output file (JSON)",
    )

    if not os.environ.get("GROQ_API_KEY"):
        os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your GROQ API Key: ")

    args = parser.parse_args()

    scrapper = GoogleFormScrapper()
    agent = QAagent(args.data_dir)

    raw_html_data = scrapper.scrape(args.url)
    logger.info(f"Number of Questions scrapped: {len(raw_html_data)}")

    result = []

    for i, raw_html_question in enumerate(raw_html_data):
        response = agent.chat(raw_html_question, args.prompt)
        result.append(response)
        logger.info(f"Processed Question {i}")

    with open(args.output_path, "w") as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    main()
