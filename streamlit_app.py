import streamlit as st
from prediction_module import predict_class

st.set_page_config(page_title="SQLi Detection",page_icon="📝",layout="wide")

st.title("SQLi Detection")
st.text("""This page is used to detect SQLi attacks.
Please enter the SQL query in the text box below to detect if this query is a SQLi attack.""")

st.header("Enter SQL query")
with st.form("SQLi Detection"):
		query = st.text_input("Enter SQL query here")
		if st.form_submit_button("Submit"):
			isSQLi = predict_class(query)
			st.write("Your query is:", query)
			if isSQLi:
				st.write("This is a SQLi attack")
			else:
				st.write("This is not a SQLi attack")