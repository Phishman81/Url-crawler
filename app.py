import streamlit as st 
import openai 
import json 
import requests 
from transformers import GPT2Tokenizer 
from newspaper import Article 
from bs4 import BeautifulSoup 

# Create a sidebar for the user to input their API key 
api_key = st.sidebar.text_input("Enter your GPT API key", value="", type="password") 
url_input = st.text_input("Enter the URL to enhance", value="")

# Check if the api_key and URL are provided 
if not api_key or not url_input: 
    st.write("Please enter your GPT API key and URL to enhance") 
    st.stop()

# Define your OpenAI GPT-3 API key 
openai.api_key = api_key 

def truncate_string_to_tokens(content, max_tokens): 
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2") 
    content_tokens = tokenizer.tokenize(content)
    if len(content_tokens) > max_tokens: 
        content_tokens = content_tokens[:max_tokens] 
    truncated_content = tokenizer.convert_tokens_to_string(content_tokens) 
    return truncated_content 

def gpt4_response(prompt): 
    response = openai.ChatCompletion.create( 
                model="gpt-4", 
                messages=[ 
                    { 
                        "role": "system", 
                        "content": "Please simulate an expert at SEO Schema. Your goal is to think step by step and provide the highest quality, most accurate result possible for the given question." 
                    }, 
                    { 
                        "role": "user", 
                        "content": f"{prompt}" 
                    } 
                ], 
                max_tokens=1000, 
                n=1, 
                stop=None, 
                temperature=0.7,
            ) 
      
    result = response["choices"][0]["message"]["content"].strip() 
    return result 

def enhance_html_with_schema(url): 
    article = Article(url) 
    article.download() 
    article.parse() 

    content = f"Title: {article.title}\n" 
    content += f"Author: {article.authors}\n" 
    content += f"Publication Date: {article.publish_date}\n" 
    content += f"Content: {article.text}\n"

    content = truncate_string_to_tokens(content, 3500) 

    schema_type_prompt = f"What schema type should be applied to the following content from URL {url}?\n{content}\nSchema type:" 
    schema_type = gpt4_response(schema_type_prompt) 

    data_points_prompt = (
        f"Data points (Simple example for format, yours will be much more comprehensive.Example format: {{\"title\": \"Sample Title\", \"author\": \"John Doe\", \"datePublished\": \"2023-05-01\"}}):"
        f"Extract relevant data points for {schema_type} schema from the following content from URL {url}:\n"
        f"{content}\n"
        f"Use all possible Schema improvements. Remember there are hundreds of potential ways schema might be applied. Your job is to findall possible ways to leverage schema to improve the given html. \n Please go well beyond the example wherever possible. After providing the updated html, also provide a readout/report of the update that would be useful to a client or SEO. Include as many improvements as possible. \n Updated HTML with Schema Applied and final readout/summary:"
    )
    data_points_text = gpt4_response(data_points_prompt) 
    return str(data_points_text) 

# Enhance HTML with schema markup using GPT-3 
enhanced_html = enhance_html_with_schema(url_input)

# Display the enhanced HTML
st.text(enhanced_html)
