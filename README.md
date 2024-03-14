# Final Year Project - Image Translation App

An image translator app that auto-translates foreign language images into a language of your choice.
1) Upload the image
2) App identifies the text and overlays the image

## Getting started

The following instructions setups a new virtual environment for python and installs the needed libraries.  
These instructions assumes that the user is using a Windows machine.

```bash
python -m venv .venv
.venv\Scripts\activate
```

To install CUDA-supported PyTorch: https://pytorch.org/get-started/locally/
(12.1 in this example)

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Install dependencies from requirements.txt file:
```bash
pip install -r requirements.txt
```

### React-Flask File Upload with CORS Setup Guide
This repository provides a guide to set up the React front-end application with the Flask back-end API.

#### Prerequisites
Before getting started, make sure you have the following installed:
- Node.js and npm (for React)
- Python and pip (for Flask)

#### Setting up React App
Navigate to the `react-spa-template-master` folder
```bash
 cd .\react-spa-template-master\
```
Follow the `README.md` instructions inside to setup.

#### Setting up Flask API
Activate the virtual environment and run it
```bash
.venv\Scripts\activate
python app.py
```

You may need to enable cross-origin requests between your React app and Flask API. Modify the `origins` to configure for your local production address.
```python
CORS(app, origins=['https://localhost:3000', 'https://{insert your hostname}}'])
```

Install `mkcert` with this [guide](https://github.com/FiloSottile/mkcert).

Afterwards, installing it as such will create a local CA certificate and add it to your system's trust store, allowing mkcert to generate valid SSL certificates for local domains.
```bash
mkcert -install
```

Afterwards, navigate to `settings_config` and run this command:
```bash
mkcert -key-file localhost.key -cert-file localhost.crt localhost
```

### Testing File Upload
1. Start both the React development server and the Flask API.
2. Use Postman or send a file upload request from your React app to the Flask API.
3. Verify that the file upload works and CORS headers are properly set.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or create a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.