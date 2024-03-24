import React, { useState } from 'react';
import { css } from '@emotion/react';
import UploadButtons from '../components/UploadButtons';

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
  const [selectedTranslateToLanguage, setSelectedTranslateToLanguage] = useState('English');
  const [selectedOriginalLanguage, setSelectedOriginalLanguage] = useState('Japanese'); // State for the original language
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
  
  const handleUploadComplete = (imageUrl) => {
    setUploadedImageUrl(imageUrl);
  };

  const handleTranslateToLanguageChange = (event) => {
    setSelectedTranslateToLanguage(event.target.value);
  };
  const handleOriginalLanguageChange = (event) => { // Event handler for original language dropdown
    setSelectedOriginalLanguage(event.target.value);
  };

  return (
    <div css={[HomePageStyle]}>
      <h1 className="title">Image Translator App</h1>

      <h2 className="introduction">Welcome!</h2>

      <div className="description">
        <p>Upload as many images as you want to be translated.</p>
      </div>

      {/* Original Language Selection Dropdown */}
      <div className="language-selection">
        <label htmlFor="original-language-select">Select original language: </label>
        <select id="original-language-select" value={selectedOriginalLanguage} onChange={handleOriginalLanguageChange}>
          <option value="English">English</option>
          <option value="Chinese">Chinese</option>
          <option value="Spanish">Spanish</option>
          <option value="Japanese">Japanese</option>
          <option value="Thai">Thai</option>
          <option value="French">French</option>
          <option value="German">German</option>
          <option value="Italian">Italian</option>
          <option value="Portuguese">Portuguese</option>
          {/* Add more options as needed */}
        </select>
      </div>

      {/* Language Selection Dropdown */}
      <div className="language-selection">
        <label htmlFor="language-select">Select language to translate into: </label>
        <select id="language-select" value={selectedTranslateToLanguage} onChange={handleTranslateToLanguageChange}>
          <option value="English">English</option>
          <option value="Chinese">Chinese</option>
          <option value="Spanish">Spanish</option>
          <option value="Japanese">Japanese</option>
          <option value="Thai">Thai</option>
          <option value="French">French</option>
          <option value="German">German</option>
          <option value="Italian">Italian</option>
          <option value="Portuguese">Portuguese</option>
          {/* Add more language options as needed */}
        </select>
      </div>

      <div className="instructions">
        <h2>Instructions:</h2>
        <ol>
          <li>1. Choose the original language found in the image.</li>
          <li>2. Choose the language to be translated into.</li>
          <li>3. Click the "Upload" button to select your images.</li>
          <li>4. Receive the translated images and enjoy them!</li>
        </ol>
      </div>

      {/* Display the uploaded image if available */}
      {uploadedImageUrl && (
        <div className="uploaded-image">
          <h3>Uploaded Image:</h3>
          <img src={uploadedImageUrl} alt="Uploaded" />
        </div>
      )}

      {/* Pass the onUploadComplete callback and selectedTranslateToLanguage to the UploadButtons component */}
      <UploadButtons 
        onUploadComplete={handleUploadComplete} 
        selectedTranslateToLanguage={selectedTranslateToLanguage} 
        selectedOriginalLanguage={selectedOriginalLanguage} // Pass the selected original language
      />

      {/* Add more sections or components as needed */}
    </div>
  );
};

export default HomePage;
