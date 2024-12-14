# Models

## Generative AI chatbot hukum

1. Buat virtual environment:

```
python -m venv venv
```

2. Aktifkan virtual environment:

```
.\venv\Scripts\activate

```

3. Instal dependensi di dalam virtual environment:

```
pip install -r requirements.txt
```

4. Deploy

```
gcloud functions deploy chatbot \
--runtime python310 \
--trigger-http \
--allow-unauthenticated \
--entry-point app

```

```

```
