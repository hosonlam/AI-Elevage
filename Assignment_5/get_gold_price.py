from tenacity import (
    retry,
    wait_random_exponential,
    stop_after_attempt,
    retry_if_exception_type,
)
from openai import RateLimitError, APIError, AzureOpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
import os
import time
import json

load_dotenv()
console = Console()

DEPLOYMENT_NAME = "GPT-4o-mini"

client = AzureOpenAI(
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

functions = [
    {
        "type": "function",
        "function": {
            "name": "get_gold_price",
            "description": "Generate the gold price for a specific year or month.",
            "parameters": {
                "type": "object",
                "properties": {
                    "year": {
                        "type": "integer",
                        "description": "Year for which to fetch the gold price",
                    },
                    "month": {
                        "type": "integer",
                        "description": "Month of the year for which to fetch the gold price (1-12)",
                    },
                },
                "required": ["year"],
            },
        },
    }
]

@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_random_exponential(min=1, max=10),
    stop=stop_after_attempt(5),
    reraise=True,
)
def call_openai_function(messages):
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=messages,
        tools=functions,
        tool_choice="auto",
    )
    return response

@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_random_exponential(min=1, max=10),
    stop=stop_after_attempt(5),
    reraise=True,
)
def get_response_messages(messages):
    system_message = [
        {
            "role": "system",
            "content": "You are a helpful assistant that provides gold prices for a given year or month.",
        },
    ]

    system_message.extend(messages)

    final_response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=system_message,
    )
    return final_response

def batch_process(inputs):
    results = []
    for input_data in inputs:
        try:
            messages = [input_data]  # Each input_data is a single message dict
            res = call_openai_function(messages)

            # Process the model's response
            response_message = res.choices[0].message
            messages.append(response_message)

            if response_message.tool_calls:
                tool_call = response_message.tool_calls[0]
                # Call the function with the arguments provided by the model
                if tool_call.function.name == "get_gold_price":
                    function_args = json.loads(tool_call.function.arguments)
                    year = function_args.get("year")
                    month = function_args.get("month")

                    # Get the price based on the provided year and month
                    if month:
                        tool_response = f"The gold price in {month}/{year} was ***price***$ per ounce."
                    else:
                        tool_response = f"The gold price in {year} was ***price***$ per ounce."
                    
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": "get_gold_price",
                            "content": tool_response,
                        }
                    )
            else:
                print("No tool calls were made by the model.")

            # Append the final response to results
            final_response = get_response_messages(messages)
            results.append(final_response.choices[0].message.content)
            time.sleep(1)
        except Exception as e:
            print(f"Error processing: {e}")
            results.append(None)
    return results


batch_inputs = [
    {"role": "user", "content": "What was the gold price in 2023?"},
    {"role": "user", "content": "What was the gold price in 2022?"},
    {"role": "user", "content": "What was the gold price in 2021, 3rd month?"},
]

if __name__ == "__main__":
    outputs = batch_process(batch_inputs)

    for idx, output in enumerate(outputs):
        if output:
            content = Markdown(output)
            console.print(content, style="bold cyan", new_line_start=True)
        else:
            print("❌ No result due to error or retry failure.")

        print(f"{'=' * 40}\n")
