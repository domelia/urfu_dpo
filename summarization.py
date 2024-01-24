from PIL import Image
import torch
from transformers import pipeline
import streamlit as st
from transformers import MBartTokenizer, MBartForConditionalGeneration

image1 = Image.open('images/sincerely-media-DgQf1dUKUTM-unsplash.jpg')
device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

st.set_page_config(page_title="", page_icon=':random:', layout="centered")
model_name = "IlyaGusev/mbart_ru_sum_gazeta"
tokenizer = MBartTokenizer.from_pretrained(model_name, max_langth=5000)

@st.cache_resource()
def load_summarizer():
    model = pipeline("summarization", model=model_name, device=device)
    return model


def generate_chunks(inp_str):
    max_chunk=50000
    inp_str = inp_str.replace('.', '.<eos>')
    inp_str = inp_str.replace('?', '?<eos>')
    inp_str = inp_str.replace('!', '!<eos>')
    
    sentences = inp_str.split('<eos>')
    current_chunk = 0 
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])
    return chunks


summarizer = load_summarizer()

st.title("Приложение по созданию аннотаций")
st.sidebar.title("О приложении")
st.sidebar.image(image1)
st.sidebar.info(
"Это демо-приложение создано для автоматического создания аннотаций научных статей на основе библиотеки Transformers и модели ")

st.sidebar.info(
"Автор приложения: [Дарья Омельченко](https://www.asu.ru/univer_about/personalities/484/)"
)


sentence = st.text_area('Введите текст :', height=50)

st.write(f'Ваш текст содержит {len(sentence)} знаков')

button = st.button("Создать аннотацию")

with st.spinner("Подождите, идет процесс создания аннотации.."):
    if button and sentence:
        chunks = generate_chunks(sentence)
        res = summarizer(chunks)
        text = ' '.join([summ['summary_text'] for summ in res])
        st.write(text)
