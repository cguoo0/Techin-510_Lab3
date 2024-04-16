import os
from dataclasses import dataclass
import datetime

import streamlit as st
import psycopg2
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Prompt:
    title: str
    prompt: str
    is_favorite: bool
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

def setup_database():
    con = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS prompts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            prompt TEXT NOT NULL,
            is_favorite BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )streamlit run app.pystreamlit run app.py
        """
    )
    con.commit()
    return con, cur

def display_prompts(cur):
    cur.execute("SELECT * FROM prompts ORDER BY created_at DESC")  # Default sort by created date 
    prompts = cur.fetchall()

def display_prompts(cur, search_term=None):
    if search_term:
        # Use ILIKE for case-insensitive search
        cur.execute("SELECT * FROM prompts WHERE title ILIKE %s ORDER BY created_at DESC", ('%' + search_term + '%',))
    else:
        cur.execute("SELECT * FROM prompts ORDER BY created_at DESC")
    prompts = cur.fetchall()
    return prompts

def main():
    st.title("Prompt Viewer")
    search_term = st.text_input("Search for prompts by title:")

    con, cur = setup_database()
    prompts = display_prompts(cur, search_term)
    

    for prompt in prompts:
        st.subheader(prompt[1])  # Title
        st.write(prompt[2])  # Prompt
        st.write("Favorite:", prompt[3])  # is_favorite
        st.text("Created at: " + str(prompt[4]))
        st.text("Updated at: " + str(prompt[5]))
        st.write("---")

#enter information
# Store the initial value of widgets in session state
title = st.text_input('title', 'enter title here')

txt = st.text_area(
    "Enter the prompt",
    "you can enter the prompt here",
    )


#search function
def main():
    st.title("Prompt Viewer")
    search_term = st.text_input("Search for prompts by title:")
    sort_by = st.selectbox("Sort by:", options=['created_at', 'updated_at'], index=0)
    sort_order = st.radio("Sort order:", options=['asc', 'desc'], index=1)

    con, cur = setup_database()
    prompts = display_prompts(cur, search_term, sort_by, sort_order)
    
    for prompt in prompts:
        st.subheader(prompt[1])  # Title
        st.write(prompt[2])  # Prompt
        st.write("Favorite:", prompt[3])  # is_favorite
        st.text("Created at: " + str(prompt[4]))
        st.text("Updated at: " + str(prompt[5]))
        st.write("---")

if __name__ == "__main__":
    main()


    # TODO: Add a sort by date
    # TODO: Add favorite button





