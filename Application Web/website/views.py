from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Image
from . import db
import json
from PIL import Image as im
import face_recognition
views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        file = request.files['file']
        pic=im.open(file)
        img = face_recognition.load_image_file(file)
        unknown_face_encodings = face_recognition.face_encodings(img)
        if file and  allowed_file(file.filename):
            if len(unknown_face_encodings) > 0:
                image_data = pic.tobytes()
                new_image = Image(data=image_data, user_id=current_user.id)  #providing the schema for the note 
    
                db.session.add(new_image) #adding the note to the database 
                db.session.commit()
                flash('image added!', category='success')
            else:
                flash('image not valid',category='error')
        else:
            flash('invalid image file',category='error')
    return render_template("home.html", user=current_user)


@views.route('/delete-image', methods=['POST'])
def delete_image():  
    image = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    imageId = image['imageId']
    image = Image.query.get(imageId)
    if image:
        if image.user_id == current_user.id:
            db.session.delete(image)
            db.session.commit()

    return jsonify({})
