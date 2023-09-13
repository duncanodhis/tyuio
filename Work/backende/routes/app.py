from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    try:
        data = request.form  # Assuming the data is being sent as form data

        # ... (rest of your code)

        # Get the uploaded image file
        image_file = request.files.get('image')
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path_on_server = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path_on_server)

        # Return a success response
        return jsonify({"message": "Product updated successfully"})
    except Exception as e:
        # Handle any errors that might occur
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
