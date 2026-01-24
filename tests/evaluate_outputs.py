import os
from azure.ai.evaluation import evaluate, TaskAdherenceEvaluator, RelevanceEvaluator, ResponseCompletenessEvaluator, OpenAIModelConfiguration

# Set your OpenAI API key (ensure this is set in your environment for security)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Model configuration for OpenAI
model_config = OpenAIModelConfiguration(
	type="openai",
	model="gpt-4",
	base_url="https://api.openai.com/v1",
	api_key=OPENAI_API_KEY
)

data_path = "tests/test_payloads.jsonl"
output_path = "evaluation_results.jsonl"

task_adherence = TaskAdherenceEvaluator(model_config=model_config)
relevance = RelevanceEvaluator(model_config=model_config)
completeness = ResponseCompletenessEvaluator(model_config=model_config)

result = evaluate(
	data=data_path,
	evaluators={
		"task_adherence": task_adherence,
		"relevance": relevance,
		"completeness": completeness
	},
	evaluator_config={
		"task_adherence": {
			"column_mapping": {
				"query": "${data.clientName}",
				"response": "${data.response}"
			}
		},
		"relevance": {
			"column_mapping": {
				"query": "${data.clientName}",
				"response": "${data.response}"
			}
		},
		"completeness": {
			"column_mapping": {
				"response": "${data.response}",
				"ground_truth": "${data.ground_truth}"
			}
		}
	},
	output_path=output_path
)

print("Evaluation complete. Results saved to", output_path)
