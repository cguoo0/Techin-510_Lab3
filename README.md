# Techin-510_Lab3
This Lab3 is a practice of using Streamlit and SQL database to store and display data.

# Overview
In this lab, I used Supabase to store my CHATGPT prompt data in SQL format. I have learned how to add, delete and edit data for not just coding in the VScode, but also in the UI page to update data. Another key takeaways is apply filters and time selection tools in the prompt history. This practice help me improve my overall skills in both front end and back end development, and also craft my skills in UI design.

# Getting started
psycopg2
A PostgreSQL database
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

# What's included
- CRUD prompt for users to create new prompt, show prompts,update propmts, and delete prompts
- Users can search, and add filter to prompts history
- USers are able to add, edit, and delete current prompts, and also they can add prompts into their favorite.


# What I learned
- Enhanced my understanding of CRUD operations with PostgreSQL using psycopg2 in Python.
- Implemented features to filter data based on user input, enhancing interactivity.
- Used Streamlit's dynamic rerun capabilities to update the UI in response to user actions like editing or deleting entries.
- Utilized `.env` files to securely manage sensitive information like database credentials.
- Used correct URL format to make correct URL link

# Questions
- How to apply the button of edit, delete, and mark as favorite into one line, instead of three seperate lines.
- How to apply the fold and unfold structure for the saved prompts histories.
- How to show and highlight the favorite prompts.