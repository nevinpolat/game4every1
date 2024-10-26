# define_schema.py

import weaviate

# Initialize Weaviate client
client = weaviate.Client("http://localhost:8080")  # Adjust the URL if needed

def create_schema():
    # Clear the existing schema (optional, use with caution)
    client.schema.delete_all()

    # Define the schema for the Game class
    game_class_schema = {
        "class": "Game",
        "vectorizer": "none",  # Using manual vectorization with SentenceTransformer
        "properties": [
            {"name": "gameId", "dataType": ["string"]},
            {"name": "gameName", "dataType": ["string"]},
            {"name": "alternateNames", "dataType": ["string"]},
            {"name": "subcategory", "dataType": ["string"]},
            {"name": "level", "dataType": ["string"]},
            {"name": "description", "dataType": ["text"]},
            {"name": "playersMax", "dataType": ["int"]},
            {"name": "ageRange", "dataType": ["string"]},
            {"name": "duration", "dataType": ["int"]},
            {"name": "equipmentNeeded", "dataType": ["string"]},
            {"name": "objective", "dataType": ["string"]},
            {"name": "skillsDeveloped", "dataType": ["string"]},
            {"name": "setupTime", "dataType": ["int"]},
            {"name": "place", "dataType": ["string"]},
            {"name": "physicalIntensityLevel", "dataType": ["string"]},
            {"name": "educationalBenefits", "dataType": ["string"]},
            {"name": "category", "dataType": ["string"]},
        ]
    }

    # Create the Game class in Weaviate
    client.schema.create_class(game_class_schema)
    print("Schema for 'Game' class created successfully.")

if __name__ == "__main__":
    create_schema()
