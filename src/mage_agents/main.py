#!/usr/bin/env python
import sys
import warnings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
import uvicorn
from mem0 import Memory
from mage_agents.routes.api import AgentsApi
from mage_agents.crew import MageAgents
load_dotenv()


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Ensure the path exists
os.makedirs("./data", exist_ok=True)

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    try:
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Chatbot: Goodbye! It was nice talking to you.")
                break

            inputs = {
                "user_message": f"{user_input}",
            }

            response = MageAgents().crew().kickoff(inputs=inputs)

            print(f"Assistant: {response}")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


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