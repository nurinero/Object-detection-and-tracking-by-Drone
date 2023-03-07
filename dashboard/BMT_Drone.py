from ultralytics import YOLO
import cv2
from PIL import Image
import djitellopy as tello
from datetime import datetime
import time
import numpy as np
import math
import pandas as pd 
import streamlit as st

st.set_page_config(page_title="Drone Dashboard", page_icon=":bar_chart:", layout="wide")
col1, col2, col3 = st.columns([4,1,4])
with col1:
    st.write("")
with col2:
    st.image("/media/nouri/Data/Final_pro/Drone_project/ObjectDetecter/ultralytics/dashboard/LOGONEW.png")
with col3:
    st.write("")
st.markdown("<h1 style='text-align: center; color: Orange;'>Real-Time AutoControl System</h1>", unsafe_allow_html=True)


##### Making a List of the Classes Names from COCO #####
classNames=[]
classFile='/media/nouri/Data/Final_pro/Drone_project/ObjectDetecter/coco.names'
with open(classFile,'rt') as f:
    classNames=f.read().rstrip('\n').split('\n')

##### Loding my Model #####
model = YOLO("/media/nouri/Data/Final_pro/ultralytics/examples/yolov8n.pt") # accepts all formats, 0 for webcam

##### Seting up Tracking  #####
forwordRange=[90000,180000] # Min and Max range to keep the drone win the green zone 
pid=[0.3,0,0.4] # type of controler system by using (trapilshoting and respoins and stpaltiy) PID (proportional integral derivative)
pError=0 #previous horizontal Error of drone movement
pError_v=0 #previous vertical Error of drone movement


#streamlit
st.header("Object Detection:")
col1, col2, col3 = st.columns([2,4,4])
with col1:
    Type_Object=st.selectbox("Select the object type to detect",("Person","Cat","Dog","Pottedplant"))
with col2:
    st.write("")
with col3:
    st.write("")

#Detection and Tracking function
def recogniseObiects(img,info_prev,count):
    results = model.predict(img) # make prediction with (boxes,masks,probs) https://docs.ultralytics.com/predict/
    boxes = results[0].boxes # the the boxes that have info (x,y,xw,yh)& confidence score& classesID 
    myclassesNameList=[]
    myObiectsListCentre=[]
    myObiectsListArea=[] 
    myObiectsListXY=[]
    myObiectsListXWYH=[]
    myObiectsListconf=[]
    CountOneClass=1
    
    for box in boxes:
        # Make a boarding box with the class ID and confidence score for each object in the image based on the setting  score 
        Person=int(box.cls)==0 and float(box.conf)>.6
        Cat=int(box.cls)==15 and float(box.conf)>.6
        Dog=int(box.cls)==16 and float(box.conf)>.6
        Cell_phone=int(box.cls)==67 and float(box.conf)>.5
        Laptop=int(box.cls)==63 and float(box.conf)>.5
        Monitor=int(box.cls)==62 and float(box.conf)>.5
        Pottedplant=int(box.cls)==58 and float(box.conf)>.5
        
        if  Person:# monitor or pottedplant or Cat or Dog or Pottedplant or Cell_phone or Laptop or Monitor:

            xy=int(box.xyxy[0][0]),int(box.xyxy[0][1])
            xwyh=int(box.xyxy[0][2]),int(box.xyxy[0][3])

            CentreX=int(box.xywh[0][0])
            CentreY=int(box.xywh[0][1])
                    
            w=int(box.xywh[0][2])
            h=int(box.xywh[0][3])
            Area=w*h
            # print(f'The boxes.(W,H,Area)is ==>>{w,h,Area}\n\n')
            
            # give every object have the same class a different name in the frame
            if classNames[int(box.cls)] in myclassesNameList: 
                className=classNames[int(box.cls)]+str(CountOneClass)
                myclassesNameList.append(className)
                CountOneClass+=1 
            else:
                className=classNames[int(box.cls)]
                myclassesNameList.append(className)
            
            myObiectsListCentre.append([CentreX,CentreY])
            myObiectsListArea.append(Area)
            myObiectsListXY.append(xy)
            myObiectsListXWYH.append(xwyh)
            myObiectsListconf.append(round(float(box.conf)*100,2))
            
            #cv2.circle(img,(CentreX,CentreY),3,(255,255,255),cv2.FILLED)
            cv2.putText(img,className.upper(),(int(box.xyxy[0][0])+5,int(box.xyxy[0][1])-10),cv2.FONT_HERSHEY_DUPLEX,0.75,(255,225,255),1)
            cv2.putText(img,str(round(float(box.conf)*100,2))+'%',(int(box.xyxy[0][0])+145,int(box.xyxy[0][1])-10),cv2.FONT_HERSHEY_DUPLEX,0.75,(255,225,255),1)
            cv2.rectangle(img,xy,xwyh,color=(255, 255, 255),thickness=2)
            
                            
    if len(myObiectsListArea)!=0: # safety from the bugs when there are no valuess 
        i=myObiectsListArea.index(max(myObiectsListArea))
        
        #myObiectsListArea.sort(reverse=True)        
        return img,[[myObiectsListCentre[i]],[myObiectsListArea[i]],[myclassesNameList[i]],count,myObiectsListXY[i],myObiectsListXWYH[i],myObiectsListconf[i]] #,key #[myFaceListCentre[i],myFaceListArea[i]]
    else:
        return img,[[[0,0]],[0],["0"],count,[0,0],[0,0],[0]]#info_prev#   


# Following the object by controlling the drone movement   
def trackControl(info,wFram,hFram,pid,pError,pError_v,collect_data=False): # w= the w of our img for the drone
    x,y=info[0][0]# 
    area=(info[1][0])
    fb=0 #forward and backward
    error=x-wFram//2
    speed=pid[0]*error+ pid[2]*(error-pError) # control the horizontal value speed when it is close to the object point
    speed=int(np.clip(speed,-32,32))# range our speed 
    
    error_v=y-hFram//2
    speed_v=pid[0]*error_v+ pid[2]*(error_v-pError_v) # control the vertical value speed when it is close to the object point
    speed_v=int(np.clip(speed_v,-70,70))# range our speed 
    
    
    if area >= forwordRange[0] and area <= forwordRange[1]:#forwordRange=[6200,6800] 
        if collect_data==True:
            fb= 0
            rl=-25    
        elif collect_data==False:
            fb= 0
            rl= 0
    elif  area > forwordRange[1]:
        if collect_data==True:
            fb= -30
            rl=int(-speed*0.25)    
        elif collect_data==False:
            fb= -40
            rl=int(-speed*0.25) 
    elif area< forwordRange[0] and area !=0:
        if collect_data==True:
            fb= 30
            rl=int(-speed*0.25)    
        elif collect_data==False:
            fb= 40
            rl=int(-speed*0.25)     
    if x==0 and y==0: 
        error=0
        speed=0
        error_v=0
        speed_v=0
        rl=0    
    
    print (f'speed-H={speed},speed-V={speed_v},forwordspeed{fb}')
    info_movment=[rl,fb,error_v,-speed_v,error,speed]
    me.send_rc_control(rl,fb,-speed_v,speed) # Send the new movement to Draw a circle lift
    return (error,error_v,info_movment)

#colacting data and Imges function
def colacting_data_Imges(img,info,info_movment,wFram,hFram,collect_data=False):
    
    Date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Time_frame=time.time()
    x=info[0][0][0]
    y=info[0][0][1]
    Area=info[1][0]
    Class_name=info[2][0]
    Frame_number=info[3]
    RL=info_movment[0]
    FB=info_movment[1]
    Error_v=info_movment[2]
    UD=info_movment[3]
    Error=info_movment[4]
    VRL=info_movment[5]
    WFram=wFram
    HFram=hFram
    data = {'Date_time':[Date_time],'Time_frame': [Time_frame],'x': [x], 'y': [y], 'Area': [Area], 'Class_name': [Class_name],
            'RL': [RL], 'FB': [FB], 'Error_v': [Error_v], 'UD': [UD], 'Error': [Error], 'VRL': [VRL],
            'Frame_number': [Frame_number],'WFram': [WFram], 'HFram': [HFram]}
    df = pd.DataFrame(data)
    
    if collect_data ==False:
        df.to_csv(f'/media/nouri/Data/Final_pro/Drone_project/ObjectDetecter/ultralytics/database/CSV_DATA_following_mode_SAVE.csv', mode='a', index=False, header=False)
        
        with open("/media/nouri/Data/Final_pro/Drone_project/ObjectDetecter/ultralytics/database/CSV_DATA_following_mode.csv", "w") as f:
            df.to_csv(f, mode='a', index=False, header=True)
    
    elif collect_data ==True :
        df.to_csv(f'/media/nouri/Data/Final_pro/Drone_project/ObjectDetecter/ultralytics/database/CSV_DATA_collect_data_mode_SAVE.csv', mode='a', index=False, header=False)
        
        with open("/media/nouri/Data/Final_pro/Drone_project/ObjectDetecter/ultralytics/database/CSV_DATA_collect_data_mode.csv", "w") as f:
            df.to_csv(f, mode='a', index=False, header=True)
    



collect_data=False 
# collecting data mode True makes you follow and move in a circle around the object and take the Image.
# collecting data mode False makes you follow and keep the object in the middle of the frame.

st.header("Tracking Task:")
col1, col2, col3 = st.columns([2,4,4])
with col1:
    Tracking_Task=st.selectbox("Select your tracking task",("Following Object","Collecting Data"))
    if Tracking_Task =="Following Object":
        collect_data=False
    elif Tracking_Task =="Collecting Data":
        collect_data=True
with col2:
    st.write("")
with col3:
    st.write("")

##### Confg The Drone #####

Run=False 
st.header("Drone Configuration:")
if st.checkbox('Connect and check battery :satellite::battery: :'):
    me = tello.Tello()
    me.connect()
    st.subheader(f'**```The battery life is ```-->> ```{me.get_battery()}% ```**')
    
##Open the Camera from Drone or Webcam  ##
    if st.checkbox('Activate the Streamon :movie_camera: :'):
        me.streamon() #cap =cv2.VideoCapture(1) #or 0
        wFram,hFram= 960,720
        st.subheader('```Detection and Tracking system are actived```')

        if st.checkbox('Activate The takeoff :airplane: :warning: :'):
            
            value=st.slider("Determine the altitude in meter :",min_value=10,max_value=20) 
            st.subheader(f'```Make sure the Drone is in a safe place to take off:```')        
            if st.button("Yes ,take off and run :running: :white_check_mark:", key=None, help=None, on_click=None, args=None, type="secondary", disabled=False):
                Run=True  
                me.takeoff()
                me.send_rc_control(0,0,value,0) # jast to the hight that can detact objactes rl,fb,Dud,Rrl
                time.sleep(1)   
            if st.button("Land and stop :x::x: ", key=None, help=None, on_click=None, args=None, type="secondary", disabled=False):
                me.land()
                Run=False  

FRAME_WINDOW = st.image([])        
    
##### Confg The Drone #####

info_prev=[[[0,0]],[0],["0"],0]
count = 0

while Run:
    print(f'\n\nThe battery live is ==>>{me.get_battery()}\n')
    img_main= me.get_frame_read().frame # Read the one Imge from the Dron #img=cap.read() # Read the one Imge from the Webcam and  #img = cv2.flip(img, 1)
    img_main=cv2.resize(img_main,(wFram,hFram))
    count += 1 # count the frame
    # center_points_cur_frame = []# save center Points from the  current frame
    print(f'info prev is ==>>{info_prev}\n')
    img,info = recogniseObiects(img_main,info_prev,count)
    info_prev=info
    print(f'myFaceListCentre is ==>>{info[0]}\nmyObiectsListArea is ==>>{info[1]}\nmyclassesNameList is ==>>{info[2]}\n')
    # center_points_cur_frame.append(info[0][0])
    
    cv2.circle(img_main,(info[0][0]),3,(42, 219, 151),cv2.FILLED)
    cv2.putText(img_main,info[2][0].upper(),(info[4][0]+5,info[4][1]-10),cv2.FONT_HERSHEY_DUPLEX,0.75,(255,255,255),1)
    cv2.putText(img_main,str(info[6])+'%',(info[4][0]+145,info[4][1]-10),cv2.FONT_HERSHEY_DUPLEX,0.75,(255, 255, 255),1)
    cv2.rectangle(img_main,info[4],info[5],color=(0,255, 255),thickness=2)    
    
    pError,pError_v,info_movment=trackControl(info,wFram,hFram,pid,pError,pError_v,collect_data)
    print(f'pError,pError_v is ==>>{pError,pError_v}\n')
    
    colacting_data_Imges(img_main,info,info_movment,wFram,hFram,collect_data)
    
    #cv2.imshow("Image Track out For", img_main)
    img_main = cv2.cvtColor(img_main, cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(img_main)
        
    cv2.waitKey(1)
    # if cv2.waitKey(1) & 0xFF== ord('q') :
