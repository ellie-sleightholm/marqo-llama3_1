# Marqo x Llama 3.1 for RAG

This is a small demo of a RAG Question and Answering System with [LlaMa 3.1](https://llama.meta.com/) and [Marqo](https://marqo.ai/).

<p align="center">
    <a><img src="https://github.com/ellie-sleightholm/marqo-llama3_1/blob/main/assets/marqo_llama3_1_demo.gif"></a>
</p>

## Project Structure

### `frontend/`

This folder contains the code for the frontend of the application, as seen in the video above. This is written with NextJS and TypeScript.

### `backend/`

This folder contains the backend code, the backend is written as a webserver using flask.

## Setup and Installation

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
To run this project locally, you will need to obtain the appropriate models. If you have 16GB of RAM, I would recommend starting with 8B parameter LlaMa 3.1 GGML models. For this demo I used `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`. 

There are several models you can download from the `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF` [Hugging Face hub](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main). I recommend starting with `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`. The demo video above uses `Q2_K`.

Download this model and place it into a new directory `backend/models/8B/`.

Feel free to experiment with different 8B models!

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

Great, now all that's left to do is run the webserver!

#### 4. Run the Web Server
Starts a Flask development server in debug mode on port 5001 using Python 3:
```
python3 -m flask run --debug -p 5001
```

Navigate to http://localhost:3000 and begin inputting your questions to Llama 3.1!

## Further Guidance
To accompany this project, I wrote an article covering how you can run this repository and what you can expect to see when doing so. Visit this article for further guidance and information.

## Specifications
This can run locally on an M1 or M2 Mac or with a CUDA capable GPU on Linux or Windows. If you want to run this on an M1 or M2 Mac please be sure to have the ARM64 version of Python installed, this will make `llama.cpp` builds for ARM64 and utilises Metal for inference rather than building for an x86 CPU and being emulated with Rosetta.
