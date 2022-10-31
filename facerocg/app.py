from unicodedata import name
from cv2 import RETR_CCOMP
import numpy as np
import tensorflow as tf
from flask import Flask,render_template,Response, request,flash,redirect,url_for
import os
import face_recognition
import cv2
from werkzeug.utils import secure_filename


def copy_attr(a, b, include=(), exclude=()):
    # Copy attributes from b to a, options to only include [...] and to exclude [...]
    for k, v in b.__dict__.items():
        if (len(include) and k not in include) or k.startswith('_') or k in exclude:
            continue
        else:
            setattr(a, k, v)

UPLOAD_FOLDER = './static'
TRAIN_PATH = './uploads'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRAIN_PATH']=TRAIN_PATH
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # file.save(os.path.join(app.config['BOUNDED'],filename))
            full_filename = os.path.join("../"+app.config['UPLOAD_FOLDER'],filename)
            # bounded_path = os.path.join("../"+app.config['BOUNDED'],filename)
            # print("-----------"+full_filename+"-------------------")
            filepaht1 = "./static/"+filename
            test = face_recognition.load_image_file(filepaht1)
            test = cv2.cvtColor(test,cv2.COLOR_BGR2RGB)
            testfacLoc = face_recognition.face_locations(test)[0]
            # print(facLoc)
            encodeTest = face_recognition.face_encodings(test)[0]
            l=["rohit","virat","virat","virat"]
            flag=1
            for i,file in enumerate(os.listdir("./uploads")):
                # print(i,file)
                real_path = os.path.join("../"+app.config['TRAIN_PATH'],file)
                path = "./uploads"+"/"+file
                real = face_recognition.load_image_file(path)
                real = cv2.cvtColor(real,cv2.COLOR_BGR2RGB)
                facLoc = face_recognition.face_locations(real)[0]
                encodedImage = face_recognition.face_encodings(real)[0]
                results = face_recognition.compare_faces([encodedImage],encodeTest)
                faceDis = face_recognition.face_distance([encodedImage],encodeTest)
                if(faceDis>0.5 and results):
                    results[0]=False
                if(results[0]==True):
                    flag=0
                    # print("hey i got the image==>"+l[i])
                    img = cv2.imread(filepaht1)
                    cv2.rectangle(img,(testfacLoc[3],testfacLoc[0]),(testfacLoc[1],testfacLoc[2]),(201,54,155),2)
                    cv2.imwrite(filepaht1, img)
                    return render_template("showimage.html", user_image = full_filename,test="Match found",name=l[i])
            # if(flag):
                # print("imaget not found")
            return render_template("showimage.html", user_image = full_filename,test="No match found")
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



if __name__=='__main__':
    app.run(debug=True)