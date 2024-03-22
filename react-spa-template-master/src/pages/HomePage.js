import React, { useState } from 'react';
import { css } from '@emotion/react';
import UploadButtons from '../components/UploadButtons';
import FileUpload from '../components/FileUpload'; // Import the FileUpload component

const HomePageStyle = css`
  h1 {
    font-size: 4rem;
    font-weight: 600;
    text-align: center;
  }

  .description {
    margin: 20px 0;
    text-align: center;
  }

  .instructions {
    margin: 30px 0;
  }

  .footer {
    margin-top: 40px;
    text-align: center;
  }
  rect.btn {
    stroke: #fff;
    fill: #fff;
    fill-opacity: 0;
    stroke-opacity: 0;
  }
`;

const HomePage = () => {
  const [selectedLanguage, setSelectedLanguage] = useState('en'); // Default language: English
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null); // State to store uploaded image URL

  // Callback function to handle uploaded image data
  const handleUploadComplete = (imageUrl) => {
    // Perform further processing with the uploaded image data (e.g., OCR, translation)
    console.log('Uploaded image URL:', imageUrl);
    // Update the state with the uploaded image URL
    setUploadedImageUrl(imageUrl);
    // Add your logic for further processing here
  };

  // Function to handle language selection
  const handleLanguageChange = (event) => {
    setSelectedLanguage(event.target.value);
  };

  // Function to handle selected files from FileUpload component
  const handleFilesSelected = (files) => {
    // Process the selected files here (e.g., recursively process images)
    console.log('Selected files:', files);
  };

  return (
    <div css={[HomePageStyle]}>
      <h1 className="title">Image Translator App</h1>

      <div className="description">
        <p>Welcome to the Image Translator App! Upload an image, perform OCR, translate text, and view the results.</p>
      </div>

      {/* Language Selection Dropdown */}
      <div className="language-selection">
        <label htmlFor="language-select">Language to translate into: </label>
        <select id="language-select" value={selectedLanguage} onChange={handleLanguageChange}>
          <option value="en">English</option>
          <option value="zh">Chinese</option>
          <option value="es">Spanish</option>
          <option value="ja">Japanese</option>
          <option value="th">Thai</option>
          <option value="fr">French</option>
          <option value="de">German</option>
          <option value="it">Italian</option>
          <option value="pt">Portuguese</option>
          {/* Add more language options as needed */}
        </select>
      </div>

      <div className="instructions">
        <h2>Instructions:</h2>
        <ol>
          <li>1. Click the "Upload Image" button to select an image.</li>
          <li>2. Perform OCR to extract text from the image.</li>
          <li>3. Translate the extracted text using the selected language.</li>
          <li>4. View the translated text overlaid on the image.</li>
        </ol>
      </div>

      {/* Display the uploaded image if available */}
      {uploadedImageUrl && (
        <div className="uploaded-image">
          <h3>Uploaded Image:</h3>
          <img src={uploadedImageUrl} alt="Uploaded" />
        </div>
      )}

      {/* Add the FileUpload component */}
      {/* <FileUpload onFilesSelected={handleFilesSelected} /> */}

      {/* Pass the onUploadComplete callback and selectedLanguage to the UploadButtons component */}
      <UploadButtons onUploadComplete={handleUploadComplete} selectedLanguage={selectedLanguage} />

      {/* Add more sections or components as needed */}
    </div>
  );
};

export default HomePage;
