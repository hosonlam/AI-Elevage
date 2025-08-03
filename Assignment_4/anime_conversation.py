from services.openAI_services import create_client
from rich.console import Console
from rich.markdown import Markdown

# Configuration
DEPLOYMENT_NAME = "GPT-4o-mini"

console = Console()

# Few-shot examples for category and title analysis
few_shot_examples = [
    {
        "role": "user",
        "content": "Analyze the category and title of this text:'A ninja anime with epic battles and a deep storyline about friendship and perseverance.'",
    },
    {
        "role": "assistant",
        "content": "Category: Action, Adventure, Title: Naruto.",
    },
    {
        "role": "user",
        "content": "Analyze the category and title of this text: 'a group of friends who travel through a fantasy world, facing challenges and growing together.'",
    },
    {
        "role": "assistant",
        "content": "Category: Fantasy, Adventure, Title: Sword Art Online.",
    },
    {
        "role": "user",
        "content": "Analyze the category and title of this text: 'The group pirate anime with a charismatic captain and a quest for the ultimate treasure.'",
    },
    {
        "role": "assistant",
        "content": "Category: Action, Adventure, Title: One Piece.",
    },
]

conversation_message = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant that analyzes anime titles and categories. "
            "For each anime description provided, respond in a clear, step-by-step format. "
            "Your final answer should be well-structured using markdown with bold section titles. "
            "Include:\n\n"
            "- **Title**\n"
            "- **Category** (comma-separated)\n"
            "- **Summary**\n"
            "- **Main Characters** (if identifiable)"
        ),
    }
]

chain_of_thought_examples = [
    {
        "role": "user",
        "content": (
            "I saw the anime on the internet. It was about a group of people flying with special equipment "
            "and fighting giant humanoid creatures. Find and analyze the category and title of this anime step by step. "
            "Return the answer in a clear markdown format with bold section headers."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "**Step 1: Analyze the plot description**\n"
            "The anime involves people flying with special equipment and fighting giant humanoid creatures. This is a distinctive plot element.\n\n"
            "**Step 2: Identify the anime**\n"
            "This description matches *Attack on Titan*.\n\n"
            "**Step 3: Provide structured output**\n\n"
            "**Title**: Attack on Titan\n\n"
            "**Category**: Action, Adventure, Fantasy\n\n"
            "**Summary**: The anime is set in a world where humanity resides within enormous walled cities to protect themselves from Titans — gigantic humanoid creatures. A military group called the Survey Corps uses special maneuvering gear to combat the Titans and uncover the truth behind their existence.\n\n"
            "**Main Characters**:\n"
            "- Eren Yeager\n"
            "- Mikasa Ackerman\n"
            "- Armin Arlert\n"
        ),
    },
]


conversation_message.extend(few_shot_examples)
conversation_message.extend(chain_of_thought_examples)
conversation_message.append(
    {
        "role": "user",
        "content": (
            "I want to know about an anime I saw on the internet, it was about the man who in form of a six years old child, who is a genius detective and solves mysteries with his friends."
            "Find and analyze the category and title of this anime step by step"
        ),
    }
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
