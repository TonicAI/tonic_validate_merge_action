import json
import os
from typing import List
from tonic_validate import BenchmarkItem, LLMResponse, ValidateApi, ValidateScorer

<<<<<<< Updated upstream
def get_env_variable(var_name: str, error_message: str) -> str:
    """Retrieve an environment variable or exit with an error message."""
    value = os.environ.get(var_name)
    if not value:
        exit(error_message)
    return value

def load_responses(path: str) -> List[LLMResponse]:
    """Load LLM responses from a JSON file."""
    with open(path, 'r') as json_data:
        try:
            responses = json.load(json_data)
        except ValueError as e:
            exit(f'Error: Failed to parse {path}, please ensure it is valid JSON. Error: {e}')
    return [
        LLMResponse(
            response['llm_answer'],
            response.get('llm_context_list', []),
            benchmark_item=BenchmarkItem(response['benchmark_item']['question'], response['benchmark_item']['answer'])
        ) for response in responses
    ]

validate_api_key = get_env_variable('TONIC_VALIDATE_SERVER_API_KEY', 'Error: TONIC_VALIDATE_SERVER_API_KEY is required.')
validate_project_id = get_env_variable('TONIC_VALIDATE_SERVER_PROJECT_ID', 'Error: TONIC_VALIDATE_SERVER_PROJECT_ID is required.')
path_to_responses = get_env_variable('VALIDATE_RESPONSES_PATH', 'Error: VALIDATE_RESPONSES_PATH is required.')

if not os.path.exists(path_to_responses):
    exit(f'ERROR: The path {path_to_responses} does not exist.')

llm_responses = load_responses(path_to_responses)
=======
path_to_responses = os.environ.get('VALIDATE_RESPONSES_PATH', None)
if path_to_responses is None:
    exit('Error: You must specify VALIDATE_RESPONSES_PATH, the path to your LLM question and responses')
if not os.path.exists(path_to_responses):
    exit('ERROR: The VALIDATE_RESPONSES_PATH provided ("{}") does not exist'.format(path_to_responses))

validate_api_key = os.environ.get('TONIC_VALIDATE_SERVER_API_KEY', None)
if validate_api_key is None:
    exit('Error: You must specify TONIC_VALIDATE_SERVER_API_KEY, the API key for the Tonic Validate server')

validate_project_id = os.environ.get('TONIC_VALIDATE_SERVER_PROJECT_ID', None)
if validate_project_id is None:
    exit('Error: You must specify TONIC_VALIDATE_SERVER_PROJECT_ID, the project ID for the Tonic Validate server')

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
>>>>>>> Stashed changes

scorer = ValidateScorer()
run = scorer.score_responses(llm_responses)

validate_api = ValidateApi(validate_api_key)

# Use default github action environment variables
github_server = os.environ.get('GITHUB_SERVER_URL', None)
github_repository = os.environ.get('GITHUB_REPOSITORY', None)
github_sha = os.environ.get('GITHUB_SHA', None)

run_metadata = {
    'commit_url': f"{github_server}/{github_repository}/commit/{github_sha}"
}

validate_api.upload_run(validate_project_id, run, run_metadata)