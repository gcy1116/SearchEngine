import sqlite3
import streamlit as st

# cur.execute('CREATE TABLE IF NOT EXISTS Counts (count INTEGER)')
# table name: Counts
# column name: count
def count_main():
    conn = sqlite3.connect('count.db')
    c = conn.cursor()

    c.execute('SELECT * FROM Counts')
    count = c.fetchone()
    if count is None:
        count = 0
    else:
        count = count[0]
    count += 1
    c.execute('DELETE FROM Counts')
    c.execute('INSERT INTO Counts VALUES (?)', (count,))
    conn.commit()
    conn.close()
    return count

def create_table():
    conn = sqlite3.connect('count.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Counts (count INTEGER)')
    conn.commit()
    conn.close()

# 测试
if __name__ == '__main__':
    cur.execute('CREATE TABLE IF NOT EXISTS Counts (count INTEGER)')
    # 这里没写删除数据库和数据库数据的函数，应跟 QnA_db.py类似
    st.title("Count_Test")
    st.write("This is a test of the count function")
    st.sidebar.title("Count_Test")
    st.sidebar.write("This is a test of the count function😋")
    count_main()
