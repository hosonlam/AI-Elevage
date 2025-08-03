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
import math

load_dotenv()
console = Console()

DEPLOYMENT_NAME = "GPT-4o-mini"

client = AzureOpenAI(
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)


# Function to calculate the triangle type and area
def calculate_triangle_properties(sides):
    a, b, c = sides

    # Check if it's a right triangle using Pythagoras theorem
    if a**2 + b**2 == c**2 or b**2 + c**2 == a**2 or c**2 + a**2 == b**2:
        triangle_type = "Right Triangle"
        # Calculate area of right triangle: (1/2) * base * height
        area = 0.5 * a * b  # Assuming 'a' and 'b' as base and height
    elif a == b == c:
        triangle_type = "Equilateral Triangle"
        # Equilateral triangle area formula
        area = (math.sqrt(3) / 4) * (a**2)
    elif a == b or b == c or a == c:
        triangle_type = "Isosceles Triangle"
        # Calculate area using Heron's formula
        s = (a + b + c) / 2
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    else:
        triangle_type = "Scalene Triangle"
        # Calculate area using Heron's formula
        s = (a + b + c) / 2
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))

    return triangle_type, area


# Function to print triangle shape using stars
def print_triangle(height):
    shape = ""
    for i in range(1, height + 1):
        shape += "*" * i + "\n"
    return shape


functions = [
    {
        "type": "function",
        "function": {
            "name": "get_triangle_properties",
            "description": "Calculate the type and area of a triangle based on its sides, and print its shape.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sides": {
                        "type": "array",
                        "items": {
                            "type": "integer",
                        },
                        "description": "The three sides of the triangle.",
                    },
                },
                "required": ["sides"],
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
            "content": "You are a helpful assistant that calculates the triangle type, area, and prints its shape based on the sides.",
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
                if tool_call.function.name == "get_triangle_properties":
                    function_args = json.loads(tool_call.function.arguments)
                    sides = function_args.get("sides")

                    # Calculate triangle properties (type and area)
                    triangle_type, area = calculate_triangle_properties(sides)

                    # Print the triangle shape
                    triangle_shape = print_triangle(
                        sides[1]
                    )  # Using second side as the height for simplicity

                    tool_response = f"The triangle with sides {sides} is a {triangle_type}. The area is {area:.2f} square units.\n\nTriangle Shape:\n{triangle_shape}"

                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": "get_triangle_properties",
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


# Batch input for different triangle types
batch_inputs = [
    {
        "role": "user",
        "content": "What is the type and area of the right triangle with sides [3, 4, 5]?",
    },
    {
        "role": "user",
        "content": "What is the type and area of the equilateral triangle with sides [5, 5, 5]?",
    },
    {
        "role": "user",
        "content": "What is the type and area of the scalene triangle with sides [7, 8, 9]?",
    },
    {
        "role": "user",
        "content": "What is the type and area of the isosceles triangle with sides [5, 5, 8]?",
    },
]

if __name__ == "__main__":
    outputs = batch_process(batch_inputs)

    for idx, output in enumerate(outputs):
        if output:
            content = Markdown(output)
            console.print(content, style="bold cyan", new_line_start=True)
        else:
            print("❌ No result due to error or retry failure.")

        print(f"{'=' * 100}\n")
