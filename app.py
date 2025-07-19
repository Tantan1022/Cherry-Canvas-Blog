from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

posts = []

@app.route('/')
def home():
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']
    image = request.files.get('image')
    
    image_url = None
    if image and image.filename != '':
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(os.path.join('static/uploads', filename))

        image_url = url_for('static', filename='uploads/' + filename)

    posts.insert(0, {
        'title': title,
        'content': content,
        'image_url': image_url
    })
    return redirect(url_for('home'))
@app.route('/delete/<int:post_index>', methods=['POST'])
def delete_post(post_index):
    if 0 <= post_index < len(posts):
        # Optional: remove uploaded image file
        image_url = posts[post_index].get('image_url')
        if image_url:
            image_path = image_url.replace('/static/', 'static/')
            if os.path.exists(image_path):
                os.remove(image_path)
        posts.pop(post_index)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
