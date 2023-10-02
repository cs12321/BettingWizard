from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from metaphor_python import Metaphor
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('web_page.html')

def summarize_url(url):
   
    # Fetch webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract text content from HTML
    paragraphs = soup.find_all('p')
    content = ' '.join([paragraph.text for paragraph in paragraphs])
    
    # Initialize the parser and summarizer
    parser = PlaintextParser.from_string(content, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count=5)  # Number of sentences in the summary

    res = ""
    for sentence in summary:
        res += str(sentence) + " "
    return res

def process_query(query):
   
    metaphor = Metaphor("8b327024-1aef-4b69-87dc-00b200f7ebd4")
    
    url_list = []

    # Store URLs
    res = metaphor.search(query, use_autoprompt=True, num_results=3, start_published_date="2023-09-30")
    for result in res.results:
        url_list.append(result.url)
    
    
    
    # Return tuple containing urls and summary of first url
    return (url_list, summarize_url(url_list[0]))
   
    
@app.route('/process_query', methods=['POST'])
def process_query_route():

    # Retreive data 
    query = request.form['query']
    data = process_query(query)

    # Send data to HTML file
    return render_template('result.html', processed_data=data[0], summarized_data=data[1])


if __name__ == '__main__':
    app.run(debug=True)
