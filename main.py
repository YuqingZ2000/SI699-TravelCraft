# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, render_template, url_for, request, redirect

from flask import Flask, request, render_template
import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine
import pandas as pd
import numpy as np

# Load pre-trained model tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to generate embeddings
def get_embedding(text):
    tokens = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**tokens)
    # Use the average of the last hidden states as the embedding
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings


departure_list = pd.read_csv('static/data/US_cities_latlng.csv')
city_descriptions = pd.read_csv('static/data/city_descriptions.csv',index_col = 0)
city_embeddings = pd.read_csv('static/data/city_embeddings.csv',index_col = 0)

app = Flask(__name__)


# Flask constructor

# Root endpoint
@app.route('/', methods=['GET'])
def index():
    ## Display the HTML form template
    return render_template('index.html',departure_list = departure_list['city'].to_list(),
                           recommended_cities = None,city_descriptions = None)


# `read-form` endpoint
@app.route('/read_form', methods=['POST','GET']) 
def read_form(city_descriptions = city_descriptions):
    # Get the form data as Python ImmutableDict datatype
    data = request.form
    if data['description']:
        keyword_embedding = get_embedding(data['description'])
        similarities = [1 - cosine(keyword_embedding, city_embedding) for index, city_embedding in
                        city_embeddings.iterrows()]
        top_5_idx = np.argsort(similarities)[-5:]
        top_5_cities = city_descriptions.iloc[top_5_idx]
        recommended_cities = top_5_cities['city'].to_list()
        city_descriptions = top_5_cities['description'].to_list()
        city_rank = list(range(1, len(recommended_cities) + 1)) 
    else:
        recommended_cities = None
        city_descriptions = None
        city_rank = None 

    ## Return the extracted information 
    return render_template('index.html',departure_list = departure_list['city'].to_list(),
                           recommended_cities = recommended_cities,city_descriptions = city_descriptions, city_rank = city_rank, 
                           zip = zip)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(port=8080,debug=True)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
