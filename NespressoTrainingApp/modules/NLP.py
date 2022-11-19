import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity, euclidean_distances, manhattan_distances
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score, roc_curve

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
def get_recommendationResultsTFIDF(df, coffee_select, numRec, min_df, max_df, max_features, stop_words, sublinear_tf, n_lower, n_upper, similarity):
    df_NLP = get_dataframeNLP(df, coffee_select);
        
    vectorizer = TfidfVectorizer(min_df=min_df, max_df=max_df, max_features=max_features, stop_words=stop_words, sublinear_tf=sublinear_tf, ngram_range=(n_lower, n_upper));
    matrix = vectorizer.fit_transform(df_NLP["Textual Info"]);
    sim_measure = similarity(matrix, matrix);
    indices = pd.Series(df_NLP.index, index=df_NLP["Name"]).drop_duplicates();
    
    df_Rec = get_recommendations(df, coffee_select, numRec, indices, sim_measure);
    if (similarity.__name__ != 'cosine_similarity') & (similarity.__name__ != 'linear_kernel'):
        df_Rec = df_Rec.sort_values(by='Similarity Score', ascending=True).reset_index(drop=True);
    
    return df_Rec;

# Bag of Words Recommendations:
def get_recommendationResultsBagOfWords(df_Prep, coffee_select, numRec, min_df, max_df, max_features, stop_words, analyzer, token_pattern, n_lower, n_upper, similarity):
    df_NLP = get_dataframeNLP(df_Prep, coffee_select);
    
    vectorizer = CountVectorizer(min_df=min_df, max_df=max_df, max_features=max_features, stop_words=stop_words, analyzer=analyzer, token_pattern=token_pattern, ngram_range=(n_lower, n_upper));
    matrix = vectorizer.fit_transform(df_NLP["Textual Info"]);
    sim_measure = similarity(matrix, matrix);
    indices = pd.Series(df_NLP.index, index=df_NLP["Name"]).drop_duplicates();
    
    df_Rec = get_recommendations(df_NLP, coffee_select, numRec, indices, sim_measure);
    if (similarity.__name__ != 'cosine_similarity') & (similarity.__name__ != 'linear_kernel'):
        df_Rec = df_Rec.sort_values(by='Similarity Score', ascending=True).reset_index(drop=True);
    
    return df_Rec;

# Retrieve Recommendation Results as a Dataframe based on technique selected:
def get_recommendationResults(techniqueSelected, df, coffee_select, numRec, min_df, max_df, max_features, stop_words, n_lower, n_upper, sublinear_tf, analyzer, token_pattern, similarity):
    # TF-IDF
    if techniqueSelected == 0:
        dff_rec = get_recommendationResultsTFIDF(df, coffee_select, numRec, min_df, max_df, max_features, stop_words, sublinear_tf, n_lower, n_upper, similarity);
    # BoW
    elif techniqueSelected == 1:
        dff_rec = get_recommendationResultsBagOfWords(df, coffee_select, numRec, min_df, max_df, max_features, stop_words, analyzer, token_pattern, n_lower, n_upper, similarity);

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

# Get Validation by Classification Information:
def getPipeAccuracy(dataframe, features, target, vectorizer, test_size, random_state, alpha, parameters, cv, refit):
    X_train, X_test, y_train, y_test = train_test_split(dataframe[features], dataframe[target], test_size=test_size, random_state=random_state)
    if alpha == None:
        pipe = Pipeline([
            ('vectorizer', vectorizer), 
            ('mulNB', MultinomialNB())
        ]);
    else:
        pipe = Pipeline([
            ('vectorizer', vectorizer), 
            ('mulNB', MultinomialNB(alpha=alpha))
        ]);
    pipe.fit(X_train, y_train);
    pipeScore = pipe.score(X_test, y_test);
    print(f'Pipe Score = {pipeScore}');
    # y_predPipe = pipe.predict(X_test);
    # print(classification_report(y_test, y_predPipe, zero_division=0));
    
    grid = GridSearchCV(pipe, param_grid=parameters, cv=cv, refit=refit, scoring='accuracy');
    grid.fit(X_train, y_train);
    print(f'Grid Best Parameter = {grid.best_params_}');
    print(f'Grid Best Score = {grid.best_score_}');
    # gridScore = grid.score(X_test, y_test);
    # print(f'Grid Score = {gridScore}');
    y_predGrid = grid.best_estimator_.predict(X_test);
    cr = classification_report(y_test, y_predGrid, zero_division=0, output_dict=True);
    df_cr = pd.DataFrame(cr).transpose().round(3);

    data = confusion_matrix(y_test, y_predGrid);
    df_cm = pd.DataFrame(data, columns=np.unique(y_test), index=np.unique(y_test));
    df_cm.index.name = 'Actual';
    df_cm.columns.name = 'Predicted';
    df_cm = df_cm.round(2);

    data = [[pipeScore, grid.best_params_.get('mulNB__alpha'), grid.best_score_]];
    df_score = pd.DataFrame(data, columns=['Pipe Score','MultinomialNB Best Alpha','Grid Best Score']);
    df_score = df_score.round(2);

    return df_cm, df_cr, df_score;