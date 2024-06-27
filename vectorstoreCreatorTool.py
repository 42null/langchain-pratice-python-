"""
Credits:
This basis of the langchain in this file was used from a notebook in the tutorial "Langchain-Full-Course-main"
- On GitHub: https://github.com/Coding-Crashkurse/Langchain-Full-Course
- On YouTube: https://www.youtube.com/watch?v=a89vqgK-Qcs
"""

from helperFunctions import *

import pickle

from langchain_community.document_loaders import DirectoryLoader, CSVLoader, BSHTMLLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


if __name__ == '__main__':
    # color_test()
    display_header_text("-~<:({[ Setup ]}):>~-")
    path = input("Please enter the path to directory containing your documents (default = \"../Documents\"): ")
    if(len(path)) == 0:
        path = "../Documents"
    glob_pattern = input("Please enter the file pattern pattern (leave empty to use \"**/*.txt\" and skip loader type): ")
    save_filename = f"{input('Please enter the file name you would like to save the vectorstore as (exclude file extension .pkl)')}.pkl"
    loaderOptionNames = [ "CSVLoader", "BSHTMLLoader", "TextLoader" ]
    if(len(glob_pattern)) == 0:
        glob_pattern = "**/*.txt"
        picked_loader = TextLoader
        pickedIndex = 2
    else:
        pickedIndex = select_one_from_array("Please pick your loader type: ", loaderOptionNames)
        loaderOptions = [
            CSVLoader,
            BSHTMLLoader,
            TextLoader,
        ]
        picked_loader = loaderOptions[pickedIndex]
    loader = DirectoryLoader(
        path=path, glob=glob_pattern, loader_cls=picked_loader, show_progress=True, recursive=True
    )
    chunk_size = get_int_in_range(0,1_000, "the chunk size", 500)
    chunk_overlap = get_int_in_range(0,500, "the chunk overlap size", 100)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    embeddings_model_options = [
        "mxbai-embed-large",
        "nomic-embed-text",
        "all-minilm",
    ]

    embeddings_model = select_one_from_array("Please pick your embeddings model from the list: ", embeddings_model_options)

    fields = [
        ("Documents path", path),
        ("Document Pattern", glob_pattern),
        ("Saving file as", save_filename),
        ("Loader Type", loaderOptionNames[pickedIndex]),
        ("Splitter Chunk Size", str(chunk_size)),
        ("Splitter Chunk Overlap", str(chunk_overlap))

    ]
    print_debugging_variables(fields)

    docs = loader.load()
    display_update_text("Loader loaded...")
    documents = text_splitter.split_documents(docs)
    display_update_text("Text splitter created documents...")
    # print("documents[0]", documents[0])
    embeddings = OllamaEmbeddings(
        model=embeddings_model,
    )
    display_update_text("Embeddings created embeddings...")
    display_update_text("FAISS creating vectorstore...")
    vectorstore = FAISS.from_documents(documents, embeddings)
    display_update_text(f"Saving vectorstore file as \"{save_filename}\"...")

    with open(save_filename, "wb") as f:
        pickle.dump(vectorstore, f)
    