from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA
from langchain.document_loaders import TextLoader

def read_from_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()


kakaotalk_sync_txt = read_from_file('data/project_data_kakaosync.txt')
kakaotalk_social_txt = read_from_file('data/project_data_kakaosocial.txt')
kakaotalk_channel_txt = read_from_file('data/project_data_kakaotalkchannel.txt')

loader = TextLoader('data/project_data_kakaosync.txt')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(texts, embeddings)

# qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=vectordb)
