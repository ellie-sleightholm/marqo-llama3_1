# Marqo x Llama 3.1 for RAG

This is a small demo of a Local RAG Question and Answering System with [LlaMa 3.1](https://llama.meta.com/) and [Marqo](https://github.com/marqo-ai/marqo). This project has been built based off the original Marqo & Llama repo by [Owen Elliot](https://github.com/OwenPendrighElliott/LocalMarqoQA).

Article to accompany project: [Fully Local RAG with Llama 3.1 & Marqo](https://marqo.ai/blog/marqo-llama-rag)

<p align="center">
    <a><img src="https://github.com/ellie-sleightholm/marqo-llama3_1/blob/main/assets/marqo_llama3_1_demo.gif"></a>
</p>

## Setup and Installation
I have also written an [article](https://marqo.ai/blog/marqo-llama-rag) that walks through this project that I encourage you to read when getting started.

### Clone This Repository
First clone this repository:
```
git clone https://github.com/ellie-sleightholm/marqo-llama3_1.git
```

### Frontend

Installs the necessary Node.js packages for the frontend project and then start the development server. This will be at http://localhost:3000.
```
cd frontend
npm i
npm run dev
```
The frontend will look the same as in the video at the top of this README. 

### Backend

#### 1. Obtaining Llama 3.1 Models
To run this project locally, you will need to obtain the appropriate models. If you have 16GB of RAM, I would recommend starting with 8B parameter LlaMa 3.1 GGUF models. For this demo I used `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`. 

There are several models you can download from the `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF` [Hugging Face hub](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main). I recommend starting with `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`. The demo video above uses `Q2_K`.

Download this model and place it into a new directory `backend/models/8B/`.

_**Important note**_: there is some adjustment needed for llama cpp (see this [issue](https://github.com/ggerganov/llama.cpp/issues/8650)). Please be aware of this when working with this project.

#### 2. Install Dependencies
Next, navigate to the backend directory, create a virtual environment, activate it, and install the required Python packages listed in the [requirements.txt](/backend/requirements.txt) file.

```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To run this project, you'll need download NLTK (Natural Language Toolkit) data because the [`document_processors.py`](/backend/document_processors.py) script uses NLTK's sentence tokenization functionality. Specifically, the `sentence_chunker` and `sentence_pair_chunker` functions rely on NLTK's sent_tokenize method to split text into sentences.

Specify Python interpreter:
```
python3
```
Import NLTK:
```python
import nltk
nltk.download("all")
```

#### 3. Run Marqo
For the RAG aspect of this project, I will be using [Marqo](https://marqo.ai/), the end-to-end vector search engine.

Marqo requires Docker. To install Docker go to the [Docker Official website](https://docs.docker.com/get-docker/). Ensure that docker has at least 8GB memory and 50GB storage. In Docker desktop, you can do this by clicking the settings icon, then resources, and selecting 8GB memory.

Use docker to run Marqo:

```bash
docker rm -f marqo
docker pull marqoai/marqo:latest
docker run --name marqo -it -p 8882:8882 marqoai/marqo:latest
```
When the project starts, the Marqo index will be empty until you add information in the 'Add Knowledge' section of the frontend. 

Great, now all that's left to do is run the webserver!

#### 4. Run the Web Server
Starts a Flask development server in debug mode on port 5001 using Python 3:
```
python3 -m flask run --debug -p 5001
```

Navigate to http://localhost:3000 and begin inputting your questions to Llama 3.1!

## Experimenting
When running this project, feel free to experiment with different settings. 

You can change the model in [`backend/ai_chat.py`](/backend/ai_chat.py):
```python
LLM = Llama(
    model_path="models/8B/your_model",
)
```

You can also change the score in the function `query_for_content` in [`backend/knowledge_store.py`](/backend/knowledge_store.py):
```python
relevance_score = 0.6
```
This queries the Marqo knowledge store and retrieves content based on the provided query. It filters the results to include only those with a relevance score above *0.6* and returns the specified content from these results, limited to a maximum number of results as specified by the limit parameter. Feel free to change this score depending on your relevance needs. 

## Specifications
This can run locally on an M1 or M2 Mac or with a CUDA capable GPU on Linux or Windows. If you want to run this on an M1 or M2 Mac please be sure to have the ARM64 version of Python installed, this will make `llama.cpp` builds for ARM64 and utilises Metal for inference rather than building for an x86 CPU and being emulated with Rosetta.

## Further Work
This is a very simple demo. Future work on this project will include several enhancements:
* Enable Chatbot Memory: Store conversation history to make conversing with the chatbot more like a real-life experience
* Provide an Initial Set of Documents: at the moment, when the project starts, the Marqo index is empty. Results will be better if we preload the Marqo knowledge store with a set of initial documents relevant to the domain of interest.
* Improve User Interface
* Optimize Backend Performance
* Extend Support for Different Document Types

## Further Guidance
To accompany this project, I wrote an [article](https://www.marqo.ai/blog/marqo-llama-rag) covering how you can run this repository and what you can expect to see when doing so. Visit this [article](https://www.marqo.ai/blog/marqo-llama-rag) for further guidance and information.
