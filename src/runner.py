import json
import os
from typing import List
from tonic_validate import BenchmarkItem, LLMResponse, ValidateApi, ValidateScorer

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

# Load environment variables
validate_api_key = get_env_variable('TONIC_VALIDATE_SERVER_API_KEY', 'Error: TONIC_VALIDATE_SERVER_API_KEY is required.')
validate_project_id = get_env_variable('TONIC_VALIDATE_SERVER_PROJECT_ID', 'Error: TONIC_VALIDATE_SERVER_PROJECT_ID is required.')
path_to_responses = get_env_variable('VALIDATE_RESPONSES_PATH', 'Error: VALIDATE_RESPONSES_PATH is required.')

if not os.path.exists(path_to_responses):
    exit(f'ERROR: The path {path_to_responses} does not exist.')

llm_responses = load_responses(path_to_responses)

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