# Syno, the Medicine Assistant Chatbot

Syno is a virtual medicine assistant chatbot designed to provide detailed and accurate information about medicines using advanced Retrieval-Augmented Generation (RAG) techniques. Leveraging a dataset of 11,000 medicines, Syno offers insights on compositions, uses, and side effects. This tool aims to enhance medical decision-making and patient care by ensuring quick and reliable access to critical drug information for both healthcare professionals and patients.

![image](https://github.com/synoloris/syno-medicine-assistant-chatbot/assets/24429312/9f2b7387-7b7c-4b1c-985e-1ac24163dde7)
![image](https://github.com/synoloris/syno-medicine-assistant-chatbot/assets/24429312/aaa462f7-6adf-4f18-b2f4-ce1be51b4b24)
![image](https://github.com/synoloris/syno-medicine-assistant-chatbot/assets/24429312/2051971d-58ad-4ed3-9871-dbbd07269ca2)


## Table of Contents

- [Syno, the Medicine Assistant Chatbot](#syno-the-medicine-assistant-chatbot)
  - [Table of Contents](#table-of-contents)
  - [Project Goal and Motivation](#project-goal-and-motivation)
    - [Goal](#goal)
    - [Motivation](#motivation)
  - [Data Collection or Generation](#data-collection-or-generation)
    - [Data Source](#data-source)
    - [Data Collection Process](#data-collection-process)
  - [Modeling](#modeling)
    - [Approach](#approach)
    - [Prompt Engineering](#prompt-engineering)
  - [Interpretation and Validation](#interpretation-and-validation)
    - [Validation Method](#validation-method)
    - [Testcases](#testcases)
      - [test\_create\_user\_and\_chat](#test_create_user_and_chat)
      - [test\_clear\_chat\_history](#test_clear_chat_history)
      - [test\_get\_messages](#test_get_messages)
    - [Benchmarking](#benchmarking)
  - [Prerequisites](#prerequisites)
  - [Used Technologies](#used-technologies)
  - [Setup](#setup)
    - [1. Create and Activate Virtual Environment](#1-create-and-activate-virtual-environment)
      - [Windows](#windows)
      - [macOS/Linux](#macoslinux)
    - [2. Install Dependencies](#2-install-dependencies)
    - [3. Set Up Environment Variables](#3-set-up-environment-variables)
    - [4. Set Up MySQL Database](#4-set-up-mysql-database)
    - [5. Embed the Dataset](#5-embed-the-dataset)
    - [6. Run the Application](#6-run-the-application)
  - [Usage](#usage)
  - [Example messages](#example-messages)
  - [Project Structure](#project-structure)
  - [Error Handling](#error-handling)
  - [Credits](#credits)

## Project Goal and Motivation

### Goal
The goal of this project is to develop a virtual medicine assistant chatbot named Syno, capable of providing accurate and helpful information about medicines to assist both medical professionals and patients. The chatbot leverages a comprehensive dataset of 11,000 medicines to offer detailed information on compositions, uses, and potential side effects. By integrating RAG (Retrieval-Augmented Generation) techniques, Syno aims to enhance the efficiency and reliability of medical information retrieval, ultimately improving the decision-making process in healthcare settings.

### Motivation
The motivation behind this project stems from the increasing need for rapid and reliable access to medical information. Medical professionals often require quick references to detailed drug information to make informed decisions about patient care. Traditional methods of information retrieval can be time-consuming and prone to human error. Syno aims to address these challenges by providing a streamlined, AI-powered solution that delivers precise and relevant information instantly. This not only aids in improving patient care but also reduces the cognitive load on healthcare providers, allowing them to focus more on direct patient interactions.

## Data Collection or Generation

### Data Source
The primary dataset used in this project is sourced from [Kaggle](https://www.kaggle.com/datasets/singhnavjot2062001/11000-medicine-details), contributed by the user `singhnavjot2062001`. This dataset contains extensive information on 11,000 medicines, including details such as medicine names, compositions, uses, side effects, and user reviews. This rich dataset serves as the foundation for Syno's knowledge base, enabling the chatbot to provide comprehensive responses to a wide range of medical queries.

### Data Collection Process
1. **Data Download**: The dataset was downloaded directly from Kaggle. To ensure the data is up-to-date and accurate, it is recommended to periodically check for updates on the Kaggle page.
2. **Data Embedding**: To facilitate efficient retrieval during chatbot interactions, the dataset was embedded using a Sentence Transformer model (all-MiniLM-L6-v2). This involves converting the textual information into numerical vectors that capture the semantic meaning of the data.
3. **Storage**: The embedded dataset is stored as corpus_embeddings.pt and embedded_dataset.csv for quick access during runtime. This allows the chatbot to efficiently search and retrieve relevant information based on user queries.

## Modeling

### Approach
- **Pre-trained Model**: The project utilizes the `all-MiniLM-L6-v2` model from the Sentence Transformers library to encode the dataset, which can be found on [HuggingFace](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). This model is chosen for its balance of speed and accuracy, making it suitable for real-time applications.
- **RAG (Retrieval-Augmented Generation)**: The core approach involves two main components:
  1. **Retrieval**: Given a user query, the embedded dataset is searched to retrieve the most relevant pieces of information. This is done using the pre-trained Sentence Transformer model to ensure semantically similar results.
  2. **Generation**: The retrieved information is then passed to OpenAI's GPT-3.5-turbo model to generate a coherent and contextually appropriate response. This ensures that the chatbot's answers are not only accurate but also easy to understand.

### Prompt Engineering
The chatbot, named Syno, is designed to act as a knowledgeable medical assistant. The prompts are carefully engineered to keep the conversation focused on providing medical information while maintaining a natural and engaging interaction style. Key aspects of prompt engineering include:

- **Contextual Prompts**: Ensuring that each user query is handled within the context of the conversation, maintaining continuity and relevance.
- **Information Extraction**: Prompts are structured to also gather essential some patient information before addressing the medical query. This ensures that the responses are tailored to the individual needs of the user.
- **Concise and Accurate Responses**: The prompts are designed to elicit concise and accurate responses from the model, minimizing the risk of information overload and focusing on the most relevant details.

By combining retrieval and generation techniques, Syno is able to provide accurate, contextually appropriate, and easily understandable medical information to users, enhancing the overall utility of the chatbot in healthcare settings.

## Interpretation and Validation

### Validation Method
- The chatbot's performance is validated by testing it with multiple queries and scenarios.
- Responses are compared with known correct answers and human judgments to ensure accuracy and relevance.
- The project includes a variety of test cases to demonstrate the chatbot's capabilities across different queries.

### Testcases

The file `test_app.py` contains three tests to validate the functions of the application. Execute the following command in bash to run the tests.

```bash
python test_app.py
```

#### test_create_user_and_chat
This test case simulates the process of creating a new user named "John Doe" and initiating a chat with the virtual assistant. It performs the following steps:

- Sends a POST request to create a new user.
Verifies that the user is successfully added to the database.
- Sends a message from the user to the virtual assistant.
- Verifies that both the user's message and the virtual assistant's response are stored in the database.


#### test_clear_chat_history

This test case ensures that the functionality to clear the chat history works correctly. It performs the following steps:

- Sends a POST request to create a new user named "Jane Doe".
- Sends a message from the user to the virtual assistant.
- Sends a DELETE request to clear the chat history for the user.
- Verifies that the chat history is cleared, leaving only the initial prompt message in the database.

#### test_get_messages

This test case tests the functionality of retrieving chat messages for a user. It performs the following steps:

- Sends a POST request to create a new user named "Alice".
- Sends a message from the user to the virtual assistant.
- Sends a GET request to retrieve the chat messages for the user.
- Verifies that the messages are correctly retrieved and match the expected content (one user message and one virtual assistant response).

These test cases help ensure that the core functionalities of user creation, chat history management, and message retrieval are working as expected in the application.

### Benchmarking
- The chatbot's responses are benchmarked against human-provided answers.
- Further validation is done using word embeddings to ensure the semantic similarity of responses.

## Prerequisites

- Python 3.7+
- Local MySQL (for example MySQL Workbench)

## Used Technologies
The project is implemented using the following technologies:

- **Python**: The core programming language used for developing the application.
- **Flask**: A lightweight WSGI web application framework used to create the web server for the chatbot interface.
- **OpenAI API**: Utilized for generating natural language responses based on the retrieved information.
- **Sentence Transformers**: A library for embedding sentences into high-dimensional vectors, used for semantic search and retrieval.
- **Pandas**: A powerful data manipulation library used for handling and processing the medicine dataset.
- **PyTorch**: A machine learning framework used for handling tensor operations and model computations.
- **MySQL**: A relational database management system used for storing user data and chat history.
- **Flask-MySQLdb**: A Flask extension used to integrate MySQL with the Flask application.
- **Flask-CORS**: A Flask extension used to handle Cross-Origin Resource Sharing (CORS) to allow the frontend to interact with the backend.
- **Kaggle**: Used for the dataset.
- **ConfigParser**: A module used to handle configuration files for setting environment variables and database configurations.

## Setup

### 1. Create and Activate Virtual Environment

First, navigate to the project directory and create a virtual environment:

```bash
python -m venv .venv

```

Activate the virtual environment:

#### Windows

```bash
.\.venv\Scripts\activate
```

#### macOS/Linux

```bash
source .venv/bin/activate
```

### 2. Install Dependencies

With the virtual environment activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a file named `application.properties` in the root directory of the project and add the following configuration, replacing the placeholders with your actual values:

```application.properties
MYSQL_HOST=your_mysql_host
MYSQL_PORT=your_mysql_port
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=your_mysql_database
OPENAI_API_KEY=your_openai_api_key
```

### 4. Set Up MySQL Database

```sql
CREATE DATABASE your_mysql_database;

USE your_mysql_database;

CREATE TABLE IF NOT EXISTS users (
    uuid VARCHAR(36) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    user_uuid VARCHAR(36) NOT NULL,
    sender ENUM('user', 'bot') NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_uuid) REFERENCES users(uuid)
);
```

### 5. Embed the dataset

The dataset has been downloaded from Kaggle and lies under `dataset/Medicine_Details.csv` and can be embedded using the `embed_dataset.py` script.

Run the following command in the root of the project to embed the dataset.

```bash
python model/embed_dataset.py
```

After running the command, the files `embed_dataset.py` and `embed_dataset.py` will be created inside folder `model`. 

### 6. Run the Application

Start the Flask application:

```bash
python app.py
```

The application will be available at http://127.0.0.1:8080.

## Usage

1. Open the application in your browser.
2. Create a new user.
3. Start chatting with the virtual assistent.
4. Use the clear history button to clear the chat history (if needed).

## Example messages

- My patient has a headache. What can I do?
- What's the composition of Melanorm-MS Cream?
- What are the side effects of Atocor 5 Tablet?
- Which medicines contain Dimethicone?
- Are there alternatives to Respizen Nasal Spray?
- My client broke his nose.
- My client experiences Hallucination. Which medicament could he have taken?

## Project Structure


```bash
.
├── .gitignore
├── app.py
├── application.properties
├── README.md
├── requirements.txt
├── test_app.py
├── chatbot
│   ├── __pycache__/
│   ├── chatbot.py
│   └── rag.py
├── dataset
│   └── Medicine_Details.csv
├── model
│   ├── corpus_embeddings.pt
│   ├── embed_dataset.py
│   └── embedded_dataset.csv
├── static
│   ├── css
│   │   └── style.css
│   └── images
│       ├── back.png
│       ├── favicon.png
│       ├── patient.png
│       ├── syno.png
│       └── trash.png
└── templates
    ├── chat.html
    ├── index.html
    └── new_user.html

```

## Error Handling

The application has been implemented with robust error handling mechanisms to ensure smooth and reliable operation. Key aspects of error handling include:

1. **API Error Handling**:
   - The chatbot's interaction with the OpenAI API is wrapped in a retry logic. If an API call fails due to rate limits, timeouts, or other transient issues, the application will automatically retry the request up to three times before returning a fallback error message.
   - Specific exceptions handled include `APIError`, `RateLimitError`, `Timeout`, `InvalidRequestError`, and `AuthenticationError`.

2. **Database Error Handling**:
   - Database interactions are managed using try-except blocks to catch and handle any SQL errors. This ensures that any issues with the database connection or queries do not crash the application.
   - The application ensures that database connections are properly closed after each operation to prevent connection leaks.

3. **Flask Application Error Handling**:
   - The Flask application includes global error handlers to catch and handle any unexpected errors that may occur during request processing.
   - Custom error handlers are implemented for different HTTP error codes:
     - 404 Not Found: Returns a JSON response with an error message indicating the resource was not found.
     - 500 Internal Server Error: Returns a JSON response with an error message indicating an internal server error occurred.

   - Custom error pages or JSON responses are returned to provide meaningful feedback to the user.

1. **Validation and Input Handling**:
   - User inputs are validated to prevent injection attacks and ensure that the data conforms to expected formats.
   - Any invalid inputs are gracefully handled, with appropriate error messages returned to the user.

By implementing these error handling strategies, the application aims to provide a robust and user-friendly experience, even in the face of unexpected issues.

## Credits

This application was implemented by Loris Vonlanthen (vonlalor@students.zhaw.ch) for the ZHAW module "Machine Learning II". For any issues or further assistance, feel free to contact the project maintainers.
