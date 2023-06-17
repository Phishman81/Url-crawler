import streamlit as st
import requests
from bs4 import BeautifulSoup

def extract_text(url):
    try:
        # Send a GET request
        response = requests.get(url)
        # If the GET request is successful, the status code will be 200
        if response.status_code == 200:
            # Get the content of the response
            webpage_content = response.content
            # Create a BeautifulSoup object and specify the parser
            soup = BeautifulSoup(webpage_content, 'html.parser')
            # Remove all script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            # Get the text from the BeautifulSoup object
            text = soup.get_text()
            # Return the text
            return text
    except Exception as e:
        return str(e)

def main():
    st.title('Webpage Text Extractor')
    url = st.text_input('Enter the URL of the webpage')
    if st.button('Extract Text'):
        if url:
            extracted_text = extract_text(url)
            st.write(extracted_text)
        else:
            st.write('Please enter a URL.')

if __name__ == "__main__":
    main()
