import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

log_entries = [
    "Driver reported heavy traffic on highway due to construction",
    "Package not accepted, customer unavailable at given time",
    "Vehicle engine failed during route, replacement dispatched",
    "Unexpected rainstorm delayed loading at warehouse",
    "Sorting label missing, required manual barcode scan",
    "Driver took a wrong turn and had to reroute",
    "No issue reported, arrived on time",
    "Address was incorrect, customer unreachable",
    "System glitch during check-in at loading dock",
    "Road accident caused a long halt near delivery point",
    "Driver encountered detour due to road closure, delayed arrival",
    "Customer requested rescheduled delivery time, postponed to tomorrow",
    "Vehicle's tire burst on route, repair team sent for assistance",
    "Loading dock delayed due to faulty equipment, processing took longer",
    "Delivery confirmed but customer unable to accept due to missing ID",
    "Truck broke down on highway, additional vehicle dispatched for delivery",
    "Security check delayed due to equipment malfunction at warehouse",
    "Delivery was delayed by 45 minutes due to heavy snowfall",
    "Customer requested expedited delivery, rerouted for quicker arrival",
    "No packages available for delivery at the given location, returned to warehouse",
]

def initial_classify(text):
    keywords = {
        "traffic": "Traffic",
        "road accident": "Traffic",
        "construction": "Traffic",
        "detour": "Traffic",
        "reroute": "Human Error",
        "wrong turn": "Human Error",
        "customer": "Customer Issue",
        "unavailable": "Customer Issue",
        "engine": "Vehicle Issue",
        "vehicle": "Vehicle Issue",
        "breakdown": "Vehicle Issue",
        "tire burst": "Vehicle Issue",
        "rain": "Weather",
        "storm": "Weather",
        "snow": "Weather",
        "fog": "Weather",
        "sorting": "Sorting/Labeling Error",
        "label": "Sorting/Labeling Error",
        "barcode": "Sorting/Labeling Error",
        "equipment": "Warehouse/Loading Issue",
        "loading": "Warehouse/Loading Issue",
        "check-in": "Warehouse/Loading Issue",
        "system": "Technical Failure",
        "glitch": "Technical Failure",
        "error": "Technical Failure",
    }

    for keyword, value in keywords.items():
        if keyword in text.lower():
            return value
    return "Other"

DEPLOYMENT_NAME = "GPT-4o-mini"

client = AzureOpenAI(
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

def refine_classification(text, initial_label):
    prompt = f"""
        You are a logistics assistant. A log entry has been auto-categorized as
        "{initial_label}". Please confirm or correct it by choosing one of the
        following categories:
        - Traffic
        - Customer Issue
        - Vehicle Issue
        - Weather
        - Sorting/Labeling Error
        - Human Error
        - Technical System Failure
        - Other
        Log Entry:
        \"\"\"{text}\"\"\"
        Return only the most appropriate category from the list.
    """
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content.strip()

def classify_log(text):
    initial = initial_classify(text)
    final = refine_classification(text, initial)
    return {"log": text, "initial": initial, "final": final}

if __name__ == "__main__":
    results = []
    for entry in log_entries:
        result = classify_log(entry)
        results.append([result['log'], result['final']])
    
    # Print the table using tabulate
    headers = ["Log Entry", "Initial Classification", "Final Classification"]
    table = tabulate(results, headers, tablefmt="grid", numalign="left", stralign="left")
    
    # Display the table
    print(table)
