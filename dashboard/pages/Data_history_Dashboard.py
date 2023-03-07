import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import time
st.set_page_config(page_title="Drone Dashboard", page_icon=":bar_chart:", layout="wide")
col1, col2, col3 = st.columns([4,1,4])
with col1:
    st.write("")
with col2:
    st.image("/media/nouri/Data/Final_pro/Drone_project/ObjectDetecter/ultralytics/dashboard/LOGONEW.png")
with col3:
    st.write("")
st.markdown("<h1 style='text-align: center; color: Orange;'>Data history Dashboard</h1>", unsafe_allow_html=True)


def get_data():
    with open(filename, "r") as f:
            df= pd.read_csv(f,index_col=False,header=0)      
    df.columns = ['Date_time','Time_frame', 'x', 'y', 'Area', 'Class_name', 'RL', 'FB', 'Error_v', 'UD', 'Error', 'VRL', 'Frame_number', 'WFram', 'HFram']
    df=df.drop(['Time_frame','Class_name','WFram','HFram'], axis=1)
    #df = df[df['Area'] != 0].copy()
    return df


col1, col2, col3 = st.columns([3,1,3])
with col1:
    st.header("Choose you Data :")
    Data_Mode= st.selectbox("Which Type of Object tracking",('Follow Objcet Mode',' Collect Data Mode'))
with col2:    
    st.write("")
with col3:
    st.header("DataFrame Info :")
    if Data_Mode ==' Collect Data Mode' :
        filename= "/media/nouri/Data/Final_pro/Drone_project/ObjectDetecter/ultralytics/database/CSV_DATA_collect_data_mode_SAVE.csv"
        df=get_data()
        my_table = st.dataframe(df.tail(10)) 

    elif Data_Mode =='Follow Objcet Mode' :
        filename = "/media/nouri/Data/Final_pro/Drone_project/ObjectDetecter/ultralytics/database/CSV_DATA_following_mode_SAVE.csv"
        df=get_data()
        my_table = st.dataframe(df.tail(5)) 
    elif  Data_Mode =='':
        pass

placeholder = st.empty() 
st.header("Select the area ```Forward-Backward```range:")
FB_level= st.selectbox("",('All','Far','Green zone','Close'))

if FB_level=='All':
    df_FB_level= df.copy()
elif FB_level=='Far':
    df_FB_level= df[df["FB"] == pd.unique(df["FB"])[0]] 
elif FB_level=='Green zone':
    df_FB_level= df[df["FB"] == pd.unique(df["FB"])[1]] 
elif FB_level=='Close':
    df_FB_level= df[df["FB"] == pd.unique(df["FB"])[2]] 


st.header(" Object movement ```UP & Down``` , ```Vactor Right & Lift``` :")
my_chart3 = st.line_chart(data=df_FB_level,x='Date_time', y=['VRL','UD'])

st.header("The relationship between the ```Drone movement response``` and ```Errors optimization```:")
my_chart3 = st.line_chart(data=df_FB_level,x='Date_time', y=['VRL','Error'])
my_chart3 = st.line_chart(data=df_FB_level,x='Date_time', y=['UD','Error_v'])




    
with placeholder.container():
    st.header("""Vertical and Horizontal ```Errors``` by using ```PID``` control: """)
    fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(15,5))
    chart_1=sns.scatterplot(x='Date_time', y='Error_v', data=df,hue='UD', alpha=0.8,ax=ax[0])#,hue='workingday', color='red'
    chart_2=sns.scatterplot(x='Date_time', y='Error', data=df, hue='VRL', alpha=0.8,ax=ax[1])
    st.pyplot(fig)
        
    
    st.header("The object movement```UD```,```VRL```,```FB``` based on Area:")
    col1, col2, col3 = st.columns([1,8,1])
    with col1:
        st.write("")
    with col2:    
        fig = px.scatter_3d(df, x='VRL', y='UD', z='FB', color='Area')
        st.plotly_chart(fig)
    with col3:
        st.write("")






while False:
    new_row =get_data()
    df = df.append(new_row)
    my_table.add_rows(new_row)
    
    with placeholder.container():
        st.header("""Vertical and Horizontal ```Errors``` by using ```PID``` control: """)
        fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(15,5))
        chart_1=sns.scatterplot(x='Date_time', y='Error_v', data=df,hue='UD', alpha=0.8,ax=ax[0])#,hue='workingday', color='red'
        chart_2=sns.scatterplot(x='Date_time', y='Error', data=df, hue='VRL', alpha=0.8,ax=ax[1])
        st.pyplot(fig)
            
        
        st.header("The object movement```UD```,```VRL```,```FB``` based on Area:")
        col1, col2, col3 = st.columns([1,8,1])
        with col1:
            st.write("")
        with col2:    
            fig = px.scatter_3d(df, x='VRL', y='UD', z='FB', color='Area')
            st.plotly_chart(fig)
        with col3:
            st.write("")
    time.sleep(.01)

 
