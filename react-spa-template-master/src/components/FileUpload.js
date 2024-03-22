// FileUpload.js
// Doesn't work for now
import React from 'react';
import { useDropzone } from 'react-dropzone';

const FileUpload = ({ onFilesSelected }) => {
  const onDrop = (acceptedFiles) => {
    // Pass the accepted files to the parent component
    onFilesSelected(acceptedFiles);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div {...getRootProps()} style={{ border: '2px dashed #eee', padding: '20px', textAlign: 'center' }}>
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop the files here ...</p>
      ) : (
        <p>Drag 'n' drop some files here, or click to select files</p>
      )}
    </div>
  );
};

export default FileUpload;
