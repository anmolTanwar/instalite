from fileinput import filename
import sqlite3,json
from flask import render_template,redirect,flash,session,current_app,send_from_directory,url_for
from instalite.db import db_session
from instalite.models import Profile,Post
from flask import request,g
from werkzeug.utils import secure_filename
import os
def register():
        if request.method == 'POST':
                uname = request.form['uname']
                email = request.form['email']
                pwd = request.form['pwd']

                profile = Profile(uname,email,pwd)
                try:
                        db_session.add(profile)
                        db_session.commit()
                except Exception as e:
                        flash(message = "Sorry! Email or Username Already Exists!")
                else:
                        flash(message = "Registeration Successfull!")
                        return redirect('login')
        return render_template('register.html')

def login():
        if request.method == 'POST':
                email = request.form['email']
                pwd = request.form['pwd']

                try:
                        profile = db_session.query(Profile).filter(Profile.email==email).first()
                        if profile:
                                if profile.verify_password(pwd):
                                        session['profile'] = [profile.profile_id,profile.username,
                                        profile.email,profile.phone_no,profile.about_me,profile.profile_pic,
                                        profile.profile_date,profile.profile_time]
                                        return redirect('/')
                                else:
                                        flash(message='Invalid Password!')
                        else:
                                flash(message='Invalid Credentials!')
                except Exception as e:
                        pass
        return render_template('login.html')

def logout():
        session.pop('profile',None)
        return redirect('/')

def home():
        postdata = []
        #g.profile_icon = url_for('static',filename='cover.jpg')
        if 'profile' in session:
                posts = db_session.query(Post).order_by(Post.post_time.desc()).order_by(Post.post_date.desc()).all()
                # if 'profile' in session:
                #         # g.profile_icon = session['profile'][5]
                for post in posts:
                        postdata.append(post)
        return render_template('home.html',postdata=postdata)


def profile():
        if 'profile' in session:
                uprofile = session['profile']
                return render_template('profile.html',data=uprofile)
        return redirect(url_for('login'))

def uploads(fname='cover.jpg'):
        return send_from_directory(current_app.config["UPLOAD_FOLDER"], fname)

        
def uploadPost():
        if 'profile' in session:
                if request.method == 'POST':
                        file = request.files['postimg']
                        title = request.form['title']
                        desc = request.form['desc']
                        file_name = secure_filename(file.filename)
                        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),current_app.config['UPLOAD_FOLDER'],file_name).replace('\\','/')
                        post = Post(title,desc,file_name,session['profile'][0],session['profile'][1])
                        try:
                                db_session.add(post)
                                db_session.commit()
                        except:
                                pass
                
                        file.save(file_path)
                        flash('Post Uploaded Successfully')
                return render_template('post.html')
        return redirect('login')

def my_posts():
        postdata = []
        try:
                profile = db_session.query(Profile).filter(Profile.profile_id==session['profile'][0]).one()
                posts = profile.posts
                for post in posts:
                        postdata.append(post)
        except Exception as e:
                pass
        if len(postdata) == 0:
                flash(message='No Post Available')
        return render_template('mypost.html',postdata=postdata)

def delete_post(post_id):
        if 'profile' in session:
                try:
                        db_session.query(Post).filter(Post.post_id == post_id).delete()
                except:
                        pass
                else:
                        db_session.commit()
                        flash('Post deleted Successfully')    
        return redirect(url_for('my_posts'))    

def update_profile():
        if request.method == 'POST':
                if 'fname' in request.files:
                        file = request.files['fname']
                        if not file.filename:
                                file_name = 'cover.jpg'
                                
                        else:
                                file_name = secure_filename(file.filename)
                                file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),current_app.config['UPLOAD_FOLDER'],file_name).replace('\\','/')
                                try:
                                        file.save(file_path)
                                except:
                                        pass
                                
                phone_no = request.form['phone_no']
                desc = request.form['desc']
                profile = db_session.query(Profile).filter(Profile.profile_id == session['profile'][0]).one()
                profile.profile_pic = file_name
                profile.phone_no = phone_no
                profile.about_me = desc
                db_session.commit()
                session['profile'] = [profile.profile_id,profile.username,
                                        profile.email,profile.phone_no,profile.about_me,profile.profile_pic,
                                        profile.profile_date,profile.profile_time]
                uprofile = session['profile']
        return redirect(url_for('profile',data=uprofile))
                        





