#from cgitb import text
from flask import Flask,jsonify,render_template,request
#importing the os module
import os

#to get the current working directory
dir = os.getcwd() + "/" + 'nltk_data'
print(dir)

import nltk
nltk.data.path.append(dir)

import pickle as pk
app = Flask('__name__')

# load the pickle files 
count_vector = pk.load(open('Pickle/count_vector.pkl','rb'))            # Count Vectorizer
tfidf_transformer = pk.load(open('Pickle/tfidf_transformer.pkl','rb')) # TFIDF Transformer
LR_model = pk.load(open('Pickle/model.pkl','rb'))                          # Classification Model
#model = pk.load(open('Pickle/model.pkl','rb'))                          # Classification Model
recommend_matrix = pk.load(open('Pickle/user_final_rating.pkl','rb'))   # User-User Recommendation System 

import model

valid_userid = ['warren','00sab00','1234','zippy','zburt5','joshua','dorothy w','rebecca','walker557','samantha','raeanne','kimmie','cassie','moore222']
@app.route('/')
def view():
    return render_template('index.html')

@app.route('/recommend',methods=['POST'])
def recommend_top5():
    print(request.method)
    user_name = request.form['User Name']
    print('User name=',user_name)
    
    if  user_name in valid_userid and request.method == 'POST':
            top20_products = model.recommend_products(user_name)
            print(top20_products.head())
            get_top5 = model.top5_products(top20_products)
            #return render_template('index.html',tables=[get_top5.to_html(classes='data',header=False,index=False)],text='Recommended products')
            return render_template('index.html',column_names=get_top5.columns.values, row_data=list(get_top5.values.tolist()), zip=zip,text='Recommended products')
    elif not user_name in  valid_userid:
        return render_template('index.html',text='No Recommendation found for the user')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)
