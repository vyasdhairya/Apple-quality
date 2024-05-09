import streamlit as st
import re
import sqlite3 
import pickle
import pandas as pd
import bz2

conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()


menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

if choice=="Home":
    st.markdown(
        """
        <h2 style="color:black">Apple Quality Prediction System</h2>
        <h1>    </h1>
        <p align="justify">
        <b style="color:black">Apple's Quality Prediction System leverages cutting-edge ML models to anticipate defects in production processes, ensuring high-quality products. The Streamlit web app provides an intuitive interface for real-time monitoring and analysis, empowering teams to make data-driven decisions swiftly. This integrated approach enhances efficiency, minimizes waste, and upholds Apple's renowned standards for excellence.</b>
        </p>
        """
        ,unsafe_allow_html=True)

if choice=="SignUp":
    Fname = st.text_input("First Name")
    Lname = st.text_input("Last Name")
    Mname = st.text_input("Mobile Number")
    Email = st.text_input("Email")
    City = st.text_input("City")
    Password = st.text_input("Password",type="password")
    CPassword = st.text_input("Confirm Password",type="password")
    b2=st.button("SignUp")
    if b2:
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if Password==CPassword:
            if (pattern.match(Mname)):
                if re.fullmatch(regex, Email):
                    create_usertable()
                    add_userdata(Fname,Lname,Mname,City,Email,Password,CPassword)
                    st.success("SignUp Success")
                    st.info("Go to Logic Section for Login")
                else:
                    st.warning("Not Valid Email")         
            else:
                st.warning("Not Valid Mobile Number")
        else:
            st.warning("Pass Does Not Match")
    
if choice=="Login":
    Email = st.sidebar.text_input("Email")
    Password = st.sidebar.text_input("Password",type="password")
    b1=st.sidebar.checkbox("Login")
    if b1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            create_usertable()
            if Email=='a@a.com' and Password=='123':
                st.success("Logged In as {}".format("Admin"))
                Email=st.text_input("Delete Email")
                if st.button('Delete'):
                    delete_user(Email)
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                st.dataframe(clean_db)
            else:
                result = login_user(Email,Password)
                if result:
                    st.success("Logged In as {}".format(Email))
                    menu2 = ["K-Nearest Neighbors", "SVM",
                             "Decision Tree", "Random Forest",
                             "Naive Bayes","ExtraTreesClassifier","VotingClassifier"]
                    choice2 = st.selectbox("Select ML",menu2)
                    Size=float(st.slider('Size=', -7.15, 7.15))
                    Weight=float(st.slider('Weight=', -7.15, 7.15)) 
                    Sweetness=float(st.slider('Sweetness=', -7.15, 7.15))
                    Crunchiness=float(st.slider('Crunchiness=', -7.15, 7.15)) 
                    Juiciness=float(st.slider('Juiciness=', -7.15, 7.15))
                    Ripeness=float(st.slider('Ripeness=', -7.15, 7.15))
                    Acidity=float(st.slider('Acidity=', -7.15, 7.15))
                    my_array=[Size, Weight, Sweetness, Crunchiness, 
                              Juiciness, Ripeness, Acidity]
                    
                    b2=st.button("Predict")
                    sfile = bz2.BZ2File('model.pkl', 'rb')
                    model=pickle.load(sfile)
                                           
                    if b2:                        
                        df = pd.DataFrame([my_array], 
                                          columns=['Size', 'Weight', 'Sweetness', 
                                                   'Crunchiness', 'Juiciness', 
                                                   'Ripeness', 'Acidity'])
                        tdata=df.to_numpy()
                        if choice2=="K-Nearest Neighbors":
                            test_prediction = model[0].predict(tdata)
                            query=test_prediction[0]
                            
                        if choice2=="SVM":
                            test_prediction = model[1].predict(tdata)
                            query=test_prediction[0]
                                             
                        if choice2=="Decision Tree":
                            test_prediction = model[2].predict(tdata)
                            query=test_prediction[0]
                            
                        if choice2=="Random Forest":
                            test_prediction = model[3].predict(tdata)
                            query=test_prediction[0]
                            
                        if choice2=="Naive Bayes":
                            test_prediction = model[4].predict(tdata)
                            query=test_prediction[0]
                            
                        if choice2=="ExtraTreesClassifier":
                            test_prediction = model[5].predict(tdata)
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="VotingClassifier":
                            test_prediction = model[6].predict(tdata)
                            query=test_prediction[0]
                        if query=="good":
                            st.success("Apple Quality is "+query)
                        else:
                            st.error("Apple Quality is "+query)
                            
                else:
                    st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")
                
           

            
        

        
