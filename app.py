import streamlit as st
import psycopg2
from dotenv import load_dotenv
import os
import datetime
from dataclasses import dataclass

load_dotenv()

@dataclass
class Prompt:
    title: str
    prompt: str
    is_favorite: bool
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

def setup_database():
    try:
        with psycopg2.connect(os.getenv("DATABASE_URL")) as con:
            with con.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS prompts (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        prompt TEXT NOT NULL,
                        is_favorite BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """
                )
                con.commit()
    except psycopg2.OperationalError as e:
        st.error("Unable to connect to the database. Please check the connection settings.")
        st.stop()

def save_prompt(title, prompt_text):
    try:
        with psycopg2.connect(os.getenv("DATABASE_URL")) as con:
            with con.cursor() as cur:
                cur.execute(
                    "INSERT INTO prompts (title, prompt) VALUES (%s, %s)",
                    (title, prompt_text)
                )
                con.commit()
    except psycopg2.OperationalError as e:
        st.error("Unable to save the prompt to the database. Please try again later.")

def search_prompts(search_term, filter_date=None):
    try:
        with psycopg2.connect(os.getenv("DATABASE_URL")) as con:
            with con.cursor() as cur:
                base_query = """
                    SELECT id, title, prompt, is_favorite, created_at FROM prompts
                    WHERE (title ILIKE %s OR prompt ILIKE %s)
                """
                params = ['%' + search_term + '%', '%' + search_term + '%']

                if filter_date:
                    base_query += " AND DATE(created_at) = DATE(%s)"
                    params.append(filter_date)

                base_query += " ORDER BY created_at DESC"
                cur.execute(base_query, tuple(params))
                return cur.fetchall()
    except psycopg2.OperationalError as e:
        st.error("Unable to retrieve prompts from the database. Please try again later.")
        return []

def delete_prompt(prompt_id):
    try:
        with psycopg2.connect(os.getenv("DATABASE_URL")) as con:
            with con.cursor() as cur:
                cur.execute("DELETE FROM prompts WHERE id = %s", (prompt_id,))
                con.commit()
    except psycopg2.OperationalError as e:
        st.error("Unable to delete the prompt from the database. Please try again later.")

def update_prompt(prompt_id, new_title, new_prompt):
    try:
        with psycopg2.connect(os.getenv("DATABASE_URL")) as con:
            with con.cursor() as cur:
                cur.execute(
                    "UPDATE prompts SET title = %s, prompt = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                    (new_title, new_prompt, prompt_id)
                )
                con.commit()
    except psycopg2.OperationalError as e:
        st.error("Unable to update the prompt in the database. Please try again later.")

def toggle_favorite(prompt_id):
    try:
        with psycopg2.connect(os.getenv("DATABASE_URL")) as con:
            with con.cursor() as cur:
                cur.execute(
                    "UPDATE prompts SET is_favorite = NOT is_favorite WHERE id = %s",
                    (prompt_id,)
                )
                con.commit()
    except psycopg2.OperationalError as e:
        st.error("Unable to toggle the favorite status. Please try again later.")

def main():
    st.title("Promptbase")
    setup_database()

    with st.form(key='prompt_form'):
        title = st.text_input("Title")
        prompt_text = st.text_area("Prompt")
        submit_button = st.form_submit_button(label='Save Prompt')
    if submit_button:
        save_prompt(title, prompt_text)
        st.success("Prompt saved successfully!")

    st.subheader("All Saved Prompts")
    filter_date = st.date_input("Filter prompts by date:")
    search_term_history = st.text_input("Search prompts by title or content:")

    if st.button('Apply Filters'):
        all_prompts = search_prompts(search_term_history, filter_date)
    else:
        all_prompts = search_prompts("", None)

    for result in all_prompts:
        st.markdown(f"**{result[1]}**")
        st.write(result[2])
        edit = st.button('Edit', key=f'edit_history{result[0]}')
        delete = st.button('Delete', key=f'delete_history{result[0]}')
        fav_text = 'Unmark as Favorite' if result[3] else 'Mark as Favorite'
        fav = st.button(fav_text, key=f'fav_history{result[0]}')

        if delete:
            delete_prompt(result[0])
            st.success("Prompt deleted successfully!")
            st.experimental_rerun()

        if edit:
            with st.form(key=f'edit_form_history{result[0]}'):
                new_title = st.text_input("New Title", value=result[1], key=f'new_title_history{result[0]}')
                new_prompt = st.text_area("New Prompt", value=result[2], key=f'new_prompt_history{result[0]}')
                update_button = st.form_submit_button('Update Prompt')
            if update_button:
                update_prompt(result[0], new_title, new_prompt)
                st.success("Prompt updated successfully!")
                st.experimental_rerun()

        if fav:
            toggle_favorite(result[0])
            st.success(f"Prompt marked as {'favorite' if not result[3] else 'not favorite'}!")
            st.experimental_rerun()
        st.write("---")

if __name__ == "__main__":
    main()
