import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
DEPLOYMENT_NAME = "GPT-4o-mini"

# Sample tasks
TASK_DESCRIPTIONS = [
    "Install the battery module in the rear compartment, connect to the high-voltage harness, and verify torque on fasteners.",
    "Calibrate the ADAS (Advanced Driver Assistance Systems) radar sensors on the front bumper using factory alignment targets.",
    "Apply anti-corrosion sealant to all exposed welds on the door panels before painting.",
    "Perform leak test on coolant system after radiator installation. Record pressure readings and verify against specifications.",
    "Program the infotainment ECU with the latest software package and validate connectivity with dashboard display.",
]


def create_client():
    """Create and return Azure OpenAI client."""
    return AzureOpenAI(
        api_version="2023-05-15",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )


def generate_instruction(client, task):
    """Generate work instructions for a given task."""
    prompt = f"""You are an expert automotive manufacturing supervisor. Generate step-by-step 
                work instructions for the following new model task. Include safety 
                precautions, required tools (if any), and acceptance checks. Write in clear, 
                numbered steps suitable for production workers.

Task:
\"\"\"{task}\"\"\"

Work Instructions:"""
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating instructions: {e}"


def main():
    """Main function to generate instructions for all tasks."""
    client = create_client()

    for task in TASK_DESCRIPTIONS:
        instructions = generate_instruction(client, task)
        print(f"\nTask: {task}")
        print(f"Work Instructions:\n{instructions}\n")
        print("-" * 80)


if __name__ == "__main__":
    main()
