import streamlit as st
from prediction_module import predict_class

st.set_page_config(page_title="SQLi Detection",page_icon="👾",layout="wide")	# Set the page title and icon

st.title("SQLi Detection")																																			# Set the title of the page
st.text("""This page is used to detect SQLi attacks.																						
Please enter the SQL query in the text box below to detect if this query is a SQLi attack.""")	# Set the text of the page

st.header("Enter SQL query")												# Set the header of the page
with st.form("SQLi Detection"):											# Create a form with name "SQLi Detection"
		query = st.text_input("Enter SQL query here")		# Create a text input with name "Enter SQL query here"
		if st.form_submit_button("Submit"):							# if the user clicks the submit button
			isSQLi = predict_class(query)									# Call the predict_class function and store the result in isSQLi
			st.write("Your query is:", query)							# Write the query in the text box
			if isSQLi:																		# If the query is a SQLi attack
				st.write("This is a SQLi attack")						# Write "This is a SQLi attack"
			else:																					
				st.write("This is not a SQLi attack")				# else write "This is not a SQLi attack"