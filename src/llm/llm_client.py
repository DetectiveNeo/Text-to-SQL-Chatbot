"""
Docstring for src.agent.agent_executor

An agent does the following thingh necessarily
1) Think/Plan : LLM plans the tool
2) Act : your code executes something
3) Observe/Stop : agent decides it is done

Simple AI agent AI decides what to do next and the Python code does it.

"""

from openai import OpenAI
import json
from src.config import OPENAI_API_KEY
from src.agent.tools import write_file, finish, retrieve_documents

client = OpenAI(api_key= OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a simple Python AI Agent.

Your job is to decide the next tool needed to complete task.

You must respond ONLY with valid JSON.

{
    "thought" : string,
    "tool" : "retrieve_documents" or "write_file" or "finish",
    "tool_input" : {
            "content" : string
        }
}

Rules :
- Choose exactly one tool at a time "retrieve_documents" or "write_file" or "finish"
- If you recieve confirmation that the Task is completed then you mush choose tool "finish"
- Content should be in simple plain words. (Maximum Words allowed : 10)
- No Markdown no explanations
"""

TOOLS = {
    "retrieve_documents" : retrieve_documents,
    "write_file" : write_file,
    "finish" : finish
}


TASK = "What is a Calendar ? save it in a file"


def call_llm(model= "gpt-4.1-mini", SYSTEM_PROMPT= SYSTEM_PROMPT, TASK= TASK):
    response = client.responses.create(
        model= model,
        input= [
                {
                    "role" : "system",
                    "content" : SYSTEM_PROMPT
                },
                {
                    "role" : "user",
                    "content" : TASK
                }
            ]
    )
    return response.output_text