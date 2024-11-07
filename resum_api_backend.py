import streamlit as st
import json
import time
from transformers import BartTokenizer, BartForConditionalGeneration, pipeline


@st.cache_resource
def summarize_text(text_input):
    """
    Generate a summary for the given text input using a pre-trained BART model.    
    Args:
        text_input (str): The input text to summarize.    
    Returns:
        dict: A dictionary containing the original text, generated summary, and a unique identifier.
    """

    # Load the model and tokenizer
    model = BartForConditionalGeneration.from_pretrained("model\model_saved")
    tokenizer = BartTokenizer.from_pretrained("model\model_saved")

    # Initialize the summarization pipeline
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

    # Measure the time taken to generate the summary
    start_time = time.time()

    # Generate the summary
    summary = summarizer(
        text_input,
        max_length=80,
        min_length=5,
        length_penalty=5.0,
        num_beams=100,
        early_stopping=True,
    )[0]['summary_text']

    elapsed_time = time.time() - start_time
    # print(f"Elapsed time for summary generation: {elapsed_time:.2f} seconds")

    # Create the summary dictionary
    summary_data = {
        "uid": "unique_id",  # Replace with a real unique ID generator if needed
        "original_text": text_input,
        "generated_summary": summary,
    }

    # Save the summary to a JSON file
    output_file_path = "data/generated-summary.json"
    with open(output_file_path, "w") as json_file:
        json.dump(summary_data, json_file, indent=4)


    return summary_data