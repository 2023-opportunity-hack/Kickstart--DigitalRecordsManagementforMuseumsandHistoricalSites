from flask import Flask, request, jsonify
import os
import audio_process
import text_process
import image_process
import shutil
app = Flask(__name__)

@app.route('/processFile/<path:file_path>', methods=['GET'])
def process_file(file_path):
    
    SUPPORTED_IMAGE_EXTENSIONS = ['.jpg','.jpeg','.png'] #support for bmp?
    SUPPORTED_AUDIO_EXTENSIONS = ['.mp3','.wav','.mp4']
    SUPPORTED_TEXT_EXTENSIONS = ['.txt','.pdf','.docx','.doc','.rtfs']
    UNSUPPORTED_FORMAT_PATH = "UNSUPPORTED/"
    # Check if the file exists
    if not os.path.isfile(file_path):
        return jsonify({'error': 'Bad file'}), 200
    
    
    # Read the content of the file
    _, file_extension = os.path.splitext(file_path)

    if file_extension in SUPPORTED_IMAGE_EXTENSIONS:
        print("Processing image file")
        output = image_process.image_process(file_path)
        output["file_format"] = file_extension
        return jsonify(output)  


    elif file_extension in SUPPORTED_AUDIO_EXTENSIONS:
        print("Processing audio file")
        output = image_process.image_process(file_path)
        output["file_format"] = file_extension
        return jsonify(output)  

    elif file_extension in SUPPORTED_TEXT_EXTENSIONS:
        print("Processing text file")
        output = text_process.text_process(file_path)
        
        output["tags"] = output["tags"].append("Text File")
        output["tags"] = output["tags"].append("Document")

        if file_extension == ".pdf":
            output["tags"] = output["tags"].append("pdf file")

        output["file_format"] = file_extension
        return jsonify(output)  
     
    else:
        print("ERROR: **Unknown file format**")
        if not (os.path.exists(UNSUPPORTED_FORMAT_PATH)):
            os.mkdir(UNSUPPORTED_FORMAT_PATH)

        try:
        # Move the file to the destination directory
            shutil.move(file_path, UNSUPPORTED_FORMAT_PATH)
            print(f"File '{file_path}' moved to '{UNSUPPORTED_FORMAT_PATH}'")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    app.run(debug=True)