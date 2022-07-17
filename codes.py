from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date, datetime, timedelta
import altair as alt
import streamlit as st
import lists
import matplotlib.pyplot as plt

st.write("""
# Stock Analysis
""")
ids = st.text_input('Enter the ID', 'MRF')

st.write('You selected:', ids)
new = pd.DataFrame.from_dict(lists.Dict,orient='index',columns=['ID-Firm'])
agree = st.checkbox('Click here to see the available ID')
if agree:
   st.dataframe(new)



url = "https://www.moneycontrol.com/stocks/hist_stock_result.php?ex=B&sc_id=" +ids+"&mycomp="+lists.Dict[ids]

today = datetime.now() 
last_date= today-timedelta(31)
last_day = int(last_date.strftime("%d"))
last_month = int(last_date.strftime("%m"))
last_year = int(last_date.strftime("%Y"))
today_day = int(today.strftime("%d"))
today_month = int(today.strftime("%m"))
today_year = int(today.strftime("%Y"))
today_file = int(today.strftime("%d_%m_%Y"))


datas={}
datas["frm_dy"] = last_day
datas["frm_mth"] = last_month
datas["frm_yr"] = last_year
datas["to_dy"] = today_day
datas["to_mth"] = today_month
datas["to_yr"] = today_year
datas["hdn"] = "daily"
send_date=requests.post(url,data=datas)
soup=BeautifulSoup(send_date.text,"html.parser")
table = soup.find('table', attrs={'class': 'tblchart'})
list1=[ ]
dic={ }
str1 = ""
for j in table.find_all('th'):
    str1= j.text
    list1.append(str1)
dic['items']=list1
k=0
list2=[ ]
for i in table.find_all('tr'):
    str2=''
    for j in i.find_all('td'):
        str2= j.text
        list2.append(str2)
    dic[f"items{k}"]=list2
    k+=1
    str2=''
    list2=[ ]
df=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dic.items() ]))
df2=df.drop('items0', inplace=True, axis=1)
df2=df.drop('items1', inplace=True, axis=1)
df2=df.transpose()   
df2.drop(7,inplace=True,axis=1)
df2.drop(8,inplace=True,axis=1)
df2.columns = df2.iloc[0] 
df2 = df2[1:]
#df2.set_index("Date", inplace=True)
#df2.to_csv(f"scrape_{today_file}.csv",index=True,header=True)
def convert_df(df2):
     return df2.to_csv().encode('utf-8')
csv = convert_df(df2)
st.write(f"""
# {lists.Dict[ids]} Last 30 days Stock Analysis
""")
st.subheader('Download last 30 day file')
st.download_button(
      "Press to Download",
      csv,
      "file.csv",
      "text/csv",
      key='download-csv'
      )
# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
df2['Volume'] = df2['Volume'].astype('int')
df2['High'] = df2['High'].astype('int')
st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.table(df2)
#hist = alt.Chart(df2).mark_line().encode(x = 'Date',y=alt.Y('Volume', sort='y'))
fig = plt.figure(figsize = (10, 5))
plt.plot(df2.Date, df2.Volume)
plt.xlabel("Date")  # add X-axis label
plt.ylabel("Volume")  # add Y-axis label
plt.xticks(rotation = 90)
plt.title("Stock Volume")  # add title
st.subheader('Trend Analysis: Stock Volume')
st.pyplot(fig)
#st.altair_chart(hist,use_container_width=True)

hist1 = alt.Chart(df2).mark_line().encode(x = 'Date',
                                             y = 'High')
st.subheader('Trend Analysis: Stock Highest Price')
st.altair_chart(hist1,use_container_width=True)

