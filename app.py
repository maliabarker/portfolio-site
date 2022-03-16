from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/skills', methods=['GET'])
def skills():
    return render_template('skills.html')

@app.route('/blog', methods=['GET'])
def blog():
    return render_template('blog.html')

@app.route('/resume', methods=['GET'])
def resume():
    return render_template('resume.html')

if __name__ == '__main__':
    app.run(port=5002, debug=True)
