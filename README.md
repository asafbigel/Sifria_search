# Sifria Search

This project provides a set of tools for creating a searchable index of Jewish texts, primarily sourced from Sefaria, and then querying those texts. The goal is to enable efficient semantic search and question-answering over a corpus of Jewish literature.

## Features

*   **Text Import**: Import texts from Sefaria (or other sources) into a local format.
*   **Index Creation**: Generate a searchable index from the imported texts using various indexing strategies.
*   **Semantic Search**: Perform semantic searches on the indexed texts to find relevant passages.
*   **Question Answering (QA)**: Ask questions and retrieve answers directly from the text corpus.

## Setup

To set up the project, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/asafbigel/Sifria_search.git
    cd Sifria_search
    ```

2.  **Create a Python virtual environment** (recommended):
    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```
    (Note: A `requirements.txt` file will be created in a later step if it doesn't exist.)

## Usage

### 1. Import Sefaria Texts

The `import_sefaria_text.py` script is used to download and process texts from Sefaria.

```powershell
python import_sefaria_text.py
```

### 2. Create the Search Index

There are two main scripts for creating the index:

*   `create_index.py`: Creates a basic index.
*   `create_full_index.py`: Creates a more comprehensive index, potentially including embeddings or advanced processing.

Choose the appropriate script based on your needs:

```powershell
python create_index.py
# OR
python create_full_index.py
```

### 3. Run the QA Application

The `qa_app.py` script provides an interface for querying the indexed texts.

```powershell
python qa_app.py
```

## Project Files

*   `bereshit_chapter_1.txt`: Example text file (Genesis Chapter 1).
*   `create_full_index.py`: Script to create a comprehensive search index.
*   `create_index.py`: Script to create a basic search index.
*   `import_sefaria_text.py`: Script to import texts from Sefaria.
*   `qa_app.py`: The main application for question answering and semantic search.
*   `README.md`: This README file.
*   `Shlom_Echaiv.txt`: Example text file.
*   `WhatTheManShouldEat.txt`: Example text file.
*   `whoCreatedFromTheMan.txt`: Example text file.
*   `whoIsSholet.txt`: Example text file.