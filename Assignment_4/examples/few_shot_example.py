from services.openAI_services import create_client
from rich.console import Console
from rich.markdown import Markdown

# Configuration
DEPLOYMENT_NAME = "GPT-4o-mini"

console = Console()

few_shot_examples = [
    {
        "role": "user",
        "content": "IronMan is known for his intelligence and his suit of armor.",
    },
    {"role": "assistant", "content": "IronMan is a super hero"},
    {
        "role": "user",
        "content": "SpiderMan is known for his agility and spider-like abilities.",
    },
    {"role": "assistant", "content": "SpiderMan is a super hero"},
    {
        "role": "user",
        "content": "Thanor is known for his strength and his villainous plans.",
    },
    {"role": "assistant", "content": "Thanor is a super villain"},
]

conversation_message = [
    {
        "role": "system",
        "content": "You are a helpful assistant that classifies characters as either super hero or super villain based on their characteristics.",
    }
]

conversation_message.extend(few_shot_examples)
conversation_message.append(
    {"role": "user", "content": "Loki is known for his trickery and magic."}
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
