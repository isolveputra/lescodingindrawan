
import streamlit as st, sqlite3, pandas as pd
from streamlit.components.v1 import html

st.set_page_config(page_title="Sistem Akademik",layout="wide")
st.markdown("""
<style>
.stApp{background:#f4f6f9}
h1{color:#1565c0}
div[data-testid="stSidebar"]{background:#1565c0}
div[data-testid="stSidebar"] *{color:white}
</style>
""",unsafe_allow_html=True)
html("<script>console.log('Loaded');</script>",height=0)

conn=sqlite3.connect("akademik.db",check_same_thread=False)
c=conn.cursor()
for q in [
"CREATE TABLE IF NOT EXISTS mahasiswa(id INTEGER PRIMARY KEY AUTOINCREMENT,nim TEXT,nama TEXT,prodi TEXT)",
"CREATE TABLE IF NOT EXISTS dosen(id INTEGER PRIMARY KEY AUTOINCREMENT,nidn TEXT,nama TEXT)",
"CREATE TABLE IF NOT EXISTS matkul(id INTEGER PRIMARY KEY AUTOINCREMENT,kode TEXT,nama TEXT,sks INTEGER)"
]: c.execute(q)
conn.commit()

if "login" not in st.session_state: st.session_state.login=False
if not st.session_state.login:
    st.title("Login Sistem Akademik")
    u=st.text_input("Username")
    p=st.text_input("Password",type="password")
    if st.button("Login"):
        if u=="admin" and p=="admin123":
            st.session_state.login=True; st.rerun()
        else: st.error("Login gagal")
    st.stop()

menu=st.sidebar.selectbox("Menu",["Dashboard","Mahasiswa","Dosen","Mata Kuliah"])
if st.sidebar.button("Logout"):
    st.session_state.login=False; st.rerun()

if menu=="Dashboard":
    st.title("Dashboard")
    a=c.execute("select count(*) from mahasiswa").fetchone()[0]
    b=c.execute("select count(*) from dosen").fetchone()[0]
    d=c.execute("select count(*) from matkul").fetchone()[0]
    c1,c2,c3=st.columns(3)
    c1.metric("Mahasiswa",a); c2.metric("Dosen",b); c3.metric("Matkul",d)

def crud(table,fields):
    st.title(table.title())
    with st.form("f"):
        vals=[st.text_input(f) if f!="sks" else st.number_input("sks",1,6,2) for f in fields]
        if st.form_submit_button("Simpan"):
            q=f"insert into {table}({','.join(fields)}) values({','.join(['?']*len(fields))})"
            c.execute(q,vals); conn.commit(); st.success("Tersimpan"); st.rerun()
    df=pd.read_sql_query(f"select * from {table}",conn)
    st.dataframe(df,use_container_width=True)
    if not df.empty:
        hid=st.number_input("ID Hapus",1,int(df.id.max()),1,key=table)
        if st.button("Hapus",key=table+"h"):
            c.execute(f"delete from {table} where id=?",(hid,)); conn.commit(); st.rerun()

if menu=="Mahasiswa": crud("mahasiswa",["nim","nama","prodi"])
elif menu=="Dosen": crud("dosen",["nidn","nama"])
else: crud("matkul",["kode","nama","sks"])
