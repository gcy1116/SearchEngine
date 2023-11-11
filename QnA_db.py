import sqlite3
import streamlit as st
import uuid

# table name: Text
# column name: id, question, answer, timestamp
def create_text_db():
    conn = sqlite3.connect('QnA.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS Text (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userID TEXT NOT NULL,
            question TEXT,
            answer TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def generate_user_id():
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = str(uuid.uuid4())

def insert_text_db(userID, question, answer):
    conn = sqlite3.connect('QnA.db')
    c = conn.cursor()
    c.execute('INSERT INTO Text (userID, question, answer) VALUES (?, ?, ?)', (userID, question, answer))
    conn.commit()
    conn.close()

def show_text_db(userID):
    conn = sqlite3.connect('QnA.db')
    c = conn.cursor()
    records = c.execute("SELECT question, answer, timestamp FROM Text WHERE userID = ? ORDER BY timestamp DESC", (userID,)).fetchall()
    for record in records:
        if record[0] != "" and record[1] != "":
            # st.info(f"Q: {record[0]}")
            # st.info(f"A: {record[1]}")
            st.markdown(f"""
                <div style='background-color: rgba(179, 179, 179, 0.2); padding: 10px;'>
                    <i><strong>Q: {record[0]}</strong></i>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background-color: rgba(179, 179, 179, 0.5); padding: 10px;'>
                <i><strong>A</strong></i>: {record[1]}
            </div>
            """, unsafe_allow_html=True)
    
    conn.commit()
    conn.close()

def delete_records_by_user_id(userID):
    conn = sqlite3.connect('QnA.db')
    c = conn.cursor()
    c.execute("DELETE FROM Text WHERE userID = ?", (userID,))
    st.empty()
    conn.commit()
    print(f"Deleted {conn.total_changes} changes.")  # 打印删除的记录数
    conn.close()

def drop_database():
    conn = sqlite3.connect('QnA.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS Text")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    drop_database()
    create_text_db()
    