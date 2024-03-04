import json
import os
import sys
import warnings
from tabulate import tabulate
from typing import List
from tonic_validate import BenchmarkItem, LLMResponse, ValidateApi, ValidateScorer

path_to_responses = os.environ.get('VALIDATE_RESPONSES_PATH', None)
validate_api_key = os.environ.get('TONIC_VALIDATE_SERVER_API_KEY', None)
validate_project_id = os.environ.get('TONIC_VALIDATE_SERVER_PROJECT_ID', None)

repo_url = os.environ.get('GITHUB_REPO_URL', None)
commit_sha = os.environ.get('GITHUB_COMMIT_ID', None)

if validate_api_key is None:
    exit('Error: You must specify TONIC_VALIDATE_SERVER_API_KEY, the API key for the Tonic Validate server')

if validate_project_id is None:
    exit('Error: You must specify TONIC_VALIDATE_SERVER_PROJECT_ID, the project ID for the Tonic Validate server')

if path_to_responses is None:
    exit('Error: You must specify VALIDATE_RESPONSES_PATH, the path to your LLM question and responses')

if not os.path.exists(path_to_responses):
    exit('ERROR: The VALIDATE_RESPONSES_PATH provided ("{}") does not exist'.format(path_to_responses))

openai_key = os.environ.get("OPENAI_API_KEY")
azure_key = os.environ.get("AZURE_OPENAI_KEY")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")

if openai_key is None or openai_key=='':
    if (azure_key is None or azure_key=='') and (azure_endpoint is None or azure_endpoint==''):
        exit('ERROR: You must set either an OpenAI key or an Azure key and Azure endpoint')


with open(path_to_responses) as json_data:
    try:
        responses = json.load(json_data)
        json_data.close()
    except ValueError:
        exit('Error: Failed to parse {}, please ensure it is valid JSON'.format(path_to_responses))

llm_responses: List[LLMResponse] = []
for response in responses:
    llm_context_list = []
    if 'llm_context_list' in response:
        llm_context_list = response['llm_context_list']

    l = LLMResponse(response['llm_answer'], llm_context_list, benchmark_item=BenchmarkItem(response['benchmark_item']['question'], response['benchmark_item']['answer']))
    llm_responses.append(l)

scorer = ValidateScorer()
run = scorer.score_responses(llm_responses)

run_metadata = {}

if repo_url is not None and commit_sha is not None:
    run_metadata = {
        'commit_url': f"{repo_url}/commit/{commit_sha}"
    }
else:
    warnings.warn('The repository URL and the commit SHA must be passed into the runner for the run to be associated with a commit.  You can set this up in the workflow file by passing in the deafult github variables, github.sha and github.repository_url')

validate_api = ValidateApi(validate_api_key)
validate_api.upload_run(validate_project_id, run, run_metadata)