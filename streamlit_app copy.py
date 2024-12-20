import streamlit as st
from openai import OpenAI

st.title(":material/Neurology: large language model ")
st.write(
    "inspirado por Medicina Computacional [https://www.medicinacomputacional.com/](https://www.medicinacomputacional.com/)."
)

st.logo("logioto77.jpg")

client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

##############################################################################################################################
#                                                 Entrenar con pdf
##############################################################################################################################
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

file_path = "./data_ejemplo/keramatian-et-al-2023-the-canmat-and-isbd-guidelines-for-the-treatment-of-bipolar-disorder-summary-and-a-2023-update-of.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()
print("")
print(len(docs))
print("")
print(f"{docs[0].page_content[:200]}\n")
print("")
print(docs[0].metadata)
print("")

# Splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)
print("")
print("numero de split que se formaron:")
print(len(all_splits))
print("")

# Embeddings
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_1 = embeddings.embed_query(all_splits[0].page_content)
vector_2 = embeddings.embed_query(all_splits[1].page_content)

assert len(vector_1) == len(vector_2)
print("")
print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])
print("")

# Vector stores

from langchain_core.vectorstores import InMemoryVectorStore

vector_store = InMemoryVectorStore(embeddings)









##############################################################################################################################
#                                                 listo habla normal  
##############################################################################################################################
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("preguntas sobre investigación médica?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream = True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
