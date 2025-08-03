from services.openAI_services import create_client
from rich.console import Console
from rich.markdown import Markdown

# Configuration
DEPLOYMENT_NAME = "GPT-4o-mini"

console = Console()

chain_of_thought_examples = [
    {
        "role": "user",
        "content": "I have five apples and two oranges. I give two apples to my friend. Then I buy three more oranges. After that I give three oranges to my mom. How many fruits do I have now?",
    },
    {
        "role": "assistant",
        "content": """Let's break it down step by step:
            1. Start with 5 apples and 2 oranges.
            2. After giving away 2 apples, I have 5 - 2 = 3 apples left.
            3. I then buy 3 more oranges, so I have 2 + 3 = 5 oranges now.
            4. After giving away 3 oranges, I have 5 - 3 = 2 oranges left.
            5. Now, I have 3 apples and 2 oranges.
            6. Therefore, the total number of fruits I have now is 3 (apples) + 2 (oranges) = 5 fruits in total.
            So, I have a total of 5 fruits now.""",
    },
]

conversation_message = [
    {
        "role": "system",
        "content": "You are a helpful assistant that answers questions by breaking them down into steps.",
    }
]

conversation_message.extend(chain_of_thought_examples)
conversation_message.append(
    {"role": "user", "content": "I have 10 bananas and 5 apples. I eat 3 bananas and buy 4 more apples. How many fruits do I have now?"}
)

client = create_client()

response = client.chat.completions.create(
    messages=conversation_message,
    model=DEPLOYMENT_NAME,
    temperature=0.7,
)

assistant_message = response.choices[0].message.content

content = Markdown(assistant_message)

console.print(content, style="bold green", new_line_start=True)
