# Azure OpenAI Batch Processing with Function Calling

This script demonstrates how to efficiently use the Azure OpenAI API to process a batch of inputs. It leverages function calling to structure the output and includes a robust retry mechanism to handle transient API errors.

## How to Run

### 1. Prerequisites

- Python 3.8+
- An Azure OpenAI resource with a deployed `gpt-4` or `gpt-35-turbo` model that supports function calling.
- An environment file to store your API credentials.

### 2. Setup

1.  **Clone the repository or download the script.**

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    _(Note: You will need to create a `requirements.txt` file containing the following packages.)_

    **`requirements.txt`**:

    ```
    openai
    python-dotenv
    tenacity
    rich
    ```

4.  **Create a `.env` file** in the same directory as the script and add your Azure OpenAI credentials:
    ```
    AZURE_OPENAI_ENDPOINT="your_azure_openai_endpoint"
    AZURE_OPENAI_API_KEY="your_azure_openai_api_key"
    AZURE_OPENAI_API_VERSION="2024-02-15-preview"
    AZURE_OPENAI_DEPLOYMENT_NAME="your_deployment_name"
    ```

### 3. Execution

Run the script from your terminal:

```bash
python your_script_name.py
```

The script will process the predefined list of companies, print the structured output to the console in a formatted table, and save the results to `structured_responses.json`.

## Design Choices & Key Features

### 1. Batch Processing (`batch_process` function)

- **Why?**: Instead of sending one request per company, the script processes a list of inputs. This is a common real-world scenario where you need to process many items.
- **How?**: A simple `for` loop iterates through the `inputs` list. For production use, this could be scaled up with asynchronous requests or a job queue.

### 2. Robust Retries with `tenacity`

- **Why?**: Network requests to APIs like OpenAI can occasionally fail due to transient issues (e.g., temporary server overload, network hiccups). A simple script might crash on the first failure. A robust script should retry.
- **How?**: The `@retry` decorator from the `tenacity` library is used on the `call_openai_function`.
  - `wait=wait_random_exponential(min=1, max=60)`: This implements exponential backoff. The script waits for a short, random time before the first retry, and this wait time increases exponentially for subsequent retries, up to a maximum of 60 seconds. This prevents overwhelming the API with rapid-fire retries.
  - `stop=stop_after_attempt(6)`: It will attempt to call the function a maximum of 6 times before giving up.

### 3. Structured Output with Function Calling

- **Why?**: We need reliable, machine-readable JSON output. Asking the model to "please return JSON" can be unreliable. Function calling forces the model to generate a JSON object that conforms to a specific schema.
- **How?**:
  - We define a function schema (`get_company_info`) that describes the desired JSON structure (e.g., `company_name`, `stock_symbol`, `ceo`).
  - We pass this schema to the API in the `tools` parameter and set `tool_choice` to force the model to use it.
  - The script then parses the JSON response from the model's `tool_calls`.

### 4. Code Readability and Maintainability

- **Configuration Management**: API keys and endpoints are loaded from a `.env` file using `python-dotenv`. This is a best practice that separates configuration from code, making it more secure and easier to manage.
- **Clear Output**: The `rich` library is used to print a nicely formatted table to the console, making the results easy to read.

## Challenges & Solutions

1.  **Challenge**: The OpenAI API might return an incomplete or malformed JSON string in the `content` of a message, even when function calling is used.

    - **Solution**: The most reliable way to get the structured data is to ignore the `content` field and directly access the `tool_calls` attribute in the response. The arguments for the tool call are guaranteed to be a valid JSON object.

2.  **Challenge**: Handling various potential API errors (e.g., rate limits, invalid requests, server errors).
    - **Solution**: The `tenacity` library gracefully handles exceptions. If `call_openai_function` raises an exception, the `@retry` decorator catches it and decides whether to try again based on the configured policy. This makes the main loop cleaner as it doesn't need to be cluttered with complex `try...except` blocks for retries.
