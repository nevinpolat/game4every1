# ingest_games.py

import pandas as pd
import weaviate
import re
from sentence_transformers import SentenceTransformer
import numpy as np  # Import numpy to check for NaN values

# Initialize Weaviate client
client = weaviate.Client("http://localhost:8080")  # Adjust the URL if needed

# Initialize Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_duration(duration_str):
    """
    Extract the numeric part from the duration string (e.g., '90 minutes' -> 90).
    Returns 0 if the string is not in a valid format.
    """
    if isinstance(duration_str, str):
        match = re.search(r'\d+', duration_str)  # Find the first sequence of digits
        return int(match.group()) if match else 0  # Return the number or 0 if not found
    return 0  # Return 0 if input is not a string

def extract_setup_time(setup_time_str):
    """
    Extracts the numeric part from the setup time string (e.g., '10-15 minutes' -> 10).
    Returns 0 if the string is not in a valid format.
    """
    if isinstance(setup_time_str, str):
        match = re.search(r'\d+', setup_time_str)  # Find the first sequence of digits
        if match:
            return int(match.group())
    return 0  # Return 0 if no number is found or input is not valid

def parse_players_max(players_max_str):
    """
    Parse the playersMax field and return it as an integer.
    Returns 0 for invalid inputs or 'Not specified'.
    """
    if isinstance(players_max_str, str):
        if players_max_str.lower() in ['not specified', '']:
            return 0
        try:
            return int(players_max_str)  # Convert to int if possible
        except ValueError:
            return 0  # Return 0 if conversion fails
    elif isinstance(players_max_str, (int, float)):
        return int(players_max_str) if not np.isnan(players_max_str) else 0
    return 0  # Default to 0 for other types

def ingest_data(csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    # Iterate through each row and create a Weaviate object
    for _, row in data.iterrows():
        # Prepare the game data with error handling
        game_data = {
            "gameId": str(row['gameId']) if pd.notnull(row['gameId']) else "",
            "gameName": str(row['gameName']) if pd.notnull(row['gameName']) else "Unknown Game",
            "alternateNames": str(row['alternateNames']) if pd.notnull(row['alternateNames']) else None,
            "subcategory": str(row['subcategory']) if pd.notnull(row['subcategory']) else None,
            "level": str(row['level']) if pd.notnull(row['level']) else None,
            "description": str(row['description']) if pd.notnull(row['description']) else "No description available.",
            "playersMax": parse_players_max(row['playersMax']),  # Use the new function
            "ageRange": str(row['ageRange']) if pd.notnull(row['ageRange']) else "N/A",
            "duration": extract_duration(row['duration']),  # Use the existing function
            "equipmentNeeded": str(row['equipmentNeeded']) if pd.notnull(row['equipmentNeeded']) else "N/A",
            "objective": str(row['objective']) if pd.notnull(row['objective']) else "N/A",
            "skillsDeveloped": str(row['skillsDeveloped']) if pd.notnull(row['skillsDeveloped']) else "N/A",
            "setupTime": extract_setup_time(row['setupTime']),  # Use the existing function
            "place": str(row['place']) if pd.notnull(row['place']) else "N/A",
            "physicalIntensityLevel": str(row['physicalIntensityLevel']) if pd.notnull(row['physicalIntensityLevel']) else "N/A",
            "educationalBenefits": str(row['educationalBenefits']) if pd.notnull(row['educationalBenefits']) else "N/A",
            "category": str(row['category']) if pd.notnull(row['category']) else "N/A"
        }

        # Vectorize the game description
        description_vector = model.encode(game_data['description']).tolist()  # Convert numpy array to list

        # Add the object to Weaviate with the vector
        try:
            client.data_object.create(
                data_object=game_data,
                class_name="Game",
                vector=description_vector  # Provide the vectorized description
            )
            print(f"Inserted game: {game_data['gameName']}")
        except Exception as e:
            print(f"Failed to insert game: {game_data['gameName']}. Error: {e}")

if __name__ == "__main__":
    ingest_data("../data/game-dataset.csv")  # Ensure the CSV file is in the correct path
