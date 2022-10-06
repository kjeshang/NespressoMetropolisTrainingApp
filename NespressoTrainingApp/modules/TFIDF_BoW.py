import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# Constant Variables

stop_words = "english";
token_pattern = r"\b[a-zA-Z]{3,}\b";

# Functions

def get_dataframeNLP(df, coffee_select):
    df_coffeeSelect = df[df["Name"] == coffee_select];
    df_NLP = pd.concat([df_coffeeSelect, df]);
    df_NLP = df_NLP.drop_duplicates();
    df_NLP = df_NLP[df_NLP.columns.tolist()[1:]];
    df_NLP = df_NLP.reset_index();
    return df_NLP;

def get_recommendations(df_NLP, coffee_select, numRec, indices, cosine_sim):
    idx = indices[coffee_select];
    sim_scores = list(enumerate(cosine_sim[idx]));
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True);
    sim_scores = sim_scores[1:numRec+1];
    coffee_indices = [i[0] for i in sim_scores];
    df_Rec = df_NLP[["Name","Type","Serving","Headline","Intensity","Category"]].iloc[coffee_indices];
    
    similarityScores = [];
    for i in range(len(sim_scores)):
        similarityScores.append(round(sim_scores[i][1], 4));
    df_Rec["Similarity Score"] =  similarityScores;
    
    df_Rec = df_Rec.reset_index().rename(columns={"index":"id"});
    
    return df_Rec;

# Term Frequency - Inverse Document Frequency Frequency (TF-IDF) Recommendations:
def get_recommendationResultsTFIDF(df, coffee_select, numRec, min_df, max_df, max_features, stop_words, sublinear_tf, n_lower, n_upper):
    df_NLP = get_dataframeNLP(df, coffee_select);
        
    vectorizer = TfidfVectorizer(min_df=min_df, max_df=max_df, max_features=max_features, stop_words=stop_words, sublinear_tf=sublinear_tf, ngram_range=(n_lower, n_upper));
    matrix = vectorizer.fit_transform(df_NLP["Textual Info"]);
    cosine_sim = linear_kernel(matrix, matrix);
    indices = pd.Series(df_NLP.index, index=df_NLP["Name"]).drop_duplicates();
    
    df_Rec = get_recommendations(df, coffee_select, numRec, indices, cosine_sim);
    
    return df_Rec;

# Bag of Words Recommendations:
def get_recommendationResultsBagOfWords(df_Prep, coffee_select, numRec, min_df, max_df, max_features, stop_words, analyzer, token_pattern, n_lower, n_upper):
    df_NLP = get_dataframeNLP(df_Prep, coffee_select);
    
    vectorizer = CountVectorizer(min_df=min_df, max_df=max_df, max_features=max_features, stop_words=stop_words, analyzer=analyzer, token_pattern=token_pattern, ngram_range=(n_lower, n_upper));
    matrix = vectorizer.fit_transform(df_NLP["Textual Info"]);
    cosine_sim = cosine_similarity(matrix, matrix);
    indices = pd.Series(df_NLP.index, index=df_NLP["Name"]).drop_duplicates();
    
    df_Rec = get_recommendations(df_NLP, coffee_select, numRec, indices, cosine_sim);
    
    return df_Rec;

# Retrieve Recommendation Results as a Dataframe based on technique selected:
def get_recommendationResults(techniqueSelected, df, coffee_select, numRec, min_df, max_df, max_features, stop_words, n_lower, n_upper, sublinear_tf, analyzer, token_pattern):
    # TF-IDF
    if techniqueSelected == 0:
        dff_rec = get_recommendationResultsTFIDF(df, coffee_select, numRec, min_df, max_df, max_features, stop_words, sublinear_tf, n_lower, n_upper);
    # BoW
    elif techniqueSelected == 1:
        dff_rec = get_recommendationResultsBagOfWords(df, coffee_select, numRec, min_df, max_df, max_features, stop_words, analyzer, token_pattern, n_lower, n_upper)

    return dff_rec;

# TF-IDF Feature Results:
def get_featureResultsTFIDF(df, coffee_select, min_df, max_df, max_features, stop_words, sublinear_tf, n_lower, n_upper):
    df_NLP = get_dataframeNLP(df, coffee_select);
        
    vectorizer = TfidfVectorizer(min_df=min_df, max_df=max_df, max_features=max_features, stop_words=stop_words, sublinear_tf=sublinear_tf, ngram_range=(n_lower, n_upper));
    matrix = vectorizer.fit_transform(df_NLP["Textual Info"]);
    df_Feature = pd.DataFrame(matrix[0].T.todense(), 
        index=vectorizer.get_feature_names_out(), 
        columns=["TF-IDF"]
    );
    df_Feature = df_Feature.sort_values('TF-IDF', ascending=True);
    df_Feature = df_Feature[df_Feature["TF-IDF"] > 0];
    return df_Feature;

# BoW Feature Results:
def get_featureResultsBagOfWords(df, coffee_select, min_df, max_df, max_features, stop_words, analyzer, token_pattern, n_lower, n_upper):
    df_NLP = get_dataframeNLP(df, coffee_select);
        
    vectorizer = CountVectorizer(min_df=min_df, max_df=max_df, max_features=max_features, stop_words=stop_words, analyzer=analyzer, token_pattern=token_pattern, ngram_range=(n_lower, n_upper));
    matrix = vectorizer.fit_transform(df_NLP["Textual Info"]);
    df_Feature = pd.DataFrame(matrix[0].T.todense(), 
        index=vectorizer.get_feature_names_out(), 
        columns=["Bag of Words"]
    );
    df_Feature = df_Feature.sort_values('Bag of Words', ascending=True);
    df_Feature = df_Feature[df_Feature["Bag of Words"] > 0];
    return df_Feature;

# Retrieve Feature Results as a Dataframe based on technique selected:
def get_featureResults(techniqueSelected, df, coffee_select, min_df, max_df, max_features, stop_words, n_lower, n_upper, sublinear_tf, analyzer, token_pattern):
    # TF-IDF:
    if techniqueSelected == 0:
        df_Feature = get_featureResultsTFIDF(df, coffee_select, min_df, max_df, max_features, stop_words, sublinear_tf, n_lower, n_upper);
    elif techniqueSelected == 1:
        df_Feature = get_featureResultsBagOfWords(df, coffee_select, min_df, max_df, max_features, stop_words, analyzer, token_pattern, n_lower, n_upper);
    return df_Feature;