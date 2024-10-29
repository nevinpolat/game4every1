# index_weaviate.py

import pandas as pd
import weaviate
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Initialize Weaviate client
client = weaviate.Client("http://localhost:8080")

# Delete the class if it already exists
if client.schema.exists("Game"):
    client.schema.delete_class("Game")

# Define the schema
game_class = {
    "class": "Game",
    "description": "A class representing a game",
    "vectorizer": "none",  # We'll provide our own vectors
    "properties": [
        {"name": "gameId", "dataType": ["string"], "description": "Unique identifier for the game"},
        {"name": "gameName", "dataType": ["text"], "description": "Name of the game"},
        {"name": "alternateNames", "dataType": ["text"], "description": "Alternative names for the game"},
        {"name": "subcategory", "dataType": ["text"], "description": "Subcategory of the game"},
        {"name": "level", "dataType": ["text"], "description": "Difficulty or experience level required"},
        {"name": "description", "dataType": ["text"], "description": "Detailed description of the game"},
        {"name": "playersMax", "dataType": ["int"], "description": "Maximum number of players"},
        {"name": "ageRange", "dataType": ["text"], "description": "Suitable age range for players"},
        {"name": "duration", "dataType": ["text"], "description": "Duration of the game"},
        {"name": "equipmentNeeded", "dataType": ["text"], "description": "Equipment required to play the game"},
        {"name": "objective", "dataType": ["text"], "description": "The main objective of the game"},
        {"name": "skillsDeveloped", "dataType": ["text"], "description": "Skills that players develop"},
        {"name": "setupTime", "dataType": ["text"], "description": "Time required to set up the game"},
        {"name": "place", "dataType": ["text"], "description": "Specific place or setting for the game"},
        {"name": "physicalIntensityLevel", "dataType": ["text"], "description": "Physical intensity level"},
        {"name": "educationalBenefits", "dataType": ["text"], "description": "Educational benefits"},
        {"name": "category", "dataType": ["text"], "description": "Main category of the game"},
    ]
}

# Create the schema
client.schema.create_class(game_class)

# Load the game data
df_games = pd.read_csv('../data/game-dataset.csv').fillna('')

# Function to combine fields
def combine_fields(row):
    fields = [
        'gameName',
        'alternateNames',
        'subcategory',
        'level',
        'description',
        'playersMax',
        'ageRange',
        'duration',
        'equipmentNeeded',
        'objective',
        'skillsDeveloped',
        'setupTime',
        'place',
        'physicalIntensityLevel',
        'educationalBenefits',
        'category'
    ]
    return ' '.join(str(row[field]) for field in fields if row[field])

# Load the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to import data
def import_data(df):
    with client.batch as batch:
        batch.batch_size = 100
        for index, row in tqdm(df.iterrows(), total=len(df)):
            properties = {
                "gameId": str(row["gameId"]),
                "gameName": row["gameName"],
                "alternateNames": row["alternateNames"],
                "subcategory": row["subcategory"],
                "level": row["level"],
                "description": row["description"],
                "playersMax": int(row["playersMax"]) if str(row["playersMax"]).isdigit() else 0,
                "ageRange": row["ageRange"],
                "duration": row["duration"],
                "equipmentNeeded": row["equipmentNeeded"],
                "objective": row["objective"],
                "skillsDeveloped": row["skillsDeveloped"],
                "setupTime": row["setupTime"],
                "place": row["place"],
                "physicalIntensityLevel": row["physicalIntensityLevel"],
                "educationalBenefits": row["educationalBenefits"],
                "category": row["category"],
            }

            # Generate embedding for the 'combined_text' field
            combined_text = combine_fields(row)
            embedding = embedding_model.encode(combined_text).astype('float32')

            client.batch.add_data_object(
                data_object=properties,
                class_name="Game",
                vector=embedding
            )

# Import the data
import_data(df_games)

