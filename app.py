from flask import Flask,request,render_template
import pandas as pd
import numpy as np
import pickle

df = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


def recommend_songs(song_name, data= df):
  # Base case
  if df[df['track_name'] == song_name].shape[0] == 0:
    print('This song is either not so popular or you\
    have entered invalid_name.\n Some songs you may like:\n')

    for song in data.sample(n=5)['track_name'].values:
      print(song)

  data['similarity_factor'] = get_similarities(song_name, data)

  data.sort_values(by=['similarity_factor', 'rank'],
                   ascending = [False, False],
                   inplace=True)

  # First song will be the input song itself as the similarity will be highest.
  return data[['track_name', 'artist_names']][2:7]
# flask app
app = Flask(__name__)
@app.route('/')
def index():
    names = list(df['track_name'].values)
    return render_template('index.html')

@app.route('/recom',methods=['POST'])
def recom():
    song = request.form['names']
    songs = recommendation(song)
    print(songs)
    return render_template('index.html',songs=songs)


# python main
if __name__ == "__main__":
    app.run(debug=True)
