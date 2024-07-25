import re
import nltk
from typing import List

CHUNK_SIZE = 1024

def simple_denewliner(text: str) -> str:
    """Remove multiple newlines and replace with a single newline.

    Args:
        text (str): The input text containing multiple newlines.

    Returns:
        str: The text with multiple newlines replaced by a single newline.
    """
    return re.sub(r"\n{2,}", "\n", text)

def simple_chunker(document: str) -> List[dict]:
    """Chunk the document into fixed-size pieces.

    Args:
        document (str): The input document to be chunked.

    Returns:
        List[dict]: A list of dictionaries, each containing a chunk of text.
    """
    return [{"text": document[i: i + CHUNK_SIZE]} for i in range(0, len(document), CHUNK_SIZE)]

def sentence_chunker(text: str) -> List[dict]:
    """Break the text into chunks at sentence boundaries.

    Args:
        text (str): The input text to be chunked at sentence boundaries.

    Returns:
        List[dict]: A list of dictionaries, each containing a chunk of text broken at sentence boundaries.
    """
    sentences = nltk.sent_tokenize(text)
    chunks, current_chunk = [], ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= CHUNK_SIZE:
            current_chunk += sentence
        else:
            chunks.append({"text": current_chunk.strip()})
            current_chunk = sentence

    if current_chunk:
        chunks.append({"text": current_chunk.strip()})

    return chunks

def sentence_pair_chunker(text: str) -> List[dict]:
    """Break the text into chunks of sentence pairs.

    Args:
        text (str): The input text to be chunked into sentence pairs.

    Returns:
        List[dict]: A list of dictionaries, each containing a chunk of text consisting of a pair of sentences.
    """
    sentences = nltk.sent_tokenize(text)
    chunks = []

    for i in range(0, len(sentences) - 1, 2):
        chunk = sentences[i] + " " + sentences[i + 1]
        chunks.append({"text": chunk.strip()})

    if len(sentences) % 2 != 0:
        chunks.append({"text": sentences[-1].strip()})

    return chunks

def punctuation_smart_chunker(text: str) -> List[dict]:
    """Break the text into chunks at punctuation boundaries.

    Args:
        text (str): The input text to be chunked at punctuation boundaries.

    Returns:
        List[dict]: A list of dictionaries, each containing a chunk of text broken at punctuation boundaries.
    """
    chunks, current_chunk = [], ""
    pattern = re.compile(r"[\n.;,!?]")

    for line in text.splitlines():
        if len(current_chunk) + len(line) <= CHUNK_SIZE:
            current_chunk += line
        else:
            chunks.append({"text": current_chunk.strip()})
            current_chunk = line

        if pattern.search(line):
            chunks.append({"text": current_chunk.strip()})
            current_chunk = ""

    if current_chunk:
        chunks.append({"text": current_chunk.strip()})

    return chunks

def paragraph_chunker(text: str) -> List[dict]:
    """Break the text into chunks at paragraph boundaries.

    Args:
        text (str): The input text to be chunked at paragraph boundaries.

    Returns:
        List[dict]: A list of dictionaries, each containing a chunk of text broken at paragraph boundaries.
    """
    paragraphs = re.split(r"\n\s*\n", text)
    chunks, current_chunk = [], ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= CHUNK_SIZE:
            current_chunk += paragraph
        else:
            chunks.append({"text": current_chunk.strip()})
            current_chunk = paragraph

    if current_chunk:
        chunks.append({"text": current_chunk.strip()})

    return chunks
