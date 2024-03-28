import React, { useState } from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import axios from 'axios';
import LinearProgress from '@material-ui/core/LinearProgress';
import config from '../config'; // Import the config file

const Input = styled('input')({
  display: 'none',
});

const UploadButtons = ({ onUploadComplete, selectedTranslateToLanguage, selectedOriginalLanguage }) => {
  const [uploadProgress, setUploadProgress] = useState();
  const [error, setError] = useState(null); // State to hold error information

  const handleFileUpload = (event) => {
    const files = event.target.files;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }
    
    formData.append('translated_lang_code', selectedTranslateToLanguage);
    formData.append('original_lang_code', selectedOriginalLanguage);

    axios.post(`${config.development.apiUrl}/upload`, formData, {
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setUploadProgress(percentCompleted);
      },
    })
      .then(response => {
        onUploadComplete(response.data.imageUrl);
        handleProcessImages();
      })
      .catch(error => {
        console.error('Upload failed. Error:', error);
        setError('Failed to upload. Please try again.'); // Set error state with a message
      })
      .finally(() => {
        setUploadProgress(0);
      });
  };

  const handleProcessImages = () => {
    // Assuming the server returns the zip file directly as a downloadable attachment
    axios({
      method: 'GET',
      url: `${config.development.apiUrl}/downloadZip`,
      responseType: 'blob', // Set response type to 'blob' to handle binary data
    })
      .then(response => {
        // Create a blob URL for the zip file
        const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
  
        // Create an anchor element to trigger download
        const downloadLink = document.createElement('a');
        downloadLink.href = blobUrl;
        downloadLink.download = 'translated_images.zip';
        document.body.appendChild(downloadLink);
        downloadLink.click();
  
        // Clean up the blob URL and remove the anchor element
        window.URL.revokeObjectURL(blobUrl);
        document.body.removeChild(downloadLink);

        // Send a command to the server to delete the files
        axios.post(`${config.development.apiUrl}/deleteFiles`)
        .then(response => {
          console.log('Download files successful');
        })
        .catch(error => {
          console.error('Error sending download successful to server:', error);
          // Handle error
        });
      })
      .catch(error => {
        console.error('Error downloading zip file:', error);
        // Handle error
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

      {uploadProgress && <LinearProgress variant="determinate" value={uploadProgress} />}

      {/* Display error message if error state is set */}
      {error && <div>Error: {error}</div>}
    </Stack>
  );
};

export default UploadButtons;
