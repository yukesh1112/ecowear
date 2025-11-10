import os
import uuid
from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from query import query
from productrec import give_rec
from classify import classify_image

# --- Configuration ---
# Folder where user images will be saved
UPLOAD_FOLDER = 'uploads'
# Allowed image file extensions for security
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# A secret key is required for sessions to work
SECRET_KEY = 'your-super-secret-key-change-me' # Replace with a long, random string

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'


# --- Helper Function ---
def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- App Routes ---
@app.route('/', methods=["GET", "POST"])
@app.route('/home/', methods=["GET", "POST"]) # Handles both URLs
def home():
    if request.method == 'POST':
        store_name = request.form.get('text')
        # 1. Validate that the store name was entered
        if not store_name:
            flash("Please enter a store name.")
            return redirect(request.url)

        # 2. Validate that a file was included in the request
        if 'file' not in request.files:
            flash('No file part in the request.')
            return redirect(request.url)
        
        file = request.files['file']

        # 3. Validate that a file was actually selected
        if file.filename == '':
            flash('No file selected.')
            return redirect(request.url)

        # 4. Validate that the file has an allowed image type
        if file and allowed_file(file.filename):
            # Generate a unique filename to prevent files from being overwritten
            filename = secure_filename(file.filename)
            unique_filename = str(uuid.uuid4()) + "_" + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Store the unique filepath in the user's session
            session['filepath'] = filepath

            # Evaluate the store's rating
            store_info = query(store_name.upper())
            rating = store_info[0]

            if rating > 3:
                return render_template('rating.html', processed_text=store_name, rating=rating)
            else:
                # Show the rating and recommendation button
                return render_template('classify.html', processed_text=store_name, rating=rating)
        else:
            flash('Invalid file type. Please upload a JPG, JPEG, or PNG image.')
            return redirect(request.url)

    # This runs for a GET request, displaying the main page
    return render_template('home.html')


@app.route('/results/')
def results():
    # Retrieve the filepath from the session for this specific user
    filepath = session.get('filepath', None)

    # Check if the filepath exists and the file is still on the server
    if not filepath or not os.path.exists(filepath):
        flash("Could not find the uploaded image. Please try again.")
        return redirect(url_for('home'))

    # This list must match your new 10-class model in alphabetical order
    classes = ['dress', 'hat', 'longsleeve', 'outwear', 'pants', 'shirt', 'shoes', 'shorts', 'skirt', 't-shirt']
    
    # Attempt to classify the image
    pred_index = classify_image(filepath)
    
    # Check if the classification was successful (did not return None)
    if pred_index is not None:
        item_category = classes[pred_index]
        recommendations = give_rec(item_category, 2)
        
        # Check if any recommendations were found
        if not recommendations or len(recommendations) < 2:
             flash(f"We identified the item as '{item_category}', but couldn't find enough recommendations for it.")
             return redirect(url_for('home'))

        # Unpack recommendations: each item is [Store, Name, Link, Image_URL]
        store1, name1, link1, img1 = recommendations[0]
        store2, name2, link2, img2 = recommendations[1]
        
        return render_template('recommend.html', 
                             item=item_category,
                             store1=store1, name1=name1, link1=link1, img1=img1,
                             store2=store2, name2=name2, link2=link2, img2=img2)
    else:
        # This runs if classify_image() failed for any reason
        flash("Sorry, the image could not be processed. Please try a different image.")
        return redirect(url_for('home'))


# --- Main Execution Block ---
if __name__ == '__main__':
    # Create the 'uploads' folder if it doesn't already exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    # Run the Flask development server
    app.run(debug=True)