import os
import shutil
import zipfile
import fitz  # PyMuPDF

# save uploaded file to temp dir
def save_uploaded_file(uploaded_file):
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# check status of pdf - encrypted or not
def validate_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        if doc.is_encrypted:
            return True, True, doc
        return True, False, doc
    except Exception as e:
        return False, False, str(e)

# O/P folder setup
def setup_output_dir(filename):
    base_name = os.path.splitext(filename)[0]
    output_dir = os.path.join("downloads", base_name)
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# zip file for images
def create_image_zip(output_dir):
    images_dir = os.path.join(output_dir, "images")
    zip_path = os.path.join(output_dir, "images.zip")
    
    if not os.path.exists(images_dir) or not os.listdir(images_dir):
        return None

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(images_dir):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)
    
    return zip_path

# Assessment Requirement: Resource Management
def cleanup_temp_files(file_path):
    """Removes the temporary uploaded file to save space."""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass