import numpy as np
import pandas as pd


books=pd.read_csv(r"C:\Users\Sanford Jone\Downloads\Books\Books.csv")
ratings=pd.read_csv(r"C:\Users\Sanford Jone\Downloads\Books\Ratings.csv")
users=pd.read_csv(r"C:\Users\Sanford Jone\Downloads\Books\Users.csv")

ratings_name = ratings.merge(books,on='ISBN')


ratings_name.drop(columns=["ISBN","Image-URL-S","Image-URL-M"],axis=1,inplace=True)

df = ratings_name.merge(users.drop("Age", axis=1), on="User-ID")


df['Location'] = df['Location'].str.split(',').str[-1].str.strip()


no_rating_df = df.groupby('Book-Title').count()['Book-Rating'].reset_index()
no_rating_df.rename(columns={'Book-Rating': 'no_ratings'}, inplace=True)

avg_rating = df.groupby('Book-Title').mean()['Book-Rating'].reset_index()
avg_rating.rename(columns={'Book-Rating': 'avg_ratings'}, inplace=True)
popularity_df = no_rating_df.merge(avg_rating, on='Book-Title')
x=df.groupby("User-ID").count()["Book-Rating"]>200

known_user=x[x].index

fil_rating=df[df["User-ID"].isin(known_user)]

y=fil_rating.groupby("Book-Title").count()["Book-Rating"]>=50

fam_books=y[y].index

final_ratings=fil_rating[fil_rating['Book-Title'].isin(fam_books)]

piv = final_ratings.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')


piv.fillna(0,inplace=True)

from sklearn.metrics.pairwise import cosine_similarity 

sim_score = cosine_similarity(piv)

sim_score.shape

def recommend(book_name):
    index = np.where(piv.index==book_name)[0][0]
    similar_books = sorted(list(enumerate(sim_score[index])),key=lambda x:x[1], reverse=True)[1:11]
    
    data = []
    
    for i in similar_books:
        # data+=[piv.index[i[0]]]
        item = []
        temp_d = books[books['Book-Title'] == piv.index[i[0]]]
        item.extend(list(temp_d.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_d.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_d.drop_duplicates('Book-Title')['Image-URL-L'].values))
        
        data.append(item)
    return data

recommend("I Know This Much Is True (Oprah's Book Club)")


