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
        );
        """
    )
    con.commit()
    return con, cur

def save_prompt(con, cur, title, prompt):
    cur.execute(
        "INSERT INTO prompts (title, prompt) VALUES (%s, %s)",
        (title, prompt)
    )
    con.commit()

def search_prompts(cur, search_term, filter_date=None):
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

def delete_prompt(con, cur, prompt_id):
    cur.execute("DELETE FROM prompts WHERE id = %s", (prompt_id,))
    con.commit()

def update_prompt(con, cur, prompt_id, new_title, new_prompt):
    cur.execute(
        "UPDATE prompts SET title = %s, prompt = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
        (new_title, new_prompt, prompt_id)
    )
    con.commit()

def toggle_favorite(con, cur, prompt_id):
    cur.execute(
        "UPDATE prompts SET is_favorite = NOT is_favorite WHERE id = %s",
        (prompt_id,)
    )
    con.commit()


def main():
    st.title("Promptbase")
    con, cur = setup_database()

    # Input form for new prompts
    with st.form(key='prompt_form'):
        title = st.text_input("Title")
        prompt_text = st.text_area("Prompt")
        submit_button = st.form_submit_button(label='Save Prompt')
    if submit_button:
        save_prompt(con, cur, title, prompt_text)
        st.success("Prompt saved successfully!")

    # Filters for all prompts
    st.subheader("All Saved Prompts")
    filter_date = st.date_input("Filter prompts by date:")
    search_term_history = st.text_input("Search prompts by title or content:")

    # Button to apply filters
    if st.button('Apply Filters'):
        all_prompts = search_prompts(cur, search_term_history, filter_date)
    else:
        all_prompts = search_prompts(cur, "", None)  # No filters applied initially
    

    for result in all_prompts:
        st.markdown(f"**{result[1]}**")  # Title
        st.write(result[2])  # Prompt text
        edit = st.button('Edit', key=f'edit_history{result[0]}')
        delete = st.button('Delete', key=f'delete_history{result[0]}')
        fav_text = 'Unmark as Favorite' if result[3] else 'Mark as Favorite'
        fav = st.button(fav_text, key=f'fav_history{result[0]}')


        if delete:
            delete_prompt(con, cur, result[0])
            st.success("Prompt deleted successfully!")
            st.experimental_rerun()

        if edit:
            with st.form(key=f'edit_form_history{result[0]}'):
                new_title = st.text_input("New Title", value=result[1], key=f'new_title_history{result[0]}')
                new_prompt = st.text_area("New Prompt", value=result[2], key=f'new_prompt_history{result[0]}')
                update_button = st.form_submit_button('Update Prompt')
            if update_button:
                update_prompt(con, cur, result[0], new_title, new_prompt)
                st.success("Prompt updated successfully!")
                st.experimental_rerun()

        if fav:
            toggle_favorite(con, cur, result[0])
            st.success(f"Prompt marked as {'favorite' if not result[3] else 'not favorite'}!")
            st.experimental_rerun()
        st.write("---")

if __name__ == "__main__":
    main()