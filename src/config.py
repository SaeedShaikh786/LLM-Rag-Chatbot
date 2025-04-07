import os

import streamlit as st

PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

'''
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

'''