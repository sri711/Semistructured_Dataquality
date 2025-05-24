import re

def chunk_markdown(markdown: str):
    # Naive sentence-based chunking
    sentences = re.split(r'(?<=[.!?])\s+', markdown)
    return "\n".join(s.strip() for s in sentences if len(s.strip()) > 10)
