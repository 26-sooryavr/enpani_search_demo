import streamlit as st
import sys
import os

from pymilvus.model.hybrid import BGEM3EmbeddingFunction
from pymilvus import MilvusClient
from dotenv import load_dotenv

load_dotenv()

# Constants
ENV_VARS = ["MILVUS_DB_PATH", "RETURN_K_RESULTS", "DB_COLLECTION_NAME"]

@st.cache_resource
def load_model():
    return BGEM3EmbeddingFunction(
        model_name='BAAI/bge-m3', # Specify the model name
        device='cpu', # Specify the device to use, e.g., 'cpu' or 'cuda:0'
        use_fp16=False # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
    )

# Functions
def get_env_vars(env_vars_list: list) -> dict:
    """Retrieve environment variables
    @parameter env_vars_list : list - List containing keys of environment variables
    @returns dict - A dictionary of environment variables
    """

    env_vars = {}
    for var in env_vars_list:
        value = os.environ.get(var, "")
        if value == "":
            st.error(f"{var} not set", icon="🚨")
            sys.exit(f"{var} not set")
        env_vars[var] = value

    return env_vars


def get_emb(query: str):
    query_vectors = EMB_MODEL.encode_queries([query])
    return query_vectors["dense"]


def get_search_results(query: str):
    query_emb = get_emb(query)
    return CLIENT.search(
        collection_name=DB_COLLECTION_NAME,  # target collection
        data=query_emb,  # query vectors
        limit=RETURN_K_RESULTS,  # number of returned entities
        output_fields=["title", "url"],  # specifies fields to be returned
    )[0]

def format_search_results(res):
    return f"[{res.title}]({res.url})"


# Initialize search index
env_vars = get_env_vars(ENV_VARS)
CLIENT = MilvusClient(env_vars["MILVUS_DB_PATH"])
EMB_MODEL = load_model()
RETURN_K_RESULTS = int(env_vars["RETURN_K_RESULTS"])
DB_COLLECTION_NAME = env_vars["DB_COLLECTION_NAME"]

# Create UI ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

style = "<style>h1 {text-align: center;} p {text-align: center;} div {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)

# Header image
st.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiXGUX9lum3V9WqAT0flTvCx2RfH7UWGbCPx5uOL7_vD868E8T7-tt0HHVy6V4ZZklpv3KRAOQ3WM5vbIw315swYQ4uxxwc560pgnvxw4oTnxqHKAw4qknQ2eg0cvu3_kAV2Cjyhi5ZLaer/s1600/Border_KinchitKaram_Trust.png")

# Title
st.title("EnPani Search")
st.markdown("Humble attempt at a mini search engine for [EnPani](https://m.youtube.com/playlist?list=PLhrdHlkOIj-W8D_Rj76-4Z0J9d0cjoIuI) built with [Streamlit](https://streamlit.io/) and [Milvus](https://milvus.io/)")

# Search Form
search = st.form('search_bar')
query = search.text_input('Please type your search below (accepts both Tamil and English search queries)').strip()

# These methods called on the form container, so they appear inside the form.
submit = search.form_submit_button('search')

if submit:
    if query:
        results_container = st.container()
        results = get_search_results(query)
        for result in results:
            results_container.write(format_search_results(result))
    else:
        st.markdown("Please type a search query above before searching")
