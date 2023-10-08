from flask import Flask, request, jsonify
import os
import audio_process
import text_process
import image_process
app = Flask(__name__)

@app.route('/processFile/<path:file_path>', methods=['GET'])
def process_file(file_path):
    
    SUPPORTED_IMAGE_EXTENSIONS = ['.jpg','.jpeg','.png'] #support for bmp?
    SUPPORTED_AUDIO_EXTENSIONS = ['.mp3','.wav']
    SUPPORTED_TEXT_EXTENSIONS = ['.txt','.text','.pdf','.doc','.ppt']
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        return jsonify({'error': 'Bad file'}), 200
    
    # Read the content of the file
    _, file_extension = os.path.splitext(file_path)

    if file_extension in SUPPORTED_IMAGE_EXTENSIONS:
        print("Processing image file")
        image_process.image_process()

    elif file_extension in SUPPORTED_AUDIO_EXTENSIONS:
        print("Processing audio file")
        audio_process.audio_process()

    elif file_extension in SUPPORTED_TEXT_EXTENSIONS:
        print("Processing text file")
        text_process.text_process()

    else:
        print("ERROR: **Unknown file format**")


    
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    
    # Create a JSON response with the file content
    response_data = {'file_path': file_path, 'content': file_content}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)