from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', page_title='home')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', page_title='about')

@app.route('/skills', methods=['GET'])
def skills():
    return render_template('skills.html', page_title='skills')

@app.route('/blog', methods=['GET'])
def blog():
    return render_template('blog.html', page_title='blog')

@app.route('/resume', methods=['GET'])
def resume():
    return render_template('resume.html', page_title='resume')

if __name__ == '__main__':
    app.run(port=5002, debug=True)
