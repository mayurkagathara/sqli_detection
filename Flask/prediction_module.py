import pickle
import re
import pandas as pd
import numpy as np

import os
import requests

# To load the pickled model and vectorizer
_CWD = os.path.abspath(".")


# Load the pickled vectorizer and model
final_RFC_FE_model_file = _CWD+'/final_RFC_FE_model.model'	# generate path of model agnostic to OS
tfidf_vec_file = _CWD+'/tfidf_vec.sav' # generate path of vectorizer agnostic to OS

# final_RFC_FE_model_file = os.path.join(_CWD,'model','final_RFC_FE_model.model')	# generate path of model agnostic to OS
# tfidf_vec_file = os.path.join(_CWD,'model','tfidf_vec.sav')											# generate path of vectorizer agnostic to OS

# If the model and vectorizer are not already present, download them
if not os.path.isfile(final_RFC_FE_model_file): # If the model is not present
    url = r'https://github.com/mayurkagathara/sqli_detection/blob/master/model/final_RFC_FE_model.model?raw=true' # URL of the model
    resp = requests.get(url)														# Download the model
    with open(final_RFC_FE_model_file, 'wb') as fopen:	# Open the file to write the model
        fopen.write(resp.content)												# Write the model

if not os.path.isfile(tfidf_vec_file):					# If the vectorizer is not present
    url = r'https://github.com/mayurkagathara/sqli_detection/blob/master/model/tfidf_vec.sav?raw=true'	# URL of the vectorizer
    resp = requests.get(url)														# Download the vectorizer
    with open(tfidf_vec_file, 'wb') as fopen:						# Open the file to write the vectorizer
        fopen.write(resp.content)												# Write the vectorizer


with open(final_RFC_FE_model_file, 'rb') as file:
	RFC_FE_model = pickle.load(file)
with open(tfidf_vec_file, 'rb') as file:
	TFIDF_vectorizer = pickle.load(file)

def clean_query(input_string):
	"""
	This function cleans the query by removing special characters and spaces.
	It also converts the query to lower case.
	input_string: string
	return: string
	"""
	cleaned = re.sub('[^a-zA-Z0-9\s]',' ',input_string)	# Remove special characters
	cleaned = re.sub('\s{2,}',' ',cleaned)							# Remove multiple spaces
	return cleaned.lower().strip()											# Convert the query to lower case and remove the leading and trailing spaces

def predict_probab(X_query):
	"""
	This function predicts the probability of the query being a SQLi attack.
	input: string
	Output: numpy array
	"""
	cleaned_query = clean_query(X_query)
	no_of_special_chars = len(re.findall('[^a-zA-Z0-9\s]',X_query)) # Count the number of special characters
	query_length = len(X_query.split())															# Count the number of words in the query
	no_of_num_eq_num = len(re.findall(r'\d\s*=\s*\d',X_query))			# Count the pattern of number = number
	X_q = TFIDF_vectorizer.transform([cleaned_query])								# Transform the query into a vector
	X_q_tfidf_FE = pd.DataFrame(data=X_q.toarray(),columns=TFIDF_vectorizer.get_feature_names_out()) # Convert the vector to a dataframe
	X_q_tfidf_FE['num_sc'] = no_of_special_chars										# Add the number of special characters to the dataframe
	X_q_tfidf_FE['q_len'] = query_length														# Add the number of words to the dataframe
	X_q_tfidf_FE['num_eq_num'] = no_of_num_eq_num										# Add the number of pattern of number = number to the dataframe
	proba = RFC_FE_model.predict_proba(X_q_tfidf_FE)								# Predict the probability of the query being a SQLi attack
	return proba[0]																									# Return the probability of the query being a SQLi attack

def predict_class(X_q_obj, prob=False):
	"""
	This function predicts the class of the query if it is malicious or not.
	if prob is set to True, it returns the probability of the query being a SQLi attack.
	input: X_q_obj: string, prob: boolean
	output: boolean or numpy array
	"""
	if isinstance(X_q_obj,list):				# If the input is a list
		proba = []
		for x in X_q_obj:
			proba.append(predict_probab(x))
		return np.array(proba)						# Return the numpy array of probabilities

	if isinstance(X_q_obj, str):				# If the input is a string
		proba = predict_probab(X_q_obj)		# Predict the probability of the query being a SQLi attack
		class_ = np.argmax(proba)					# Return the class of the query
		if prob:													# If the prob = True
			return proba										# Return the probability value
		else:															# If the prob = False
			return class_										# Return the class of the query