<<<<<<< HEAD
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
=======
import streamlit as st
from transformers import pipeline

@st.cache(allow_output_mutation=True)
def load_summarizer():
    model = pipeline("summarization", device=0)
    return model


def generate_chunks(inp_str):
    max_chunk = 500
>>>>>>> 074e8ba622f6da59f38d8e8467383739550cbc09
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
<<<<<<< HEAD

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
=======
st.title("Summarize Text")
sentence = st.text_area('Please paste your article :', height=30)
button = st.button("Summarize")

max = st.sidebar.slider('Select max', 50, 500, step=10, value=150)
min = st.sidebar.slider('Select min', 10, 450, step=10, value=50)
do_sample = st.sidebar.checkbox("Do sample", value=False)
with st.spinner("Generating Summary.."):
    if button and sentence:
        chunks = generate_chunks(sentence)
        res = summarizer(chunks,
                         max_length=max, 
                         min_length=min, 
                         do_sample=do_sample)
        text = ' '.join([summ['summary_text'] for summ in res])
        # st.write(result[0]['summary_text'])
>>>>>>> 074e8ba622f6da59f38d8e8467383739550cbc09
        st.write(text)
