
from flask import Flask
from instalite.db import db_session,init_db_command
from instalite import views


#factory method
def create_app():
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.cfg')
    app.cli.add_command(init_db_command)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    app.add_url_rule('/register',view_func=views.register,methods=['GET','POST'])
    app.add_url_rule('/login',view_func=views.login,methods=['GET','POST'])
    app.add_url_rule('/',view_func=views.home)
    app.add_url_rule('/uploads/<fname>',view_func=views.uploads)
    app.add_url_rule('/logout',view_func=views.logout)
    app.add_url_rule('/profile',view_func=views.profile)
    app.add_url_rule('/my-post',view_func=views.my_posts)
    app.add_url_rule('/delete-post/<int:post_id>',view_func=views.delete_post)
    app.add_url_rule('/update-profile',view_func=views.update_profile,methods=['GET','POST'])
    app.add_url_rule('/upload-post',view_func=views.uploadPost,methods=['GET','POST'])

    
    return app