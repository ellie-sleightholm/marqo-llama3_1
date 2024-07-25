# Marqo x Llama 3.1 for RAG

This is a small demo of a RAG Question and Answering System with [LlaMa 3.1](https://llama.meta.com/) and [Marqo](https://marqo.ai/). 

Here is a video demonstration:

<p align="center">
    <a><img src="https://github.com/ellie-sleightholm/marqo-llama3_1/raw/mainline/assets/marqo_llama3_1_demo.mp4.gif"></a>
</p>

## Project Structure

### `frontend/`

This folder contains the code for the frontend of the application, the frontend is written with NextJS and TypeScript.

### `backend/`

This folder contains the backend code, the backend is written as a webserver using flask.

## Running for development

### Frontend

```
cd frontend
npm i
npm run dev
```

### Backend

You will need to get the models to run this locally. If you have 16GB of RAM I recommend starting with 7B parameter LLaMa GGML models, 13B parameter models do work but you must limit the memory usage of Marqo with Docker and remove the ViT-L/14 model from the pre-loading. 32GB RAM will give you enough headroom for 13B or potentially more.

There are a number of models that are commented out in the code, you can find them on hugging face by searching the name. I recommend starting with [Wizard-Vicuna-7B-Uncensored.ggmlv3.q4_K_M](https://huggingface.co/TheBloke/Wizard-Vicuna-7B-Uncensored-GGML/tree/main).

Download the model and place it in a new directory `backend/models/7B/`.

#### Install Dependencies
```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Download NLTK Data
```
python3
```
```python
import nltk
nltk.download("all")
```

#### Run the Webserver
```
python3 -m flask run --debug -p 5001
```

### Marqo

[Follow the getting started guide to run the docker image.](https://docs.marqo.ai/0.0.17/)


## Formatting code

### Frontend

```
cd frontend
npm run format
```

### Backend

```
cd backend
black .
```

## Specifications
This can run locally on an M1 or M2 Mac or with a CUDA capable GPU on Linux or Windows. If you want to run this on an M1 or M2 Mac please be sure to have the ARM64 version of Python installed, this will make `llama.cpp` builds for ARM64 and utilises Metal for inference rather than building for an x86 CPU and being emulated with Rosetta.