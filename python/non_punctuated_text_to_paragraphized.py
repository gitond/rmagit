#!/usr/bin/env python3
"""
Paragraphize - ASR Text Restoration & Segmentation Pipeline
============================================================

A lightweight UNIX pipe utility that converts unformatted, continuous speech-
to-text (ASR) streams into readable, punctuated paragraphs.

Pipeline Overview:
  1. STDIN: Reads unpunctuated, single-line or raw text from standard input.
  2. Punctuation Restoration: Employs `deepmultilingualpunctuation` (BERT-based)
     to insert missing commas, periods, question marks, and capitalization.
  3. Sentence Segmentation: Uses `spacy` (Sentencizer) to split the punctuated
     text into sentence units without heavy syntactic parsing overhead.
  4. Chunking: Batches sentences into logical paragraph blocks (default: 4 sentences).
  5. STDOUT: Writes formatted double-newline-separated paragraphs to standard output.

Dependencies:
  - deepmultilingualpunctuation (PyPI)
  - spacy (PyPI)
  - en_core_web_sm (SpaCy Model): `python3 -m spacy download en_core_web_sm`

Environment Requirements:
  - CPU-only execution (default). No GPU, CUDA, or Ollama/local LLM setup required.

Usage:
  Direct Pipe:
    $ cat raw_transcript.txt | python3 paragraphize.py

  Integration with shell preprocessing:
    $ ./clean_srt.sh original.srt | python3 paragraphize.py > final_text.txt

  Inline Python Import:
    From another module, pass raw text strings directly to `main()` or adapt logic.

Author: Self-Hosted / Local Pipeline
License: MIT
"""

import sys
import spacy
from deepmultilingualpunctuation import PunctuationModel

def main():
    # 1. Read unix pipe input
    raw_text = sys.stdin.read().strip()
    if not raw_text:
        return

    # 2. Restore punctuation & capitalization
    punct_model = PunctuationModel()
    punct_text = punct_model.restore_punctuation(raw_text)

    # 3. Process with SpaCy for sentence segmentation
    nlp = spacy.load("en_core_web_sm", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "ner"])
    nlp.add_pipe("sentencizer")
    doc = nlp(punct_text)

    # 4. Group sentences into paragraph chunks (e.g., 4 sentences per paragraph)
    sentences = [sent.text.strip() for sent in doc.sents]
    chunk_size = 4

    paragraphs = [
        " ".join(sentences[i:i + chunk_size])
        for i in range(0, len(sentences), chunk_size)
    ]

    # 5. Output paragraphized text
    print("\n\n".join(paragraphs))

if __name__ == "__main__":
    main()
