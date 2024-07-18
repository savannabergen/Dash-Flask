from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask import Flask, render_template, send_from_directory, url_for, redirect
from PIL import Image
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from dash import Dash, html, dcc
import dash
import plotly.express as px

app = Flask(__name__)
 # Learn Where to Hide this
app.secret_key = b'_53oi3uriq9pifpff;apl'
# Define Uploads Folder
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'
# ALLOWED_EXTENSIONS
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Process Image
def process_image(filename, operation):
    image1 = Image.open(f"static/{filename}")
    match operation:
        case "jpg":
            new_file_name = f"static/{filename.split('.')[0] + '.jpg'}"
            image1.save(new_file_name, 'jpeg')
            return new_file_name
        case "png":
            new_file_name = f"static/{filename.split('.')[0] + '.png'}"
            image1.save(new_file_name, 'png')
            return new_file_name
        case "gray": 
            converted_image = image1.convert("L")
            new_file_name = f"static/{filename.split('.')[0] + 'gray.jpg'}"
            converted_image.save(new_file_name, 'jpeg')
            return new_file_name             

# Route Decorator To Index
@app.route('/')
def index():
    h1 = "Instructions"
    page = "Test"
    return render_template("index.html", h1=h1, page=page)

# Configure Flask Form
class Form(FlaskForm):
    img = FileField(validators=[
        FileAllowed(photos, 'Only Images Are Allowed'),
        FileRequired('File Field Should Not Be Empty')
    ])
    operation = SelectField('Project',
                           choices=['jpg', 'png', 'gray'])
    submit = SubmitField("Submit")

# Pillow Upload
@app.route('/uploads/<filename>') 
def get_files(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)
   
# Route Decorator To Pillow
@app.route('/convert', methods=['GET', 'POST'])
def upload():
    h1 = "Welcome to the Pillow App"
    paragraph = "Pillow is a Python Library"
    form = Form()
    if form.validate_on_submit():
        filename = photos.save(form.img.data)
        operation = form.operation.data
        file_url = url_for('get_files', filename=filename)
        new_image = process_image(file_url, operation)
        return f'Your File Is Available <a href={new_image}>Here</a>'
    else: 
        file_url = None
        new_image = None      
    return render_template('convert.html', form=form, h1=h1, paragraph=paragraph, file_url=file_url, new_image=new_image)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)