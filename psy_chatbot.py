import streamlit as st
from streamlit_chat import message
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

@st.cache_data(ttl=72*3600)
def cached_model():
    model=SentenceTransformer('jhgan/ko-sroberta-multitask')
    return model

@st.cache_data(ttl=72*3600)
def get_dataset():
    targetUrl='https://raw.githubusercontent.com/lyy98ljj75/wellness/main/wellness_dataset.csv'
    df=pd.read_csv(targetUrl)
    df['embedding']=df['embedding'].apply(json.loads)
    return df

model=cached_model()
df=get_dataset()

st.header('심리상담')
st.markdown('파이 챗봇')

if 'generated' not in st.session_state:
    st.session_state['generated']=[]

if 'past' not in st.session_state:
    st.session_state['past']=[]

with st.form('form', clear_on_submit=True):
    user_input=st.text_input('고객님:', '')
    submitted=st.form_submit_button('전송')

if submitted and user_input:
    embedding=model.encode(user_input)
    df['similarity']=df['embedding'].map(lambda x: cosine_similarity([embedding], [x]).squeeze())
    answer=df.loc[df['similarity'].idxmax()]
    st.session_state.past.append(user_input)
    st.session_state.generated.append(answer['챗봇'])

for i in range(len(st.session_state['past'])):
    message(st.session_state['past'][i], is_user=True, key=str(i)+'_user')
    if len(st.session_state['generated'])>i:
        message(st.session_state['generated'][i], key=str(i)+'_bot')
