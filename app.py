import streamlit as st
import openai
import json
import requests
from transformers import GPT2Tokenizer
from newspaper import Article
from bs4 import BeautifulSoup

# Create a sidebar for the user to input their API key
api_key = st.sidebar.text_input("Enter your GPT API key", value="", type="password")

# Check if the api_key is provided
if not api_key:
    st.write("Please enter your GPT API key")
    st.stop()

# Define your OpenAI GPT-3 API key
openai.api_key = api_key

# Rest of your code here
import openai
import json
import requests
from transformers import GPT2Tokenizer
from newspaper import Article
from bs4 import BeautifulSoup

# Define your OpenAI GPT-3 API key
openai.api_key = "Your OpenAI Api Key"



def truncate_string_to_tokens(content, max_tokens):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    content_tokens = tokenizer.tokenize(content)
    print(len(content_tokens))
    if len(content_tokens) > max_tokens:
        content_tokens = content_tokens[:max_tokens]
    truncated_content = tokenizer.convert_tokens_to_string(content_tokens)
    return truncated_content




# Function to call GPT-3 and get a response
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

# Function to enhance HTML with schema markup using GPT-3
def enhance_html_with_schema(url):
    # Use newspaper3k to extract relevant information from the URL
    article = Article(url)
    article.download()
    article.parse()
    
    # Prepare content for GPT-3 analysis
    content = f"Title: {article.title}\n"
    content += f"Author: {article.authors}\n"
    content += f"Publication Date: {article.publish_date}\n"
    content += f"Content: {article.text}\n"

    # Truncate content to fit within GPT-3's token limit. If you do not have GPT4, you will need to change the 3500 to 1500 and it may not fit the full html.
    content = truncate_string_to_tokens(content, 3500)
    
    # Analyze content and determine schema type
    schema_type_prompt = f"What schema type should be applied to the following content from URL {url}?\n{content}\nSchema type:"
    schema_type = gpt4_response(schema_type_prompt)
    
    # Extract relevant data points (with example)
    data_points_prompt = (
        
        f"Data points (Simple example for format, yours will be much more comprehensive.Example format: {{\"title\": \"Sample Title\", \"author\": \"John Doe\", \"datePublished\": \"2023-05-01\"}}):"
        f"Extract relevant data points for {schema_type} schema from the following content from URL {url}:\n"
        f"{content}\n"
        f"Use all possible Schema improvements. Remember there are hundreds of potential ways schema might be applied. Your job is to find all possible ways to leverage schema to improve the given html. \n Please go well beyond the example wherever possible. After providing the updated html, also provide a readout/report of the update that would be useful to a client or SEO. Include as many improvements as possible. \n Updated HTML with Schema Applied and final readout/summary:"

    )
    data_points_text = gpt4_response(data_points_prompt)
    return str(data_points_text)



# Sample URL input
url_input = 'https://www.frac.tl/conservative-brands-content-creation/'

# Enhance HTML with schema markup using GPT-3
enhanced_html = enhance_html_with_schema(url_input)

# Save the enhanced HTML to a text file
with open('enhanced_html_output.txt', 'w', encoding='utf-8') as file:
    file.write(str(enhanced_html))

print("Enhanced HTML from GPT4. This output has also been saved to 'enhanced_html_output.txt'")
print(enhanced_html)