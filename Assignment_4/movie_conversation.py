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
        "content": "Analyze the sentiment of this text: 'IronMan movies are the best movies of all time of the Marvel Cinematic Universe.'",
    },
    {
        "role": "assistant",
        "content": "Sentiment: Positive, the text expresses strong admiration and enthusiasm for IronMan movies.",
    },
    {
        "role": "user",
        "content": "Analyze the sentiment of this text: 'The Green Lantern is a terrible series and I hate it.'",
    },
    {
        "role": "assistant",
        "content": "Sentiment: Negative, the text expresses strong dislike and criticism towards The Green Lantern series.",
    },
    {
        "role": "user",
        "content": "Analyze the sentiment of this text: 'The Flash movie is okay, not the best but not the worst.'",
    },
    {
        "role": "assistant",
        "content": "Sentiment: Neutral, the text describes a balanced and moderate condition without strong emotions.",
    },
]

conversation_message = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant that analyzes the sentiment of movie-related texts. "
            "Your task is to determine whether the sentiment is **positive**, **negative**, or **neutral**, "
            "based on the tone and language. When asked about a specific series, explain your reasoning step-by-step "
            "and conclude with a clear decision on whether to go to the cinema to watch it."
        ),
    }
]

chain_of_thought_examples = [
    {
        "role": "user",
        "content": (
            "How about the Harry Potter series? "
            "Explain your reasoning step by step: should I go to the cinema to watch this movie?"
        ),
    },
    {
        "role": "assistant",
        "content": (
            "**Section 1: Overview**\n"
            "The Harry Potter series is a beloved fantasy franchise known for its magical world, character arcs, and narrative depth.\n\n"
            "**Section 2: Pros**\n"
            "- Strong storytelling and world-building\n"
            "- Iconic characters and performances\n"
            "- Critically acclaimed with high audience scores\n\n"
            "**Section 3: Cons**\n"
            "- Some entries in the series received mixed reviews\n"
            "- Lengthy runtime may not appeal to casual viewers\n\n"
            "**Section 4: Cast & Visuals**\n"
            "Starring Daniel Radcliffe, Emma Watson, and Rupert Grint. Known for impressive visual effects and emotional storytelling.\n\n"
            "**Section 5: Final Decision**\n"
            "Yes, I recommend going to the cinema to watch the Harry Potter series. It's an immersive experience, especially for fans of fantasy and magical adventures.\n\n"
        ),
    },
]

conversation_message.extend(few_shot_examples)
conversation_message.extend(chain_of_thought_examples)
conversation_message.append(
    {
        "role": "user",
        "content": (
            "What about the Avengers series? "
            "Explain your reasoning step by step: should I go to the cinema to watch this movie?"
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
