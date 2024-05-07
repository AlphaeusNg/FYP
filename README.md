# Final Year Project - Image Translation App

An image translator app that auto-translates foreign language images into a language of your choice.
1) Upload your image
2) Call `EasyOCR` to perform text localisation
3) Call `OpenAI`'s GPT model to translate
4) Use `Image` to cover bbox coordinates and dynamically overlays with text
5) Sends back images in a zipped file to client.
6) Wala! Image translated!

## Getting started

### Library dependencies
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
Navigate to the `react-spa-template-master` folder and follow the `README.md` instructions inside to setup.

#### Setting up Flask API

Setup Flask environment variable inside Windows PowerShell
```bash
$env:FLASK_APP = "flask_server.app"
```

Check with this:
```bash
echo $env:FLASK_APP
```

Activate the virtual environment and run it
```bash
.venv\Scripts\activate
cd flask_server
flask run
```

You may need to enable cross-origin requests between your React app and Flask API. Modify the file `FYP\flask_server\app.py`, at line 30: `origins` to configure for your local production address.
```python
CORS(app, origins=['https://localhost:5000', 'https://{insert your hostname}}'])
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

#### Setting up OpenAI API key
1. Visit [OpenAI website](https://platform.openai.com/playground) and get access to an API key.
2. Create a `settings.py` file in `.\language_translation\` and fill in your details as such:
``` python
OPEN_AI_KEY = "YOUR_API_KEY"
```



### Testing File Upload
1. Start both the React development server and the Flask API.
2. Use Postman or send a file upload request from your React app to the Flask API.
3. Verify that the file upload works and CORS headers are properly set.

## To run the app
Once everything has been set up properly. To start the app, simply double click the `run_servers.bat` file. If that doesn't work, you can run these codes below on separate terminals.

### Frontend React
```bash
.venv\Scripts\activate
cd .\react-spa-template-master\
npm start
```

### Backend Flask
```bash
.venv\Scripts\activate
cd .\flask_server\
flask run
```


## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or create a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.