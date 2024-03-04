# Tonic Validate for Main Merges

Github action to run Tonic Validate evaulation on main branch merges.  This action uses the open source [Tonic Validate library](https://github.com/TonicAI/tonic_validate) to help track LLM performance over time.

![image](https://github.com/TonicAI/tonic_validate_merge_action/assets/78937627/4c5f6235-7b9c-4e25-8371-7e36f3c92cd5)

# Setup

To kick off a Tonic Validate evaluation after merging to your main branch, add the sample workflow to .github/workflows.

```yml
name: Tonic Validate
on:
  push:
    branches:
      - 'master'
      - 'main'

jobs:
  tonic-validate:
    runs-on: ubuntu-latest
    name: Tonic Validate
    env:
      TONIC_VALIDATE_API_KEY: ${{ secrets.TONIC_VALIDATE_API_KEY }}
      OPENAI_API_KEY:  ${{ secrets.OPENAI_API_KEY }}
      AZURE_OPENAI_KEY: ${{ secrets.AZURE_OPENAI_KEY}}
      AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT}}
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v4      
      - name: Validate
        uses: TonicAI/tonic_validate_pr_action@v0.1.0
        with:
          tonic_validate_project_id: <Tonic Validate Project Id>
          llm_response_path: <Path to Q&A for Evaluation>

```

This workflow requires that set a Tonic Validate API key (found in the Tonic Validate UI) and that you do one of the following:

- Set an OpenAI API key
- Set both an Azure API key and an Azure Endpoint URL

You also must provide a value for `tonic_validate_project_id`, which is the id for your Tonic Validate project, and `llm_response_path`, which is the path (relative to the root of your repository) to a JSON file that contains the questions and optional context and reference answers for Tonic Validate to evaluate. 

Here is a sample set of questions and answers:

```json
[
    {"llm_answer":"Paris", "benchmark_item":{"question":"What is the capital of Paris", "answer":"Paris"}},
    {"llm_answer":"Berlin", "benchmark_item":{"question":"What is the capital of Germany", "answer":"Berlin"}},
    {"llm_answer":"Sam Altman is the CEO of OpenAI", "llm_context_list": ["Sam Altman has been the CEO of OpenAI since 2019."], "benchmark_item":{"question":"Who is the CEO of OpenAI?", "answer":"Sam Altman"}},
]
```
