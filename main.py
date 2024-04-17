# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, request, render_template
import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine
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
city_descriptions = pd.read_csv('static/data/merged_description_city_coded.csv',index_col = 0)
city_embeddings = pd.read_csv('static/data/city_embeddings.csv',index_col = 0)
city_code = pd.read_csv('static/data/city_code.csv',index_col = 0)
city_distance = pd.read_csv('static/data/distance_coded.csv',index_col = 0)
hotel = pd.read_csv('static/data/hotel_city_coded.csv',index_col = 0)
month_dic = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
app = Flask(__name__)


# Flask constructor

# Root endpoint
@app.route('/', methods=['GET'])
def index():
    ## Display the HTML form template
    return render_template('index.html',departure_list = departure_list,
                           recommended_cities = None,city_descriptions = None,zip = zip)


# `read-form` endpoint
@app.route('/read_form', methods=['POST','GET']) 
def read_form(city_descriptions = city_descriptions):
    # Get the form data as Python ImmutableDict datatype
    if request.method == 'POST':
        data = request.form
        print(data)
        top_num = 25
        departure_date = data['departure_date']
        departure_month = int(departure_date.split('-')[1])
        departure_cities = data.getlist('departureCity')
        departure_cities_code = departure_list[departure_list['city_state'].isin(departure_cities)]['code'].to_list()
        travel_method = data['travel_method']
        hotel_option = data.getlist('hotel_option')
        if data['description']:
            keyword_embedding = get_embedding(data['description'])
            similarities = city_embeddings.apply(lambda x: 1 - cosine(keyword_embedding, x), axis=1)
            top_city_idx = np.argsort(similarities)[-top_num:][::-1]
            top_city_code = city_embeddings.iloc[top_city_idx].index.to_list()
            top_cities = city_descriptions.loc[top_city_code]
        else:
            recommended_cities = None
            city_descriptions = None
            city_rank = None
            city_pic = None
        if travel_method == 'Car':
            driving_time = int(data['driving_time'])
            selected_recommended_cities = city_distance[city_distance['source_code'].isin(departure_cities_code) &
                                                      city_distance['destination_code'].isin(top_cities.index) &
                                                      (city_distance['Duration_val_hour'] < driving_time+2)]
            selected_recommended_cities = selected_recommended_cities.groupby('destination_code').count()
            selected_recommenede_cities = selected_recommended_cities[selected_recommended_cities['source_code']==len(departure_cities_code)].index
            selected_top_cities = top_cities.loc[selected_recommenede_cities]
            recommended_cities = selected_top_cities['city'].to_list()
            city_descriptions = selected_top_cities['description'].to_list()
            city_rank = [x for x in range(1,len(selected_top_cities)+1)]
            city_state = selected_top_cities['state'].to_list()
            city_pic = [f'static/img/city_img/{code}.jpg' for code in selected_top_cities.index.to_list()]
            city_url = selected_top_cities['URL'].to_list()
        else:
            selected_top_cities =  top_cities[:10]
            recommended_cities =selected_top_cities['city'].to_list()
            city_descriptions = selected_top_cities['description'].to_list()
            city_rank = [x for x in range(1,11)]
            city_state = selected_top_cities['state'].to_list()
            city_pic = [f'static/img/city_img/{code}.jpg' for code in selected_top_cities.index.to_list()]
            city_url = selected_top_cities['URL'].to_list()

        cities_hotel_price = []
        for city_code in selected_top_cities.index:
            city_hotel_price = {}
            for star in hotel_option:
                col_name = f'{month_dic[departure_month]}_{star}-star'
                city_hotel_price[star] = hotel.loc[city_code][col_name]
            print(city_hotel_price)
            cities_hotel_price.append(city_hotel_price)

        return render_template('index.html', departure_list=departure_list,cities_hotel_price = cities_hotel_price,
                                recommended_cities = recommended_cities, city_descriptions = city_descriptions,
                                city_rank = city_rank,enumerate = enumerate, city_pic = city_pic, 
                                city_state = city_state, zip = zip,departure_month = month_dic[departure_month],
                               city_url = city_url)

    elif request.method == 'GET':
        return render_template('index.html', departure_list=departure_list,
                               recommended_cities=None, city_descriptions=None, zip=zip)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(port=8080,debug=True)
