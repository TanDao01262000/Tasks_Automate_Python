from transformers import pipeline
import textwrap


def summarize_content(text):

    chunks = textwrap.wrap(text, 1024)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
 
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=300, min_length=0, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    full_summary = " ".join(summaries)
    return full_summary
