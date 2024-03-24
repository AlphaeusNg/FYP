import React, { useState } from 'react';
import { css } from '@emotion/react';
import UploadButtons from '../components/UploadButtons';
import axios from 'axios'; // Import axios for making HTTP requests
import config from '../config';
// import FileUpload from '../components/FileUpload'; // Import the FileUpload component

const HomePageStyle = css`
  h1 {
    font-size: 5rem;
    font-weight: 600;
    text-align: center;
    margin-bottom: 40px; /* Add some margin at the bottom */
  }

  .introduction {
    font-size: 2rem; /* Decrease the font size for introduction */
    text-align: center;
    margin-bottom: 15px; /* Add some margin at the bottom */
  }

  .description {
    margin: 20px 0;
    text-align: center;
    font-size: 1.2rem; /* Adjust font size for description */
    line-height: 1.5; /* Increase line height for better readability */
  }

  .language-selection {
    margin: 10px 0;
    text-align: left;
    font-size: 1.1rem; /* Adjust font size for language selection */
  }

  .instructions {
    margin: 30px 0;
    font-size: 1.1rem;
    line-height: 1.3;
  }

  .instructions ol {
    margin-left: 20px; /* Indent the ordered list */
  }

  .uploaded-image {
    margin-top: 30px; /* Add some margin at the top */
  }
`;

const HomePage = () => {
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
  
  const handleUploadComplete = (imageUrl) => {
    setUploadedImageUrl(imageUrl);
  };

  const handleLanguageChange = (event) => {
    setSelectedLanguage(event.target.value);
  };

  return (
    <div css={[HomePageStyle]}>
      <h1 className="title">Image Translator App</h1>

      <h2 className="introduction">Welcome!</h2>

      <div className="description">
        <p>Upload as many images as you want to be translated.</p>
      </div>

      {/* Language Selection Dropdown */}
      <div className="language-selection">
        <label htmlFor="language-select">Select language to translate into: </label>
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
          <li>1. Choose the language to be translated into.</li>
          <li>2. Click the "Upload" button to select your images.</li>
          <li>3. Receive the translated images and enjoy them!</li>
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
