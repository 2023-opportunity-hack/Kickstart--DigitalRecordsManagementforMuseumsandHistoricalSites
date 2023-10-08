import React, { useState } from 'react';
import './App.css';
import SearchBar from './SearchBar';
import FileList from './FileList';
import axios from 'axios'; // Import Axios

function App() {
    const [files, setFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);

    const searchFiles = async (query) => {
        try {
            // Replace with your actual API endpoint
            const response = await axios.get(`http://localhost:8080/searchDocumentByQuery?query=${query}`);

            if (response.data && Array.isArray(response.data)) {
                setFiles(response.data);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const openFile = (file) => {
        // Implement the logic to open the file on the local machine.
        // You can use HTML5 File API or other methods depending on the file type.
        console.log(`Opening file: ${file.filePath}`);
    };

    return (
        <div className="App">
            <h1>File Search App</h1>
            <SearchBar onSearch={searchFiles} />
            <FileList files={files} onFileClick={openFile} />
        </div>
    );
}

export default App;
