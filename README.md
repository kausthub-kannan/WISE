# WISE
WISE (Web Intelligence and Scripting Engine) is collection of AI agents which is used to automate different tasks.
WISE uses LLMs for dynamic reasoning of the questions. Using RAG for context and RAW HTML scrapped by the crawler, LLMs
valuable information. For dynamic tasks such as filling forms, this information retrieved is to be used.

## Workflow
![wise-arch](/assets/wise.png)

1. To perform a task such as filling the form, WISE firsts scraps data and raw HTML using web driver. 
2. ALong with webdriver data, the Agents accept data from documents or from vector storage enabling RAG.
3. WISE empowers multiple agents, each with a specific task. To analyse and reason final data and raw HTML fine-tuned LLMs are used.
4. Sometimes, data can be hidden in the form of images, hence Vision Agent is used analyse them. These images are obtained from screenshots. The obtained text from Vision model becomes context to QA Agent which reduces hallucinations.
5. QAagents is responsible to provide answer and the XPath to automate the task. 
6. Reply JSON is an optional support which is to be added to support the way the execution has to be automated. This provides some human-like touch to the automation.
7. User's data is analysed to obtain the answers. The RAG data acts as context and external references if needed are used to obtain further detailed answers.

## TODO
- [x] Create a crawler to scrap the questions
- [x] Create a LLM model to answer the questions
- [x] Create a RAG model to get the context
- [ ] Create a Multi-model to get the answers from Screenshots
- [ ] Obtain XPath of UI elements to fill the form using Web driver
- [ ] When given the `Replay.json`, reference it to understand the workflow such as the order in which the form is filled
- [ ] Link external references if required
- [ ] Use OSS LLMs with LlamaCPP support

## Installation
Install the tar file using the following command:
```bash
wget https://github.com/kausthub-kannan/WISE/releases/download/0.1.0/wise-0.1.0.tar.gz
```
or install it from this [link](https://github.com/kausthub-kannan/WISE/releases/download/0.1.0/wise-0.1.0.tar.gz)

Now install the package using pip
```bash
pip install wise-0.1.0.tar.gz
```

## Usage
WISE currently has CLI support only. To use the CLI, run the following command:

```bash
wise --help
```
Args:
- `prompt`: The prompt to be given to the LLM model
- `--data-dir`: The directory where the data is stored to be given for RAG
- `--url`: The URL of the website to be scrapped