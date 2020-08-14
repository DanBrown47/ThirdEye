#!/usr/bin/python
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import hashlib
import sqlite3 as db
from PIL import Image, ImageEnhance
import cv2 as cv
import io
import os
# from databse as import_image
parent_path = './assets'

# Security
# passlib,hashlib,bcrypt,scrypt

connection_cred = db.connect('./database/credentials.db')
cur_cred = connection_cred.cursor()

connection = db.connect('./database/images.db')
cursor = connection.cursor()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

def create_table(table):
    cursor_image.execute('CREATE TABLE IF NOT EXISTS ? (name TEXT, data BLOB)',(table))


def create_usertable():
    cur_cred.execute('CREATE TABLE IF NOT EXISTS credentials(username TEXT,password TEXT)'
                     )


def add_userdata(username, password):
    cur_cred.execute('INSERT INTO credentials(username,password) VALUES (?,?)'
                     , (username, password))
    connection_cred.commit()


def login_user(username, password):
    cur_cred.execute('SELECT * FROM credentials WHERE username =? AND password = ?'
                     , (username, password))
    data = cur_cred.fetchall()
    return data


def view_all_users():
    cur_cred.execute('SELECT * FROM credentials')
    data = cur_cred.fetchall()
    return data

def add_image(name, length):
    with open('{}/{}/{}.png'.format(parent_path, name, length), 'rb') as f:
        m = f.read()
    # print(m)
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS {} (name TEXT, data BLOB)""".format(name))

    sql = """INSERT INTO {} (name, data ) VALUES (?,?)""".format(name)

    cursor.execute(sql, (length, m))

    connection.commit()
    cursor.close()
    connection.close()



    
def about_us():
    st.header("About us")
    
    html = """
    <div style="display:flex; flex-direction: row; justify-content: flex-start;  flex-flow:row wrap; width:150%">
    <a href="https://aniket-mishra.github.io/">
    <center>
    <div style="width:180px; height:200px; border-color:grey; border-width:medium; border-style:solid; margin:5px">
    <div style="width:150px; height:200px; padding:10px 0px; ">
    <img src="https://avatars3.githubusercontent.com/u/38854722?s=400&u=a9ed062f6b6afd3a35029f2c71ae30c60d12dad2&v=4" width="100" height="100">
    <div style="width:150px; height:200px; padding:10px;">
    <p style="color:black; margin-bottom: 0px;">
    <b >Aniket Mishra</b></p>
    <p style="color:#505050">
    Backend 
    </p>
    </div>
    </div>
    </div>
    </center>
    </a>


    <a href=" https://www.linkedin.com/in/danwand">
    <center>
    <div style="width:180px; height:200px; border-color:grey; border-width:medium; border-style:solid; margin:5px">
    <div style="width:150px; height:200px; padding:10px 0px; ">
    <img src="https://avatars2.githubusercontent.com/u/45515141?s=400&u=893b908d94b8941164104c6a5c8a3a195192058b&v=4" width="100" height="100">
     <div style="width:150px; height:200px; padding:10px 0px;">
    <p style="color:black; margin-bottom: 0px;">
    <b>Danwand</b></p>
    <p style="color:#505050">
    Backend 
    </p>
    </div>
    </div>
    </div>
    </center>
    </a>


    <a href="https://www.linkedin.com/in/dhanush-p-n-b963261b4">
    <center>
    <div style="width:180px; height:200px; border-color:grey; border-width:medium; border-style:solid; margin:5px">
    <div style="width:150px; height:200px; padding:10px 0px; ">
    <img src="https://avatars0.githubusercontent.com/u/34603898?s=400&u=00a484a7158be6d9884eecad79703e0d0881f599&v=4" width="100" height="100">
     <div style="width:150px; height:200px; padding:10px 0px;">
    <p style="color:black; margin-bottom: 0px;">
    <b>Dhanush P N</b></p>
     <p style="color:#505050">
     Backend
     </p>
    </div>
    </div>
    </div>
    </center>
    </a>


    <a href="https://www.linkedin.com/in/nirmal-george-mathew-170b62177/">
    <center>
    <div style="width:180px; height:200px; border-color:grey; border-width:medium; border-style:solid; margin:5px">
    <div style="width:180px; height:200px; padding:10px;">
    <img src="https://avatars3.githubusercontent.com/u/45124414?s=400&u=7482f83eaf5e4bed2ba80be97f483209950dab19&v=4" width="100" height="100">
    <div style="width:150px; height:200px; padding:10px 0px; text-align:center">
     <p style="color:black; margin-bottom: 0px; ">
        <b>Nirmal George Mathew</b></p>
      <p style="color:#505050 ">
     Frontend
     </p>
    </div>
    </div>
    </div>
    </center>
    </a>


    <a href="https://www.swaaz.me/">
    <center>
    <div style="width: 180px; height: 200px;border-color: grey;border-width: medium;border-style: solid;margin-top: 5px;margin-left: 5px;margin-right: 5px;margin-bottom: 5px;">
    <div style="width:150px; height:200px; padding:10px 0px;">
    <img src="https://avatars1.githubusercontent.com/u/42874695?s=400&u=5270b0013aa377093ddd4e4ba44a7723102621b8&v=4" width="100" height="100">
     <div style="width:150px; height:200px; padding:10px 0px;">
    <p style="color:black; margin-bottom: 0px; text-align:center ">
    <b>Swasthik Shetty</b></p>
    <p style="color:#505050; text-align:center">
    Frontend|Integration
     </p>
      </div>
       </div>
        </div>
     </center>
     </a>
    
    </div> 
    """
    st.subheader('Team members')
    st.markdown(html, unsafe_allow_html = True)

def documentation():
    html = """

    <div style="width:940px; border-color:grey; border-width:medium; margin:5px">
    <h2 style="text-align:center"> <b>THIRD EYE</b> - THREAT DETECTION SYSTEM </h3>
    <br>
    <br>

    <p style="text-align:left"><b>PROBLEM STATEMENT</b><p>
    <p style="text-align:left">
      The system is built for net security of the society and citizens.
    The current system is based on manual identification of criminals, which cannot be taken in a much effective way as humans can have limitations on processing multiple points of identification including face, facial features, visible marks, skin colour and so forth.
    Apart from criminals, convicts and runaways or kidnapping are becoming frequent this system can aid future policing in a more desirable and satisfactory way. Technological advancement can aid this system. With the cooperation of both Human Intelligence and Artificial Intelligence, society can be ordered more peacefully and crime rates might reduce significantly.
    </p>

    <p style="text-align:left"><b>PROBLEM SCOPE</b></p>
    <p style="text-align:left">
    The National Crime bureau suggests 63% of violent crimes are committed by just 1 % of the population.
    The purpose of the project is to Identify the convicts or run away peoples. This system is designed to fit into relatively small equipment which can be installed on public places and places people gather which can keep track of the peoples and innocent people data is not stored keeping privacy of common people intact. This can also aid in hospitals and private companies to ensure security. The project scope can again be extended to finding peoples after committing a crime.
    </p>

    <h3>PRODUCT OR SYSTEM FEATURES AND REQUIREMENTS</h3>
    <p style="text-align:left">
     <h4> System Features</h4>
       <li>Fast image recognition using a robust algorithm gone under public scrutiny 
        <li>Multiple face detection 
        <li>Extensible structure and result exported in CSV
        <li>Tested on IoT Ready Devices
        <li>Simple UI control

      <h4>System Requirements | Recommended (IoT)

       <li>CPU  -  Quad-core ARM A57 or above
        <li>GPU -  128 Core GPU Tested on Maxwell Architecture
        <li>RAM -  4 GB 64bit LPDDR4
        
    </p>
    <p>
    <h4>STANDARDS FOLLOWED</h4>
    <li>All code are well documented
    <li>All code can be traced back to author and version controlled
    <li>Modern coding conventions followed
    <li>Globals are not  used
    <li>Well Intended code

    <center>
    <h5 > Made with care, by team <b style="color:red"> Hugs for Bugs</b>



    </div>
    """
    st.subheader('Documentation')
    st.markdown(html, unsafe_allow_html = True)
   

def import_image():
    name = st.text_input('enter name of the person')
    st.set_option('deprecation.showfileUploaderEncoding', False)

    image_file = st.file_uploader('Upload Image', type=['jpg', 'png', 'jpeg'])

    if image_file is not None:
        input_image = Image.open(image_file)
        st.text('image')
        st.image(input_image)

        try:
            length = len(os.listdir(f'{parent_path}/{name}/')) + 1
            st.write(length)
        except:
            st.text('no file')
            os.mkdir('{}/{}/'.format(parent_path, name))
            length = len(os.listdir(f'{parent_path}/{name}/')) + 1
            st.write(length)

        input_image.save('{}/{}/{}.png'.format(parent_path,name,length ))

        add_image(name, length)
        # cursor_image.execute('CREATE TABLE IF NOT EXISTS {} (name TEXT, data BLOB)'.format(name))
        # st.write(length)
        # with open('./assets/swaaz/1.png' , 'rb') as f:
        #     input_image = f.read()

        # with open('ani.png', 'wb') as f:
        #     f.write(input_image)
            
        # sql = """INSERT INTO {} (name, data ) VALUES (?,?)""".format(name)
        # cursor_image.execute(sql, ('swaaz', input_image))

        
def main():
    """Simple Login App"""

    st.title('Third Eye')

    choice = st.sidebar.selectbox('Menu', ['Documentation' , 'About Us',
                                  'Sign In'])

    if choice == 'About Us':
        st.subheader('Team HUGS for BUGS')
        about_us()
    elif choice == 'Sign In':

        st.subheader('Login Section')

        username = st.text_input('User Name')
        password = st.text_input('Password', type='password')
        if st.checkbox('Login'):

            # if password == '12345':

            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password,
                                hashed_pswd))
            if result:

                st.success('Logged In as {}'.format(username))

                task = st.selectbox('Task', [ 'Upload Image'
                                    , 'Profiles'])
                if task == 'Upload Image':
                    st.subheader('Add Your Post')
                    import_image()

                # elif task == 'Add Credential':

                #     st.subheader('Add Credential')
                #     new_user = st.text_input("Username")
                #     new_password = st.text_input("Password",type='password')

                #     if st.button("Signup"):
                #         create_usertable()
                #         add_userdata(new_user,make_hashes(new_password))
                #         st.success("You have successfully created a valid Account")
                #         st.info("Go to Login Menu to login")

                elif task == 'Profiles':

                    st.subheader('User Profiles')
                    
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result, columns=['Username', 'Password'])
                    st.dataframe(clean_db)
            else:
                st.warning('Incorrect Username/Password')
    elif choice == 'Documentation':
        documentation()
        


if __name__ == '__main__':
    main()
