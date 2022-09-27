import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class TFIDF:
    
    def __init__(self, df_Prep, type, coffee_select, numRec, min_df, max_df, max_features, stop_words, n_lower, n_upper, sublinear_tf):
        self.df_Prep = df_Prep;
        self.type = type;
        self.coffee_select = coffee_select;
        self.numRec = numRec;
        self.min_df = min_df;
        self.max_df = max_df;
        self.max_features = max_features;
        self.stop_words = stop_words;
        self.n_lower = n_lower;
        self.n_upper = n_upper;
        self.sublinear_tf = sublinear_tf;
    
    def _get_dataframeNLP(self):
        mask = (self.df_Prep["Type"] == self.type) & (self.df_Prep["Name"] == self.coffee_select);
        df_coffeeSelect = self.df_Prep[mask];
        df_NLP = pd.concat([df_coffeeSelect, self.df_Prep]);
        df_NLP = df_NLP.drop_duplicates();
        df_NLP = df_NLP[df_NLP.columns.tolist()[1:]];
        df_NLP = df_NLP.reset_index();
        return df_NLP;
    
    def _get_recommendations(self, df_NLP, indices, cosine_sim):
        idx = indices[self.coffee_select];
        sim_scores = list(enumerate(cosine_sim[idx]));
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True);
        sim_scores = sim_scores[1:self.numRec+1];
        coffee_indices = [i[0] for i in sim_scores];
        df_Rec = df_NLP[["Name","Serving","Headline","Intensity","Category"]].iloc[coffee_indices];
        
        similarityScores = [];
        for i in range(len(sim_scores)):
            similarityScores.append(round(sim_scores[i][1], 4));
        df_Rec["Similarity Score"] =  similarityScores;
        
        df_Rec = df_Rec.reset_index().rename(columns={"index":"id"});
        
        return df_Rec;


    def _get_recommendationResultsTFIDF_Vertuo(self):
        df_NLP = self._get_dataframeNLP();
            
        vectorizer = TfidfVectorizer(min_df=self.min_df, max_df=self.max_df, max_features=self.max_features, stop_words=self.stop_words, sublinear_tf=self.sublinear_tf, ngram_range=(self.n_lower, self.n_upper));
        
        matrix = vectorizer.fit_transform(df_NLP["Textual Info"]);
        cosine_sim = linear_kernel(matrix, matrix);
        
        indices = pd.Series(df_NLP.index, index=df_NLP["Name"]).drop_duplicates();
        
        df_Rec = self._get_recommendations(df_NLP, indices, cosine_sim);
        
        return df_Rec;