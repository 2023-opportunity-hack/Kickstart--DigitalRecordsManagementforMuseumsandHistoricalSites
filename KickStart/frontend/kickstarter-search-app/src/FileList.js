import React from 'react';

function FileList({ files, onFileClick }) {
    return (
        <div>
            <ul>
                {files.map((file, index) => (
                    <li key={index} onClick={() => onFileClick(file)}>
                        {file.filePath}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default FileList;
