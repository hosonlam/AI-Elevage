from services.openAI_services import create_client
from rich.console import Console
from rich.markdown import Markdown

# Configuration
DEPLOYMENT_NAME = "GPT-4o-mini"

console = Console()

# Few-shot examples for sentiment analysis
few_shot_examples = [
    {
        "role": "user",
        "content": "Analyze the sentiment of this text: 'Today, the sky is clear and the sun is shining.'",
    },
    {
        "role": "assistant",
        "content": "Sentiment: Positive, the text conveys a cheerful and optimistic mood.",
    },
    {
        "role": "user",
        "content": "Analyze the sentiment of this text: 'The next day, It will rain heavily'",
    },
    {
        "role": "assistant",
        "content": "Sentiment: Negative, the text conveys a gloomy and pessimistic mood.",
    },
    {
        "role": "user",
        "content": "Analyze the sentiment of this text: 'The weather is neither too hot nor too cold.'",
    },
    {
        "role": "assistant",
        "content": "Sentiment: Neutral, the text describes a balanced and moderate condition without strong emotions.",
    },
]

conversation_message = [
    {
        "role": "system",
        "content": "You are a helpful assistant that analyzes the sentiment of text. Your task is to determine whether the sentiment is positive, negative, or neutral based on the content provided.",
    }
]

chain_of_thought_examples = [
    {
        "role": "user",
        "content": (
            "What is the weather next week?"
            "Should I bring an umbrella or wear a raincoat? How can I prepare for the weather?"
            "Exlain your reasoning step by step."
        ),
    },
]

conversation_message.extend(few_shot_examples)
conversation_message.extend(chain_of_thought_examples)

client = create_client()

response = client.chat.completions.create(
    messages=conversation_message,
    model=DEPLOYMENT_NAME,
    temperature=0.7,
)

assistant_message = response.choices[0].message.content

content = Markdown(assistant_message)

console.print(content, style="bold green", new_line_start=True)
