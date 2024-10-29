# 🎮 Welcome to Game4Every1!
Welcome to the thrilling universe of **Game4Every1**! 

Are you ready to embark on an exciting journey to discover the perfect game? Game4Every1 is your ultimate game-finding buddy! Whether you're an educator, event organizer, parent, or just a gaming enthusiast, we have **game for everyone**—from action-packed adventures to brain-teasing puzzles.
 Dive into a world where game selection is effortless, personalized, and fun!

![alt text](image-1.png)
---

## [🛤️ Development Journey](#development-journey)
  - [📅 Day 1: Problem Description](./evaluation-criteria/1-problem-description/problem-description.md)
  - [📅 Day 2: Unlocking the Power of RAG](./evaluation-criteria/2-RAG-flow/RAG-flow.md)

  - [📅 Day 3: Retrieval Evaluation](./evaluation-criteria/3-retrieval-evaluation/retrieval-evaluation.md)
  - [📅 Day 4: RAG Evaluation of GPT-4o and GPT-4o-Mini](./evaluation-criteria/4-RAG-evaluation/RAG-evaluation.md)
  - [📅 Day 5: Create User Interface](./evaluation-criteria/5-interface/interface.md)
  - [📅 Day 6: Automated Data Ingestion with Python](./evaluation-criteria/6-ingestion-pipeline/ingestion-pipeline.md)
  - [📅 Day 7: Best Practices](./evaluation-criteria/7-best-practices/best-practices.md)
  - [📅 Day 8: Monitoring in the Games Instructor Assistant](./evaluation-criteria/8-monitoring/monitoring.md)


## 🌟 Implementation Guide

- [🐋 Day 9: Using Docker ](#day-9-docker-integration-smooth-sailing-with-docker-compose)
- [🔄 Day 10: Reproducibility](#day-10-reproducibility)
  - [🐳 Running the application with Docker Compose](#running-the-application-with-docker-compose)
  - [🐙 Running the application with Docker Without Compose](#running-the-application-with-docker-without-compose)
  - [💻 Running the application Locally](#running-locally-without-docker)
-  🌐 [Day 11: Game4Every1 in Streamlit Cloud](#day-11-game4every1-in-streamlit-cloud)
- [🛠️ Troubleshooting](#troubleshooting)
- [🙌 Acknowledgment](#acknowledgment)



---

# 🛤️ Development Journey
Over 11 days, we have carefully developed Game4Every1, a platform dedicated to helping users discover games that match their preferences. Below is an overview of each development stage, highlighting the challenges we faced, the solutions we implemented, and the milestones we achieved.

Our adventure begins with an exciting introduction to the project, which aims to create a super helpful Q&A system that connects players with games tailored to their tastes and preferences.

![alt text](image1.png)
##  Features

- **Personalized Game Recommendations:** Tailor game suggestions based on criteria like age range, number of players, duration, educational benefits, and physical intensity.
- **Robust Search Capabilities:** Utilize both keyword-based (MinSearch) and semantic (Weaviate) search methods to find the best games effortlessly.
- **Retrieval-Augmented Generation (RAG):** Enhance responses with accurate and engaging information using GPT-4o and GPT-4o-Mini models.
- **Interactive User Interface:** Seamlessly interact with our intuitive UI built with Streamlit, making game selection fun and user-friendly.
- **Automated Data Ingestion:** Keep your game database fresh and up-to-date with Python-powered ingestion pipelines.
- **Comprehensive Analytics Dashboard:** Monitor user engagement, feedback, and search performance with our detailed dashboards.
- **Flexible Deployment Options:** Easily run the application locally, on the cloud, or use Docker and Docker Compose for seamless deployment.

---

## 📅 [Day 1: Problem Description](./evaluation-criteria/1-problem-description/problem-description.md)



On Day 1, we set the stage for our project by defining the core problem we're solving: helping users navigate through a vast sea of over **600 unique games** to find their perfect match. 

Our solution? 

An **Interactive Games Instructor Assistant** powered by an advanced Large Language Model (LLM) and presented through a sleek Streamlit interface.

### 🎯 What We're Tackling

Imagine having hundreds of games at your fingertips, each with different age ranges, player counts, durations, educational benefits, and physical intensities. The challenge is making this information accessible and personalized for:

- **Educators** looking for engaging lesson activities
- **Event Organizers** planning team-building exercises
- **Parents** searching for age-appropriate games for their kids
- **Gamers** eager to explore new titles that match their interests

### 🌟 Our Mission

Our mission is simple: **Empower users to discover and select games effortlessly** based on their unique criteria. By focusing on user-centric design and reliable data, we aim to make game discovery fun and stress-free.

To achieve this, we provide comprehensive information about each game through the following key attributes:
| Column Name              | Description                                                                                   |
|-------------------------|-----------------------------------------------------------------------------------------------|
| `gameId`                    | A unique identifier for each game.                                                           |
| `gameName`              | The official name of the game.                                                                |
| `alternateNames`        | Other names or variations by which the game may be known.                                    |
| `subcategory`           | The specific category or type within the broader game classification.                        |
| `level`                 | The difficulty level of the game (e.g., beginner, intermediate, advanced).                   |
| `description`           | A brief overview of the game, including its premise and key features.                        |
| `playersMax`            | The maximum number of players that can participate in the game.                              |
| `ageRange`              | The recommended age range for players suitable for the game.                                 |
| `duration`              | The average time it takes to complete a game session.                                        |
| `equipmentNeeded`       | A list of materials or equipment required to play the game.                                  |
| `objective`             | The primary goal or aim players must achieve during the game.                                |
| `skillsDeveloped`       | The skills or competencies that players can develop through playing the game.                |
| `setupTime`             | The time required to prepare the game before starting.                                       |
| `place`                 | The recommended location or setting for playing the game.                                    |
| `physicalIntensityLevel`| A measure of the physical exertion required to play the game (e.g., low, moderate, high).    |
| `educationalBenefits`    | The potential learning outcomes or educational advantages gained from playing the game.      |
|`category`              | The broader classification or genre to which the game belongs (e.g., board game, card game).|

🔗 [Read Full Problem Description](./evaluation-criteria/1-problem-description/problem-description.md)

---

## [📅 Day 2: RAG FlowThe Secret Sauce Behind Game4Every1](./evaluation-criteria/2-RAG-flow/RAG-flow.md)



Day 2 was all about understanding the **RAG (Retrieval-Augmented Generation)** Flow—the heart of our recommendation engine. This process ensures that each game suggestion is spot-on and tailored just for you.

### 🔍 How It Works

1. **Retrieve the Knowledge Base 📚**
   - **MinSearch** quickly scans our database using keywords.
   - **Weaviate** dives deeper with context-aware searches for more complex queries.

2. **Vector Search with Weaviate 🔍**
   - Captures the essence of your questions, ensuring recommendations are relevant and meaningful.

3. **Answer with GPT-4o-Mini 🤖✨**
   - Synthesizes the data into clear, engaging responses, making the experience feel like chatting with a gaming buddy.

### 🎯 Our Goal

To **enhance recommendation accuracy** by leveraging advanced data retrieval and generation techniques, ensuring you always get the best game suggestions.

### 📊 Key Components

| Component            | Description                                      |
|----------------------|--------------------------------------------------|
| **Knowledge Base**   | Organized dataset for efficient game searches.   |
| **Indexing**         | Optimizes data access for quick retrieval.       |
| **RAG Process**      | Seamlessly integrates retrieval and generation. |

🔗 [Dive Deeper into RAG Flow](./evaluation-criteria/2-RAG-flow/RAG-flow.md)

---

## [📅 Day 3 Retrieval Evaluation: Finding the Best Game Match!](./evaluation-criteria/3-retrieval-evaluation/retrieval-evaluation.md)


On Day 3, we focused on evaluating our retrieval methods to guarantee that you receive the most relevant game suggestions.

### 🛠️ Testing Different Approaches

We compared **MinSearch** and **Weaviate** to see which one delivers better results. By analyzing key metrics like **Hit Rate** and **Mean Reciprocal Rank (MRR)**, we determined that **Weaviate** outperforms **MinSearch**, especially for complex queries.

### 📏 Key Metrics

| Metric          | What It Measures                                     |
|-----------------|------------------------------------------------------|
| **Hit Rate**    | Percentage of correct games in top results           |
| **MRR**         | Average position of the first relevant game          |

### 🧠 Why Weaviate Wins

**Weaviate** not only retrieves data based on keywords but also understands the context, making your game searches more accurate and satisfying.

### 📈 Results at a Glance

![alt text](image-10.png)

🔗 [Explore Retrieval Evaluation](./evaluation-criteria/3-retrieval-evaluation/retrieval-evaluation.md)

---

 ## [📅 Day 4 RAG Evaluation: Picking the Best Approach!](./evaluation-criteria/4-RAG-evaluation/RAG-evaluation.md)

Day 4 was dedicated to refining our **RAG Flow** by testing different configurations and selecting the best-performing approach.

### 🧪 Experimenting with RAG Configurations

We tried combining **MinSearch** with **GPT-4o** and **Weaviate** with **GPT-4o-Mini**. Through rigorous testing, we found that the latter provides more engaging and accurate responses.

### 👨‍⚖️ LLM-as-a-Judge

Our language models evaluated each RAG configuration based on **relevance**, **coherence**, and **engagement**, ensuring high-quality outputs.

### ⚔️ Model Showdown

![alt text](image-12.png)

GPT-4o achieved a relevance rate of 58%, slightly surpassing GPT-4o-Mini, which had a rate of 56.5%. Despite this, **GPT-4o-Mini** is still our top choice for generating game recommendations.

### 📈 Continuous Improvement

We integrated the best-performing RAG approach, ensuring that our recommendations are always top-notch.

🔗 [Learn More about RAG Evaluation](./evaluation-criteria/4-RAG-evaluation/RAG-evaluation.md)

---

## [📅 Day 5 User Interface: Streamlit Magic!](./evaluation-criteria/5-interface/interface.md)

Day 5 was all about building our **Streamlit**-powered user interface, designed to make your interaction with **Game4Every1** smooth and enjoyable.

### 🌟 Simple and Sleek Design

Our UI features a clean, minimalist layout that makes navigation effortless. Everything is organized for quick access, ensuring you can find games without any hassle.


**Meet Jane!** 🌟  

Jane is planning a family vacation and wants to find fun games for her kids. Our app is her secret weapon! With just a few clicks, she can uncover age-appropriate games that will keep everyone entertained on the road.

**What Can Jane Ask?**  
- "What games are great for my 5-year-old?"
![alt text](image-19.png)
- "Any group games for my 10 and 12-year-olds?"
![alt text](image-20.png)
- "What quick family games can we play together?"
![alt text](image-21.png)

**User Journey Made Easy!**  

We’re designing a simple flow for Jane:
1. **Register**: Jane enters her username, age, and gender.
2. **Ask Away**: She types her game questions.
3. **Smart Check**: The app verifies if her query is game-related.
4. **Refine**: If it is, we jazz it up using techniques like paraphrasing and synonym expansion.
5. **Get Recommendations**: Jane receives personalized game suggestions in no time!


### 🛠️ Behind the Scenes

Creating an intuitive UI involved understanding user behavior and designing for ease of use, ensuring that educators, event organizers, parents, and gamers can navigate effortlessly.

We’re all set to build an engaging app that makes game searching fun and easy for everyone. Let’s keep going!

🔗 [Check Out the Interface](./evaluation-criteria/5-interface/interface.md)

---

## [📅 Day 6 🚀 Automated Data Ingestion: Keeping It Fresh!](./evaluation-criteria/6-ingestion-pipeline/ingestion-pipeline.md)

On Day 6, we tackled the crucial task of **Automated Data Ingestion** to ensure our game database remains current and comprehensive.

### 🦸‍♂️ Weaviate to the Rescue!

Using **Weaviate**, we built an efficient data ingestion pipeline in Python that seamlessly imports and manages game data.

There are only two powerful scripts at the heart of our data pipeline: `define_schema.py` and `ingest_games.py`. Together, they ensure efficient management and ingestion of game data.

### 🔄 How It Works


- **Error Handling & Validation**: Robust mechanisms are in place to ensure data integrity throughout the ingestion process.

### 🛠️ Building the Pipeline
- **Weaviate Client Initialization**: This step connects the client to a Weaviate instance running locally on port 8080, facilitating smooth data interactions.
- **Defining the Schema**: The `define_schema.py` script establishes a well-structured schema for various game attributes, ensuring consistency and accuracy.
- **SentenceTransformer Model**: A specialized model is initialized to vectorize game descriptions, enhancing search and recommendation capabilities.
- **Data Processing**: Custom functions extract relevant data from the CSV file, handling various formats and potential errors seamlessly.
- **Data Ingestion**: The `ingest_games.py` script meticulously reads the game data and ingests it into Weaviate, with comprehensive error handling for each insertion to maintain data quality.

### 📊 Maintaining Freshness

Our automated ingestion process guarantees that our game database is always up-to-date, enhancing the accuracy and relevance of our recommendations.

🔗 [Learn More about Data Ingestion](./evaluation-criteria/6-ingestion-pipeline/ingestion-pipeline.md)

---

## [📅 Day 7: Best Practices – Optimizing Game4Every1](./evaluation-criteria/7-best-practices/best-practices.md) 

Today, we dived into the exciting world of **Hybrid Search** and **Document Reranking**! With our game data structured and ready, we enhanced our search capabilities to help users find the perfect games faster.

### 🔍 Why `index_weaviate.py`?

We switched to `index_weaviate.py` to optimize our data for hybrid search, which combines:
- **Text Search**: For exact keyword matches.
- **Vector Search**: For finding semantically similar documents.

### ⚡ Today’s Highlights

- **Implemented Hybrid Search**: Leveraged both search methods for better results.
- **Document Reranking**: Rearranged search results to show the most relevant games first.

### 🎯 Performance Boost

With a rank size of 10, we achieved a **Hit Rate@10** of **97.15%** and an **MRR@10** of **0.8177**. Our users are now more likely to find what they’re looking for!

![alt text](image-13.png)

By implementing best practices, **Game4Every1** ensures a high-quality, reliable, and user-friendly platform. This dedication guarantees that users receive optimal gaming recommendations tailored to their specific preferences.

🔗 [Discover Best Practices](./evaluation-criteria/7-best-practices/best-practices.md)

---


## [📅 Day 8: Monitoring: Keeping Track of the Fun!](./evaluation-criteria/8-monitoring/monitoring.md)

On Day 8, we focused on **Monitoring** to maintain and improve the user experience by tracking engagement,gathering feedback, and analyzing queries to enhance the **Game Instructor Assistant**.


### Key Highlights:

- **Dummy Users**: Created several dummy users to simulate realistic interactions and test query handling.
- **Query Handling**: 
  - **Wonderwoman**: Demonstrated effective query refinement for clarity.
  - **Xmen & Emma**: Showed flexibility in managing diverse inquiries.

### Query Handling Techniques:

<p align="center">
  <a href="https://youtu.be/oinsFsLu1dk">
    <img src="wonderwoman.jpg" alt="Watch the user wonderwoman Demo">
  </a>
</p>


1. **Paraphrasing**: Restating questions for clarity.
2. **Synonym Expansion**: Using synonyms to broaden search scope.
3. **Query Simplification**: Making complex queries straightforward.
4. **Handling Negative Queries**: Clarifying user intent in negative contexts.
5. **Spelling Correction**: Fixing typos for accurate interpretation.

## 🚀 Features

- **User Registration & Login**: Create a profile or log in with your username.
- **Ask Questions**: Get insights, rules, strategies, and more about various games.
- **Comprehensive Analytics Dashboard**: Analyze user data, feedback, game searches, and more.
- **Search Performance Metrics**: Evaluate the effectiveness of different search methods.
- **Chat History Management**: Keep track of your interactions and feedback.

### 📈 Dynamic Dashboard

Our **Streamlit**-powered dashboard visualizes key metrics to help us make informed decisions.


<p align="center">
  <a href="https://youtu.be/3027TanX_dA">
    <img src="dashboard.jpg" alt="Watch the dashboard Demo">
  </a>
</p>


- **User Analytics**: We created **11 dummy users** to simulate realistic interactions, allowing us to analyze user behavior and preferences more effectively. Insights include gender and age distribution among these users.

- **Feedback Analytics**: Our dummy users provided **17 feedback submissions**. Analyzing this feedback helps us gauge satisfaction levels and identify areas that require improvement.

- **Chat History Analytics**: By examining the chat histories of our dummy users, we can understand common queries and interactions, which inform our approach to enhancing user support.

- **Game Analytics**: Our dummy users searched for a total of **8 games**, highlighting their interests and helping us tailor future recommendations based on these preferences.

- **Search Performance Metrics**: We monitored metrics like Hit Rate@10 and Mean Reciprocal Rank (MRR@10) to assess the effectiveness of our search functionalities and ensure relevant game suggestions.




🔗 [Learn More about Monitoring](./evaluation-criteria/8-monitoring/monitoring.md)



## Day 9: Docker Integration: Smooth Sailing with Docker Compose!

We leverage Docker to manage our application seamlessly:

1. **Everything in Docker Compose 📦**: Our entire setup runs on Docker Compose, allowing easy multi-container deployment.

2. **Dockerfile for the Main Application 🛠️**: This ensures a consistent environment for all users.

3. **Dependencies Made Easy 🔗**: Our dedicated `docker-compose.yml` simplifies pulling in necessary components.


## Day 10: Reproducibility 

### 🛠️ Technologies Used

- **Backend**:
  - Python 3.11
  - SQLAlchemy
  - PostgreSQL
  - Weaviate (Vector Database)
  - OpenAI GPT-4o-mini
- **Frontend**:
  - Streamlit
  - Plotly
- **Others**:
  - Docker & Docker-Compose
  - Sentence Transformers
  - Conda

## 🗂️ Code Structure

The project follows a modular structure, with each file serving a specific purpose.

```
game4every1/
├── app.py                # Main application entry point
├── analytics.py    # Analytics dashboard implementation
├── initialize_db.py 
├── define_schema.py        # Weaviate schema definition
├── ingest_games.py   # ingest game data into Weaviate
├── models.py               # SQLAlchemy ORM models
├── rag_flow.py      #rag using Weaviate and GPT-4o-mini
├── requirements.txt   # List of required dependencies
├── Dockerfile    # Dockerfile to build the image
├── docker-compose.yml      # Docker-Compose config.
├── .streamlit/        
│   └── secrets.toml    # OpenAI keys
├── data/                # Main data file
|   └── game-dataset.csv    
└── README.md               # Documentation file
```

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Conda**: [Install Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker-Compose**: [Install Docker-Compose](https://docs.docker.com/compose/install/)
- **Streamlit Secrets Configuration**: You'll need to set up your `streamlit` secrets for database and OpenAI API keys.

## 📂 Installation

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/nevinpolat/game4every1.git
cd game4every1
```

### 2. Set Up Conda Environment

Create a Conda environment for managing dependencies.

1. **Create the Conda Environment**:

   ```bash
   conda create -n game-instructor-env python=3.11.9
   ```

2. **Activate the Environment**:

   ```bash
   conda activate game-instructor-env
   ```
### 3. Install Dependencies

1. **Ensure the Conda Environment is Activated**:

   ```bash
   conda activate game-instructor-env
   ```

2. **Install Dependencies**:
- Installing pip
Conda Environment: When you create a new Conda environment, pip is usually installed by default. However, if for some reason it's not available, you can easily install it with:

   ```bash
   conda install pip
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
![alt text](image.png)

### 4. Configure Environment Variables: Replace placeholders with actual values.

Create a `.env` file in the root directory to store your environment variables.

```bash
touch .env
```

Add the following variables to the `.env` file:

```env
# Database Configuration

DATABASE_URL='postgresql://your_db_username:your_db_password@DB_HOST:DB_PORT/DB_NAME'
DB_PASSWORD='your_db_password'
DB_PORT='5432'
DB_NAME='game4every1-db' #your db
DB_USER='your_db_username'
OPENAI_API_KEY='sk-proj-....' #your_openai_api_key


WEAVIATE_URL='http://localhost:8080' #access db locally
WEAVIATE_URL='http://weaviate:8080' #access weaviate db

DB_HOST='db' #docker-compose
DB_HOST='localhost' #locally
DB_HOST=game4every1-db #docker without compose
```
## 🗂️ Streamlit Configuration

### Setting Up `.streamlit`

1. **Create `.streamlit` Directory**:

   ```bash
   mkdir .streamlit
   ```

2. **Add Secrets to `.streamlit/secrets.toml`**:

   ```toml
   [DB]
   USER = "your_db_username"
   PASSWORD = "your_db_password"
   NAME = "game4every1-db"
   PORT = "5432"        # Default PostgreSQL port
   HOST = "db"          # hostname for PostgreSQL service in docker-compose
   HOST='localhost' #locally
   HOST=game4every1-db #docker without compose

   [WEAVIATE]
   URL = "http://weaviate:8080"  # Correct hostname for Weaviate service
   URL='http://localhost:8080' #local access

   [OPENAI]
   API_KEY ='your_openai_api_key'
   ```
   
**Replace placeholders with actual values.**



## 🔑 Database Configuration

### Using Docker-Compose

With Docker-Compose, PostgreSQL service creates `db` automatically.
1. **Changing DB_HOST and URL for Docker-Compose**

**.env**
```bash
  - DB_HOST=db
  - WEAVIATE_URL=http://weaviate:8080
```
**streamlit**
```bash
  - HOST = "db"          # hostname for PostgreSQL 
  - URL=http://weaviate:8080
```

2. **Start Services with Docker-Compose**:

```bash
   docker-compose up --build
```
   **or  after building you can just use**
```bash
   docker-compose up
   ```
3. **Verify Database Creation**:

```bash
docker exec -it game4every1-db-1 psql -U your_db_username -d game4every1-db
```
![alt text](image-5.png)
![alt text](image-3.png)



### Running the Application with Docker-Compose



1. **Access at `http://localhost:8501`**

<p align="center">
  <a href="https://youtu.be/AEw-EPwSNbA">
    <img src="docker-compose.jpg" alt="Watch docker-compose Demo">
  </a>
</p>


2. **Stop Services**:

   ```bash
   docker-compose down
   ```




## Running the Application with Docker (Without Compose)

### 1. Changing DB_HOST and URL for Docker

If using `docker`, make sure to change `DB_HOST` to `game4every1-db` as follows:

**.env**
```bash
  - DB_HOST='game4every1-db'
  - WEAVIATE_URL='http://weaviate:8080'
```
**streamlit**

```bash
   - HOST = 'game4every1-db'          # hostname for PostgreSQL 
   - URL='http://weaviate:8080'
```
### 2.Create a Docker network (if not already):

```bash
docker network create game4every1-network
```
### 2. Running PostgreSQL Database

Run the PostgreSQL container using the host's network. This will make the database accessible at `localhost:5432`.

```bash
docker run -d \
  --name game4every1-db \
  --network="game4every1-network" \
  -e POSTGRES_USER=your_username \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=your_database_name\
  -p 5432:5432 \
  postgres:14

```
**If you encounter the following error:**

 failed to bind port 0.0.0.0:5432/tcp: Error starting userland proxy: listen tcp4 0.0.0.0:5432: bind: address already in use.


You can resolve it by identifying which process is using port 5432 with the following command:

```bash
sudo lsof -i :5432
 ```
Once you've identified the process, you can stop the PostgreSQL service with:
  ```bash
 sudo service postgresql stop
 ```
 ![alt text](image-6.png)
 if it does not work, follow the screenshot. 
 ![alt text](image-8.png)
### Docker Error: Container Name Conflict

You may encounter the following error:


 ![alt text](image-14.png)

To resolve this conflict, you can stop the existing container using its ID:

```bash
docker stop f3d41d4d196e1d059fb94988b70ac35f4277a1ea674246391088935cbd9c2839
&&
docker container prune
```


### 3. Running Weaviate

Start the Weaviate container using the host network. Make sure it runs on port 8080.

```bash
docker run -d \
  --name weaviate \
  --network="game4every1-network" \
  -p 8080:8080 \
  -e QUERY_DEFAULTS_LIMIT=20 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  semitechnologies/weaviate:latest

```
### 3. Build the app
```bash
docker build -t game4every1-app .
```
### 4. Running the Streamlit Application

Run the Streamlit app, specifying the database and Weaviate configurations.

```bash
docker run -d \
  --name game4every1-app \
  --network="game4every1-network" \
  -p 8501:8501 \
  game4every1-app

```

### 5. Accessing the Application

![alt text](image-9.png)
- Open a web browser and go to `http://localhost:8501` to access the Streamlit application.


## Running Locally (Without Docker)


### 1. Install PostgreSQL

- **Download and Install PostgreSQL**: [Download PostgreSQL](https://www.postgresql.org/download/) for your operating system and follow the installation instructions.
- For detailed guidance, refer to the [PostgreSQL Guide](https://github.com/nevinpolat/game-instructor/blob/main/evaluation-criteria/5-interface/PostgreSQL_Setup_Guide.md).


### 2. Create the Database

1. Open your terminal and create the database named `game4every1_db`:
   ```sql
   psql -U postgres
   CREATE USER your_db_username WITH PASSWORD 'your_db_password';
   CREATE DATABASE game4every1-db;
   GRANT ALL PRIVILEGES ON DATABASE game4every1-db TO your_db_username;
 
- Replace `your_db_username` and `your_db_password` with your actual PostgreSQL username and PostgreSQL password.

  
2. **Run the Script to Create Tables**:

If the tables do not exist in the PostgreSQL database, follow these steps to create them and run the application locally.
   - Run the script to create the necessary tables in your PostgreSQL database:
     ```bash
     python initialize_db.py
     ```
   - This script will create the `users`, `feedback`, `searched_games`, and `chat_history` tables.


### 3. Configure the Database URL

- Set up the `DATABASE_URL` in a `.env` file or directly in your environment settings:
  ```
  DATABASE_URL='postgresql://your_db_username:your_db_password@localhost:5432/game4every1-db'
  ```
- Replace `your_db_username` and `your_db_password` with your actual PostgreSQL credentials.


### 📊 Ingesting Data
1. **Activate Environment**:

```bash
   conda activate game-instructor-env
   ```

2. **Ensure Weaviate is Running**.
```bash
docker run -d \
  --name weaviate \
  -p 8080:8080 \
  -e QUERY_DEFAULTS_LIMIT=20 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  semitechnologies/weaviate:latest
```


3.  follow these steps to define the schema and ingest data:
  ```bash
  python define_schema.py
  python ingest_games.py
  ```


2. **Run Streamlit**:

```bash
   streamlit run app.py
```

- Access the application by opening a web browser and navigating to `http://localhost:8501`.

## DAY 11: Game4Every1 in Streamlit Cloud


### Application URL
- **Live Application**: [Game4Every1](https://game4every1.streamlit.app)
![alt text](image-18.png)

### GitHub Repository
You can find the complete source code for the Game4Every1 app in the following GitHub repository: [Game4Every1-cloud on GitHub](https://github.com/nevinpolat/game4every1-cloud).

### Deployment Steps Overview

| Step       | Description                                           | Notes                                          |
|------------|-------------------------------------------------------|------------------------------------------------|
| **1**      | Set up Supabase                           ![alt text](image-17.png)        | Create a new project and configure the database schema. Note db, user,password, name, host  |
| **2**      | Configure Weaviate  ![alt text](image-16.png)                                 | Log in to Weaviate Cloud and create a cluster. Obtain the Weaviate URL and API key. |
| **3**      | Prepare Your Streamlit App                           | Ensure the app is ready and includes a `requirements.txt` file for dependencies. |
| **4**      | Upload Code to GitHub                                | Push your application code to a GitHub repository. |
| **5**      | Deploy on Streamlit Cloud                            | Connect your GitHub repo in Streamlit Cloud and follow the deployment prompts. |


Congratulations! Your **Game4Every1** app is now deployed and operational, utilizing **Streamlit Cloud**, **Supabase**, and **Weaviate** for enhanced functionality. 


---

### Troubleshooting

If you encounter issues during the setup process, refer to the appropriate guides below for further assistance:

- **.env Setup Issues**: If you are having trouble setting up or loading environment variables from the `.env` file, please refer to the [config.md](config.md) file for detailed instructions on how to correctly configure and use environment variables in your application.

- **PostgreSQL Configuration Issues**: If you encounter any problems related to PostgreSQL setup or connectivity, please refer to the [postgres-guide.md](https://github.com/nevinpolat/game-instructor/blob/main/evaluation-criteria/5-interface/PostgreSQL_Setup_Guide.md). file for detailed troubleshooting steps, configuration examples, and connection tips.




#### 🛡️ Security Considerations

- **Environment Security**: Secure sensitive data in `.env` and `secrets.toml`.
- **API Keys**: Avoid hardcoding API keys in your codebase.

#### ❓ Additional Troubleshooting Tips

- If you encounter port conflicts, ensure that the specified ports are not in use.
- Verify that Docker services are running and containers are started correctly.

- **Connection Issues**: Double-check Weaviate and PostgreSQL URLs for accuracy.
- **Docker Failures**: If issues arise, rebuild the containers using `docker-compose up --build`.


---

## Acknowledgment

This project is part of the [**LLM-Zoomcamp**](https://github.com/DataTalksClub/llm-zoomcamp/tree/main), an initiative focused on hands-on learning and practical implementation of language models and AI technologies.

## Final Thoughts

Thank you for taking the time to explore this project! It's been an exciting journey to bring this app to life, and I hope it serves as a helpful resource or inspiration for your own projects. Whether you’re using it as a learning tool, a prototype, or a starting point for something bigger, I’m glad to have shared this experience.

If you have any feedback, suggestions, or improvements, feel free to contribute or reach out. Keep building, keep learning, and happy coding!



---


