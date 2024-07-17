# Voice Cloning and Text-to-Speech Web Application

This project is a web application that records your voice, clones it, and uses the cloned voice to read a paragraph of text aloud. The application is built using FastAPI and integrates Dropbox for file storage and Modelslab API for voice cloning and text-to-speech conversion.

## Features

- Record voice from the browser
- Upload recorded voice to Dropbox
- Clone the recorded voice
- Generate text-to-speech audio using the cloned voice

## Technologies Used

- FastAPI
- Dropbox API
- Modelslab API
- Pydub
- Requests
- Jinja2
- HTML/CSS
- JavaScript

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/siddharth-k03/Voice_Clone.git
    cd your-repository-name
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following variables:

    ```env
    DROPBOX_ACCESS_TOKEN=your-dropbox-access-token
    MODELSLAB_API_KEY=your-modelslab-api-key
    ```

5. **Run the application:**

    ```bash
    uvicorn server:app --reload
    ```

6. **Access the application:**

    Open your browser and navigate to `http://localhost:8000`

## Usage

1. Click "Start Recording" to record your voice.
2. Read the displayed script aloud.
3. Click "Stop Recording" to stop and upload the audio.
4. A small recording of the cloned voice will be made available once processing is complete.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Dropbox API](https://www.dropbox.com/developers/documentation)
- [Modelslab API](https://modelslab.com/docs)
- [Pydub](https://pydub.com/)
