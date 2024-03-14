import React from 'react';
import { css } from '@emotion/react';
import UploadButtons from '../components/UploadButtons';

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
  // Callback function to handle uploaded image data
  const handleUploadComplete = (imageUrl) => {
    // Perform further processing with the uploaded image data (e.g., OCR, translation)
    console.log('Uploaded image URL:', imageUrl);
    // Add your logic for further processing here
  };

  return (
    <div css={[HomePageStyle]}>
      <h1 className="title">Image Translator App</h1>

      <div className="description">
        <p>Welcome to the Image Translator App! Upload an image, perform OCR, translate text, and view the results.</p>
      </div>

      <div className="instructions">
        <h2>Instructions:</h2>
        <ol>
          <li>Click the "Upload Image" button to select an image.</li>
          <li>Perform OCR to extract text from the image.</li>
          <li>Translate the extracted text using the OpenAI API.</li>
          <li>View the translated text overlaid on the image.</li>
        </ol>
      </div>

      {/* Pass the onUploadComplete callback to the UploadButtons component */}
      <UploadButtons onUploadComplete={handleUploadComplete} />

      {/* Add more sections or components as needed */}
    </div>
  );
};

export default HomePage;
