from llama_cpp import Llama
import json
from typing import List, Union, Generator
from knowledge_store import MarqoKnowledgeStore

# Initialize LLM model with updated configuration
LLM = Llama(
    model_path="models/8B/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,  # Increased context size
    n_gpu_layers=1  # Enable GPU acceleration if available
)

def answer(user_input: str, mks: MarqoKnowledgeStore, limit: int = 5) -> Generator[str, None, None]:
    """Generate an answer based on user input using a LLM and Marqo Knowledge Store.

    Args:
        user_input (str): The user's query.
        mks (MarqoKnowledgeStore): An instance of the MarqoKnowledgeStore for querying context.
        limit (int, optional): The maximum number of context entries to retrieve. Defaults to 5.

    Yields:
        Generator[str, None, None]: The LLM's response in chunks.
    """

    context = mks.query_for_content(user_input, "text", limit)
    # print(json.dumps(context, indent=4))

    sources = "\n".join(f"[{i+1}] {source}" for i, source in enumerate(context))
    print(f"QUERY: {user_input}")
    print("Context from Marqo:", json.dumps(context, indent=4))
    
    prompt = f"""
    {sources}
    Q: {user_input}
    A:"""

    response = ""
    for resp in LLM(prompt, max_tokens=512, stop=["Q:"], stream=True):
        response += resp["choices"][0]["text"]
        yield resp["choices"][0]["text"].encode("utf-8")
