import React, { useState } from 'react';

const FileUploader: React.FC<{ onFileUpload: (file: File) => void }> = ({ onFileUpload }) => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setSelectedFile(e.target.files[0]);
        }
    };

    const handleUploadClick = () => {
        if (selectedFile) {
            onFileUpload(selectedFile);
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUploadClick} disabled={!selectedFile}>
                Загрузить файл
            </button>
        </div>
    );
};

export default FileUploader;
