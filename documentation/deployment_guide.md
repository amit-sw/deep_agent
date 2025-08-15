# Deployment Guide

## Local Development

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd deep_agent
   ```

2. Create and activate a virtual environment:
   ```bash
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\\venv\\Scripts\\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Production Deployment

### Option 1: Streamlit Cloud
1. Push your code to a GitHub repository
2. Sign up for Streamlit Cloud (https://streamlit.io/cloud)
3. Click "New app" and connect your repository
4. Select the branch and main file (`app.py`)
5. Click "Deploy"

### Option 2: Docker
1. Build the Docker image:
   ```bash
   docker build -t deep-agent .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 deep-agent
   ```

## Environment Variables
No environment variables are required for the initial setup.

## Monitoring and Logs
- Streamlit provides built-in logging
- Check the terminal output for any errors
- For production, consider setting up proper logging and monitoring

## Troubleshooting
- Ensure all dependencies are installed
- Check port 8501 is available
- Verify Python version is 3.8 or higher
