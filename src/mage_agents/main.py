#!/usr/bin/env python
import os
from dotenv import load_dotenv
load_dotenv()

import sys
import warnings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from mem0 import Memory
from mage_agents.routes.api import AgentsApi
from mage_agents.crew import MageAgents
import json
import hashlib


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Ensure the path exists
os.makedirs("./data", exist_ok=True)

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

mem0_custom_prompt = """
Please only extract entities containing customer support information, order details, and user information. 
Here are some few shot examples:

Input: Hi.
Output: {{"facts" : [Hi]}}

Input: The weather is nice today.
Output: {{"facts" : [weather is nice today]}}

Input: My order #12345 hasn't arrived yet.
Output: {{"facts" : ["Order #12345 not received"]}}

Input: I'm John Doe, and I'd like to return the shoes I bought last week.
Output: {{"facts" : ["Customer name: John Doe", "Wants to return shoes", "Purchase made last week"]}}

Input: I ordered a red shirt, size medium, but received a blue one instead.
Output: {{"facts" : ["Ordered red shirt, size medium", "Received blue shirt instead"]}}

Return the facts and customer information in a json format as shown above.
"""

mem0_knowledge_prompt = """
Please extract relevant information from technical documentation and user instructions.  

Here are some few-shot examples:  

Input: "category": "[Category of the content]", "summary": "[Summary of the extracted information]", "url": "[URL of reference to the extracted information]", "content": "[Full extracted content]"
Output: {{"category": [Category of the content],"summary": [Summary of the extracted information],"content": [Full extracted content],"url": [URL of reference to the extracted information]}}

Input: "category": "Adminstration", "summary": "Adobe Commerce support tools include Data Collector for system information gathering and Backup for creating code and database copies.","url": "https://experienceleague.adobe.com/en/docs/commerce-admin/systems/tools/support", "content": "Adobe Commerce provides support tools to identify system issues. The Data Collector gathers system information to assist in troubleshooting. The backup feature allows creating copies of the code and database, which can be exported as CSV or XML."
Output: {{"category": "Support","summary": "Adobe Commerce support tools include Data Collector for system information gathering and Backup for creating code and database copies.","content": "Adobe Commerce provides support tools to identify system issues. The Data Collector gathers system information to assist in troubleshooting. The backup feature allows creating copies of the code and database, which can be exported as CSV or XML.","url": "https://experienceleague.adobe.com/en/docs/commerce-admin/systems/tools/support"}}

Return the extracted information in the same format shown above.
"""

config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "chatbot_memory",
            "path": "./chroma_db",
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.2:latest",
            "temperature": 0.1,
            "max_tokens": 2000,
            "ollama_base_url": "http://localhost:11434",  # Ensure this URL is correct
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text:latest",
            "ollama_base_url": "http://localhost:11434?num_ctx=4048",
        },
    },
    "version": "v1.1",
    "custom_prompt": mem0_custom_prompt,
}

memory = Memory.from_config(config)

def run():
    """
    Run the crew.
    """
    add_knowledge()
    try:
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Chatbot: Goodbye! It was nice talking to you.")
                break

            # Add user input to memory
            memory.add([{"role": "user", "content": user_input }], user_id="gabriel")

            # Retrieve relevant information from vector store
            relevant_info = memory.get_all(user_id="gabriel", limit=10)
            context = "\n".join(relevant_info)

            print(relevant_info, context, user_input)

            inputs = {
                "user_message": f"{user_input}",
                "context": f"{context}",
            }

            response = MageAgents().crew().kickoff(inputs=inputs)
            
            # Add chatbot response to memory
            memory.add([{"role": "assistant", "content": response }], user_id="gabriel")
            print(f"Assistant: {response}")
            
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
def add_knowledge():
    """
    Add Knowledge information
    """
    try:
        print(memory.get_all(user_id="knowledge", limit=200))
        json_file = "knowledge/adobe_commerce_knowledge_embled.json"
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"File {json_file} not found.")
    
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        for url, content in data.items():
            summary = content.get("summary", "")
            category = content.get("category", "")
            embeddings = content.get("embeddings", [])
            full_content = content.get("content", "")
            unique_id = hashlib.sha256(url.encode('utf-8')).hexdigest()[0:35]


            print(f"Inserindo novo dado: {url}")
            memory_item = memory.add(
                [{"role" : "assistant", "category": json.dumps(category), "summary": json.dumps(summary), "url": json.dumps(url), "content": json.dumps(full_content)}],
                user_id="knowledge",
                metadata={"url": json.dumps(url), "category": category},
                prompt=mem0_knowledge_prompt
            )
            print(memory_item)
    except Exception as e:
        print(f"❌ Error in JSON: {e}")
        print({"role" : "system","category": category, "summary": summary, "url": json.dumps(url), "content": json.dumps(full_content)})


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        MageAgents().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MageAgents().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        MageAgents().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
    
def api():
    """
    Start API server
    """
    try:
        app = FastAPI()

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allows all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allows all methods
            allow_headers=["*"],  # Allows all headers
        )

        app.mount("/static", StaticFiles(directory="static"), name="static")
        routes = AgentsApi()
        app.include_router(routes.router)
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('APP_PORT')))

    except Exception as e:
        raise Exception(f"An error occurred while creating server: {e}")
if __name__ == "__main__":
    api()