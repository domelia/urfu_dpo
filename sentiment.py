#!/usr/bin/python3
from transformers  import pipeline
classifier=pipeline("sentiment-analysis", "blancherft/rubert-base-cased-sentiment-rusentiment")
classifier("Я  обожаю программную инженерию")


