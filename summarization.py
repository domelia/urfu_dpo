from PIL import Image
import streamlit as st
from transformers import MBartTokenizer, MBartForConditionalGeneration
import requests

image1 = Image.open('images/sincerely-media-DgQf1dUKUTM-unsplash.jpg')
API_URL = "https://api-inference.huggingface.co/models/IlyaGusev/mbart_ru_sum_gazeta"
headers = {"Authorization": f"Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.set_page_config(page_title="", page_icon=':random:', layout="centered")
st.title("Приложение по созданию аннотаций для научных статей")
st.sidebar.title("О приложении")
st.sidebar.image(image1)
st.sidebar.info(
"Это демо-приложение создано для автоматического создания аннотаций научных статей на основе модели, обученной на широком корпусе русскоязычных текстов, --  mbart_ru_sum_gazeta (автор - Илья Гусев) и Inference Endpoints (serverless) API Hugging Face")

st.sidebar.info(
"Автор приложения: [Дарья Омельченко](https://www.asu.ru/univer_about/personalities/484/)"
)


article_text = st.text_area('Введите текст :', height=50)

st.write(f'Ваш текст содержит {len(article_text)} знаков')

button = st.button("Создать аннотацию")

with st.spinner("Подождите, идет процесс создания аннотации.."):
    if button and article_text:
        summary=query(
    {
        "inputs": article_text ,
        "parameters": {"min_length": 200},
    }
)
        st.write(summary[0]['summary_text'])
