import React, { useState } from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import axios from 'axios';
import LinearProgress from '@material-ui/core/LinearProgress';

const Input = styled('input')({
  display: 'none',
});

const UploadButtons = ({ onUploadComplete }) => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploading, setUploading] = useState(false); // Track upload state

  const handleFileUpload = (event) => {
    const files = event.target.files;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }

    // Set uploading state to true when uploading starts
    setUploading(true);

    axios.post('http://127.0.0.1:5000/upload', formData, {
      onUploadProgress: (progressEvent) => {
        console.log('Upload progress:', percentCompleted);
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setUploadProgress(percentCompleted);
      },
    })
      .then(response => {
        console.log('Upload successful. Response:', response.data);
        // Call the onUploadComplete callback with the uploaded image data
        onUploadComplete(response.data.imageUrl);
      })
      .catch(error => {
        console.error('Upload failed. Error:', error);
        // handle error here
      })
      .finally(() => {
        // Reset upload progress and uploading state when upload completes
        setUploadProgress(0);
        setUploading(false);
      });
  };

  return (
    <Stack direction="row" alignItems="center" spacing={2}>
      <label htmlFor="contained-button-file">
        <Input accept="image/*" id="contained-button-file" multiple={true} type="file" onChange={handleFileUpload} />
        <Button variant="contained" component="span">
          Upload
        </Button>
      </label>

      {/* Conditionally render the LinearProgress component */}
      {uploading && <LinearProgress variant="determinate" value={uploadProgress} />}
    </Stack>
  );
};

export default UploadButtons;
