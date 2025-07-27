import os
from flask import Blueprint, jsonify, request
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

user_api = Blueprint("user_api", __name__)

# Configuration
DEPLOYMENT_NAME = "GPT-4o-mini"

client = AzureOpenAI(
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

@user_api.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Read file content (as text)
    file_content = file.read().decode("utf-8")

    prompt = f"sumerize the following meeting transcript with key points, decisions, action items: \n\n {file_content}"

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant specialized in sumarizing meetings notes.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=500
    )
    sumary = response.choices[0].message.content.strip()
    return jsonify({"content": sumary}), 201
