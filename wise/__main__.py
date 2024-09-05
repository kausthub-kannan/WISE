import argparse
from wise.agents.QAagent import QAagent
from wise.crawler.scrapper import GoogleFormScrapper

def main():
    parser = argparse.ArgumentParser(description="Wise CLI")
    parser.add_argument("--data_dir", type=str, default="data", help="Path to the data directory for context")
    parser.add_argument("--url", type=str, default="", help="URL to be give to the agent")
    args = parser.parse_args()

    scrapper = GoogleFormScrapper()
    agent = QAagent(args.data_dir)

    questions = scrapper.scrape(args.url)

    for question in questions:
        response = agent.chat(question)
        print(response)

if __name__ == "__main__":
    main()