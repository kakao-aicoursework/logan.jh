from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
import os

from util import read_from_file

DB_DIR = 'chroma-persist'
embedding_model = OpenAIEmbeddings()


# file 이름에 의존적
def get_collection_name(file_path: str) -> str:
    return file_path.rsplit('/')[-1].split('.')[0].lstrip('project_data_')


def initialize_database(document_dict: dict):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    for k, v in document_dict.items():
        texts = text_splitter.split_documents(v)
        Chroma.from_documents(
            texts,
            embedding_model,
            collection_name=k,
            persist_directory=DB_DIR
        )
        print('db succcess')

def query_db(client, query: str, use_retriever: bool = False) -> list[str]:
    if use_retriever:
        docs = client.as_retriever().get_relevant_documents(query)
    else:
        docs = client.similarity_search(query)

    str_docs = [doc.page_content for doc in docs]
    return str_docs


def get_db_client(collection_name: str):
    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=embedding_model,
        collection_name=collection_name,
    )


kakaotalk_sync_txt = read_from_file('data/project_data_kakaosync.txt')
kakaotalk_social_txt = read_from_file('data/project_data_kakaosocial.txt')
kakaotalk_channel_txt = read_from_file('data/project_data_kakaotalkchannel.txt')

path_list = ['data/project_data_kakaosync.txt', 'data/project_data_kakaosocial.txt',
             'data/project_data_kakaotalkchannel.txt']
doc_dict = {get_collection_name(p): TextLoader(p).load() for p in path_list}
client_dict = {get_collection_name(p): get_db_client(get_collection_name(p)) for p in path_list}

if not os.path.exists(DB_DIR):
    # TODO preprocessing
    initialize_database(doc_dict)