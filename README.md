# sqli_detection
Diploma project based on detecting malicious query using machine learning algorithm.  
Scope of the project: Use Machine Learning to detect SQL injection.  
**Dataset**: https://www.kaggle.com/sajid576/sql-injection-dataset  
**App link**: [SQLi Detection](https://share.streamlit.io/mayurkagathara/sqli_detection)

Directory structure:
```
sqli_detection
├── streamlit_app.py     Main file to run the streamlit app_
|── prediction_module.py Prediction module with all the utility functions
├── requirements.txt     Dependencies
├── README.md
├── Documentation        Folder for documentation
├── Notebook             Folder for jupyter notebooks
|── data                 Folder for data
```
**NOTE**: _You can ignore the files in the Documentation and Notebook folder._

## How to run in local
Clone the repo using git clone:
```
git clone https://github.com/mayurkagathara/sqli_detection  
```
Install dependencies using pip:  
```
pip install -r requirements.txt  
```
Go to CMD and run the following command:  
```
streamlit run streamlit_app.py 
```
(Run it from the root directory of the project).
