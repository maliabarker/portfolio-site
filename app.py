from flask import Flask, render_template, request, request_started, session, redirect, url_for, send_file
from flask_pymongo import pymongo
import bcrypt
import os
import dotenv
from bson.objectid import ObjectId

app = Flask(__name__)

# accessing env variables
dotenv.load_dotenv('.env')
password = os.environ.get('PASSWORD')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# connecting to mongodb atlas database
CONNECTION_STRING = f'mongodb+srv://maliabarker:{password}@cluster0.upbvp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_default_database()

### DATABASE COLLECTIONS ###
blog_posts = db.blog_posts
projects = db.projects
users = db.users

### ADMIN ADD ###
# at first load, check if there is a user in the database yet
# if not, add myself as user for admin priviledges
if len(list(users.find())) == 0:
    admin = {
        'email':      'maliabarker@icloud.com',
        'password':   bcrypt.hashpw((password).encode('utf-8'), bcrypt.gensalt())
    }
    users.insert_one(admin)

### ADMIN CHECK FOR LOGIN ###
# helper function that checks if login credentials are the same as user inserted above
# returns user if credentials match or false if they do not
def verify_credentials(user_credentials):
    print('cred', user_credentials)
    user = users.find_one({'email': user_credentials['email']})
    print('user', user)
    if user and bcrypt.checkpw(user_credentials['password'], user['password']):
        return user
    else:
        print('login failed')
        return False

@app.context_processor
def inject_context():
    if 'user' in session.keys():
        return dict(logged_in=True)
    else:
        return dict(logged_in=False)

##### ROUTES! #####
@app.route('/', methods=['GET'])
def index():
    # returns home page
    return render_template('index.html', page_title='home')

@app.route('/about', methods=['GET'])
def about():
    # returns about page
    return render_template('about.html', page_title='about')


####### SKILLS #######
@app.route('/skills', methods=['GET', 'POST'])
def skills():
    # returns skills/projects page
    # able to CRUD projects
    if request.method == 'POST':
        project_type = request.form.get('type')
        project = {
            'path': request.form.get('img_path'),
            'title': request.form.get('title'),
            'stack': request.form.get('stack'),
            'skills': request.form.get('skills'),
            'github': request.form.get('github'),
            'type': project_type
        }
        if project_type == 'ds':
            project['kaggle_link'] = request.form.get('kaggle_link')
        elif project_type == 'live_app':
            project['live_link'] = request.form.get('live_link')

        projects.insert_one(project)

    all_projects = projects.find()

    return render_template('skills.html', page_title='skills', projects=all_projects)

@app.route('/<project_id>/edit_project', methods=['GET', 'POST'])
def edit_project(project_id):
    '''Edit a project'''
    project = projects.find_one({'_id': ObjectId(project_id)})
    return render_template('edit_project.html', project=project)

@app.route('/<project_id>/update_project', methods=['GET', 'POST'])
def update_project(project_id):
    '''Update a project'''
    project_type = request.form.get('type')
    updated_project = {
        'path': request.form.get('img_path'),
        'title': request.form.get('title'),
        'stack': request.form.get('stack'),
        'skills': request.form.get('skills'),
        'github': request.form.get('github'),
        'type': project_type
    }
    if project_type == 'ds':
        updated_project['kaggle_link'] = request.form.get('kaggle_link')
    elif project_type == 'live_app':
        updated_project['live_link'] = request.form.get('live_link')
    projects.update_one (
        {'_id': ObjectId(project_id)},
        {'$set': updated_project}
    )
    all_projects = projects.find()
    return redirect(url_for('skills', page_title='skills', projects=all_projects))

@app.route('/<project_id>/delete_project', methods=['GET', 'POST'])
def delete_project(project_id):
    '''Delete a project'''
    projects.delete_one({'_id': ObjectId(project_id)})
    return redirect(url_for('skills', page_title='skills'))
####### END SKILLS #######


####### BLOG #######
@app.route('/blog', methods=['GET', 'POST'])
def blog():
    # returns blog page
    # able to CRUD blog posts
    if request.method == 'POST':
        post_type = request.form.get('type')
        blog_post = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'link': request.form.get('link'),
            'date': request.form.get('date'),
            'tags': request.form.get('tags'),
            'type': post_type
        }
        if post_type == 'ds':
            blog_post['kaggle_link'] = request.form.get('kaggle_link')
        elif post_type == 'wd':
            blog_post['live_link'] = request.form.get('live_link')

        blog_posts.insert_one(blog_post)

    all_blogposts = blog_posts.find()
    blog_list = list(all_blogposts)

    first_post = blog_list[0]
    all_posts = blog_list[1:]

    return render_template('blog.html', page_title='blog', blog_posts=all_posts, first_post=first_post)

@app.route('/<post_id>/edit_post', methods=['GET', 'POST'])
def edit_post(post_id):
    '''Edit a project'''
    print(post_id)
    post = blog_posts.find_one({'_id': ObjectId(post_id)})
    return render_template('edit_post.html', post=post)

@app.route('/<post_id>/update_post', methods=['GET', 'POST'])
def update_post(post_id):
    '''Update a project'''
    post_type = request.form.get('type')
    updated_post = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'link': request.form.get('link'),
        'date': request.form.get('date'),
        'tags': request.form.get('tags'),
        'type': post_type
    }
    if post_type == 'ds':
        updated_post['kaggle_link'] = request.form.get('kaggle_link')
    elif post_type == 'wd':
        updated_post['live_link'] = request.form.get('live_link')

    blog_posts.update_one (
        {'_id': ObjectId(post_id)},
        {'$set': updated_post}
    )

    return redirect(url_for('blog', page_title='blog'))

@app.route('/<post_id>/delete_post', methods=['GET', 'POST'])
def delete_post(post_id):
    '''Delete a project'''
    blog_posts.delete_one({'_id': ObjectId(post_id)})
    return redirect(url_for('blog', page_title='blog'))




####### END BLOG #######

@app.route('/resume', methods=['GET'])
def resume():
    # returns resume
    return render_template('resume.html', page_title='resume')

@app.route('/download_pdf')
def download_pdf():
    path = "/Users/maliabarker/Desktop/main/MakeSchool/Term3/spring2022-intensive/static/images/2022_resume.pdf"
    return send_file(path, as_attachment=True)

@app.route('/download_docx')
def download_docx():
    print('download button clicked')
    path = "/Users/maliabarker/Desktop/main/MakeSchool/Term3/spring2022-intensive/static/images/2022_resume.docx"
    return send_file(path, as_attachment=True)


@app.route('/admin', methods=['GET', 'POST'])
def login():
    #### ROUTE TO LOG IN AS ADMIN TO CRUD THINGS ####
    if request.method == 'GET':
        # returns log in form
        return render_template('login.html')
    elif request.method == 'POST':
        # logs in user (or not if credentials don't match) and redirects to corresponding page
        user_credentials = {
            'email': request.form.get('email'),
            'password': request.form.get('password').encode('utf-8')
        }
        user = verify_credentials(user_credentials)
        print(user)
        if user != False:
            session['user'] = str(user['_id'])
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
