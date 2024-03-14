import React, { useState } from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import PhotoCamera from '@mui/icons-material/PhotoCamera';
import Stack from '@mui/material/Stack';
import axios from 'axios';
import LinearProgress from '@material-ui/core/LinearProgress';

const Input = styled('input')({
  display: 'none',
});

const UploadButtons = ({ onUploadComplete }) => {
  debugger;
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileUpload = (event) => {
    console.log('handleFileUpload function called');
    const files = event.target.files;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('file', files[i]);  // Use the same key 'file' for each file
    }

    axios.post('http://127.0.0.1:5000/upload', formData, {
      onUploadProgress: (progressEvent) => {
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
      });

      console.log('File upload finished'); // Log after axios.post request
  };

  return (
    <Stack direction="row" alignItems="center" spacing={2}>
      <label htmlFor="contained-button-file">
        <Input accept="image/*" id="contained-button-file" multiple={true} type="file" onChange={handleFileUpload} />
        <Button variant="contained" component="span">
          Upload
        </Button>
      </label>
      {/* <label htmlFor="icon-button-file">
        <Input accept="image/*" id="icon-button-file" type="file" onChange={handleFileUpload} />
        <IconButton color="primary" aria-label="upload picture" component="span">
          <PhotoCamera />
        </IconButton>
      </label> */}

      {/* Include the progress bar where you want it to appear */}
      <LinearProgress variant="determinate" value={uploadProgress} />
    </Stack>
  );
};

export default UploadButtons;
