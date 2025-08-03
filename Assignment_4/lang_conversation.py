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
        "content": "Analyze the language of this text: 'Hello, My name is John and I love programming.'",
    },
    {
        "role": "assistant",
        "content": "Language: English, the text is written in a friendly and personal tone, introducing the speaker and expressing a passion for programming.",
    },
    {
        "role": "user",
        "content": "Analyze the language of this text: 'Bonjour, je m'appelle Marie et j'adore la cuisine.'",
    },
    {
        "role": "assistant",
        "content": "Language: French, the text is written in a friendly and personal tone, introducing the speaker and expressing a passion for cooking.",
    },
    {
        "role": "user",
        "content": "Analyze the language of this text: 'Hola, me llamo Carlos y me encanta el fútbol.'",
    },
    {
        "role": "assistant",
        "content": "Language: Spanish, the text is written in a friendly and personal tone, introducing the speaker and expressing a passion for football.",
    },
]

conversation_message = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant that analyzes the sentiment of language in texts"
            "Your task is to determine whether the language is **English**, **French**, or other language, "
            "based on the tone and language. When asked about a specific series, explain your reasoning step-by-step "
        ),
    }
]

chain_of_thought_examples = [
    {
        "role": "user",
        "content": (
            "Xin chào, tôi là một người yêu thích AI. Tên tôi là San San.\n"
            "Explain your reasoning step by step: what language is this text written in? "
            "Return the answer in a clean markdown format with clearly labeled sections."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "**🧠 Step-by-Step Language Analysis**\n\n"
            "**🔤 Step 1: Detect Common Phrases**\n"
            '- The phrase "Xin chào" is a common greeting in Vietnamese meaning "Hello".\n'
            '- The phrase "Tên tôi là" means "My name is" in Vietnamese.\n\n'
            "**📝 Step 2: Character Set and Syntax**\n"
            '- The sentence uses Latin script with diacritics (e.g., "à", "ô"), which is characteristic of Vietnamese.\n'
            "- Word order and grammar patterns also match Vietnamese structure.\n\n"
            "**🧾 Step 3: Translation**\n"
            "- **Original**: Xin chào, tôi là một người yêu thích AI. Tên tôi là San San.\n"
            "- **English**: Hello, I am someone who loves AI. My name is San San.\n\n"
            "**✅ Conclusion**\n"
            "The language of the text is **Vietnamese**."
        ),
    },
]


conversation_message.extend(few_shot_examples)
conversation_message.extend(chain_of_thought_examples)
conversation_message.append(
    {
        "role": "user",
        "content": (
            "Chinese: 大家好，我叫 San San，是一位对语言和文化非常感兴趣的人。今天有机会在这里认识大家，我感到非常开心和荣幸。希望以后我们能成为好朋友，一起学习、一起进步。谢谢大家！\n"
            "Pinyin: Dàjiā hǎo, wǒ jiào San San, shì yī wèi duì yǔyán hé wénhuà fēicháng gǎn xìngqù de rén. Jīntiān yǒu jīhuì zài zhèlǐ rènshi dàjiā, wǒ gǎndào fēicháng kāixīn hé róngxìng. Xīwàng yǐhòu wǒmen néng chéngwéi hǎo péngyǒu, yīqǐ xuéxí, yīqǐ jìnbù. Xièxie dàjiā!\n"
            "Explain your reasoning step by step: Can you translate this for me?"
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
