# Technology Trends AI Chatbot

This repository contains a **Retrieval-Augmented Generation (RAG) full-stack chatbot application** built with **Python, FastAPI, Redis, React and OpenAI's GPT-4o.** The chatbot specializes in answering questions about new technology trends, powered by the latest reports from leading institutions such as the World Bank, World Economic Forum, McKinsey, Deloitte, and OECD.

The application is designed to be easily customizable, allowing you to **integrate your own data sources and adapt it to different use cases.**

You can access a [live demo of the RAG Chatbot application here](https://tech-trends-chatbot.codeawake.com).

For a detailed walkthrough of the code and the technologies used, check out this blog post: [Building an AI Chatbot Powered by Your Data](https://codeawake.com/blog/ai-chatbot).

## Structure

The repository is organized into two main folders:

- `backend/`: Contains the Python FastAPI backend code and a local Python version for testing.
- `frontend/`: Contains the React frontend code. It uses Vite.js as the build tool and bundler.

## Installation

### Prerequisites ✅

- Python 3.11+.
- Node.js 18+.
- Poetry (Python package manager).
- Redis Stack Server. Follow the [installation and running instructions](https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/). The application requires the RedisJSON and RediSearch modules, which Redis Stack Server includes. Alternatively, you can install Redis and add the required modules yourself.

### Backend

1. Navigate to the backend folder and install the Python dependencies using Poetry:

    ```bash
    cd backend
    poetry install
    ```

2. Create a `.env` file in the backend folder copying the `.env.example` file provided and set the required environment variable:
    - `OPENAI_API_KEY`: Your OpenAI API key.
  
3. The application uses Pydantic Settings for configuration management. You can adjust the configuration defaults in `backend/app/config.py`, or set the configuration variables directly using environment variables.

### Frontend

1. Navigate to the frontend folder and install the JavaScript dependencies:

    ```bash
    cd frontend
    npm install
    ```

2. Create a `.env.development` file in the frontend folder copying the `.env.example` file provided that includes the required environment variable:
    - `VITE_API_URL`: The URL to connect to the backend API.

## Running the Application

### Loading Source Documents

Before running the full-stack application, you need to load the source documents and build the knowledge base. Make sure Redis Stack Server is running before executing the loading script:

```bash
cd backend
poetry run load
```

This script processes the documents in the `backend/data/docs` directory, creates vector embeddings, and stores them in the Redis database.

You can **customize this chatbot with your own data sources:**
1. Replace the existing PDF files in the `backend/data/docs` with your own data sources.
2. If needed, adjust the `process_docs` function in `backend/app/loader.py` to handle different file formats.
3. Adjust the assistant prompts in `backend/app/assistants/prompts.py` for your specific use case.
4. Run the `poetry run load` script as shown above.

### Full-Stack Application

To run the full-stack chatbot application:

1. Ensure Redis Stack Server is running.
   
2. Activate the virtual environment for the backend and start the backend server:

    ```bash
    cd backend
    poetry shell
    fastapi dev app/main.py
    ```

3. In a separate terminal, start the frontend server:

    ```bash
    cd frontend
    npm run dev
    ```

4. Open your web browser and visit `http://localhost:3000` to access the application.

### Local Application

You can run the local Python application for testing in your console using the provided Poetry script:

```bash
cd backend
poetry run local
```

### Exporting Chats

To export all conversation chats to a JSON file in the `backend/data` directory:

```bash
cd backend
poetry run export
```