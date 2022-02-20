import pickle
import re
import pandas as pd
import numpy as np

_CWD = '.' #for google drive
with open(_CWD+'/model/final_RFC_FE_model.model', 'rb') as file:
	RFC_FE_model = pickle.load(file)
with open(_CWD+'/model/tfidf_vec.sav', 'rb') as file:
	TFIDF_vectorizer = pickle.load(file)

def clean_query(input_string):
	cleaned = re.sub('[^a-zA-Z0-9\s]',' ',input_string)
	cleaned = re.sub('\s{2,}',' ',cleaned)
	return cleaned.lower().strip()

def predict_probab(X_query):
	cleaned_query = clean_query(X_query)
	no_of_special_chars = len(re.findall('[^a-zA-Z0-9\s]',X_query))
	query_length = len(X_query.split())
	no_of_num_eq_num = len(re.findall(r'\d\s*=\s*\d',X_query))
	X_q = TFIDF_vectorizer.transform([cleaned_query])
	X_q_tfidf_FE = pd.DataFrame(data=X_q.toarray(),columns=TFIDF_vectorizer.get_feature_names_out())
	X_q_tfidf_FE['num_sc'] = no_of_special_chars
	X_q_tfidf_FE['q_len'] = query_length
	X_q_tfidf_FE['num_eq_num'] = no_of_num_eq_num
	proba = RFC_FE_model.predict_proba(X_q_tfidf_FE)
	pred_class = RFC_FE_model.predict(X_q_tfidf_FE)
	return proba[0]

def predict_class(X_q_obj, prob=False):
	if isinstance(X_q_obj,list):
		proba = []
		for x in X_q_obj:
			proba.append(predict_probab(x))
		return np.array(proba)
		
	if isinstance(X_q_obj, str):
		proba = predict_probab(X_q_obj)
		class_ = np.argmax(proba)
		if prob:
			return proba
		else:
			return class_