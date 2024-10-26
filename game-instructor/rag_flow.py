import weaviate
from weaviate import Client
from models import SearchedGame
from datetime import datetime
import traceback
import openai
import streamlit as st
from sentence_transformers import SentenceTransformer

# Initialize Sentence Transformer model for query vectorization
query_model = SentenceTransformer('all-MiniLM-L6-v2')

# Set your OpenAI API key (ensure you have this in your Streamlit secrets)
openai.api_key = st.secrets["OPENAI"]["API_KEY"]  # Store your API key in Streamlit secrets

# Function to check if the question is game-related using GPT-4o-mini
def check_if_game_related(question):
    """
    Determines if the question is related to games using the GPT-4o-mini model via OpenAI API.
    Returns True if related, False otherwise.
    """
    prompt = f"Determine if the following question is related to games. Answer with 'Yes' or 'No'.\n\nQuestion: \"{question}\""
    try:
        response = call_gpt_4o_mini(prompt)
        return 'yes' in response.lower()
    except Exception as e:
        st.error(f"🚨 Error calling GPT-4o-mini: {e}")
        st.error(traceback.format_exc())
        return False

# Function to call GPT-4o-mini model via OpenAI API
def call_gpt_4o_mini(prompt):
    """
    Calls the GPT-4o-mini model to process the prompt using OpenAI API.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Specify the model
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,  # Adjusted tokens
            temperature=0.0  # For deterministic output
        )
        # Access the content of the message correctly
        message_content = response.choices[0].message.content.strip()
        return message_content
    except Exception as e:
        st.error(f"🚨 OpenAI API Request Error: {e}")
        st.error(traceback.format_exc())
        return "No"

# Function to preprocess the question using query rewriting techniques
def preprocess_query(question):
    """
    Applies query rewriting techniques to the user's question.
    """
    # Create a prompt that instructs the model to apply the techniques
    prompt = f"""
Please rewrite the following question by applying the following query rewriting techniques:

1. Correct any spelling mistakes.
2. Simplify the question to be more straightforward and easily understandable.
3. Replace words with synonyms where appropriate to broaden the search results.
4. Handle any negative queries correctly by rephrasing them to reflect the true intent.
5. Paraphrase the question while maintaining its original meaning.

Original Question: "{question}"

Rewritten Question:
"""
    try:
        rewritten_question = call_gpt_4o_mini(prompt)
        return rewritten_question.strip()
    except Exception as e:
        st.error(f"🚨 Error preprocessing query with GPT-4o-mini: {e}")
        st.error(traceback.format_exc())
        return question  # Return the original question if an error occurs

# Function to search Weaviate using pure vector search
def search_weaviate(question, client, k=1):
    """
    Searches Weaviate using pure vector search to find the answer to the question.
    Returns the search results.
    """
    try:
        # Generate vector for the query using SentenceTransformer
        query_vector = query_model.encode(question).tolist()

        response = (
            client.query
            .get(
                "Game",
                [
                    "gameId",
                    "gameName",
                    "alternateNames",
                    "subcategory",
                    "level",
                    "description",
                    "playersMax",
                    "ageRange",
                    "duration",
                    "equipmentNeeded",
                    "objective",
                    "skillsDeveloped",
                    "setupTime",
                    "place",
                    "physicalIntensityLevel",
                    "educationalBenefits",
                    "category",
                    "_additional { id }"
                ]
            )
            .with_near_vector({
                "vector": query_vector,
                "certainty": 0.7  # Lowered certainty threshold
            })
            .with_limit(k)
            .do()
        )

        # Extract the game results
        return response.get('data', {}).get('Get', {}).get('Game', [])
    except Exception as e:
        st.error(f"🚨 Error searching Weaviate: {e}")
        st.error(traceback.format_exc())
        return []

# Function to save searched game to the database
def save_searched_game_to_db(session_db, game_info):
    """
    Saves the searched game information to the database.
    Args:
        session_db: SQLAlchemy session.
        game_info (dict): Information about the game.
    """
    try:
        game_id = game_info.get('gameId')
        if game_id:
            existing_game = session_db.query(SearchedGame).filter_by(game_id=game_id).first()
            if not existing_game:
                searched_game = SearchedGame(
                    game_id=game_id,
                    game_name=game_info.get('gameName'),
                    subcategory=game_info.get('subcategory'),
                    level=game_info.get('level'),
                    category=game_info.get('category'),
                    searched_time=datetime.utcnow()
                )
                session_db.add(searched_game)
                session_db.commit()
    except Exception as e:
        st.error(f"🚨 Error saving searched game to DB: {e}")
        st.error(traceback.format_exc())

# Function to generate an answer using GPT-4o-mini
def generate_answer_from_game_info(game_info, question):
    """
    Generates an answer based on the game information and the user's question.
    """
    game_description = game_info.get('description', 'No description available.')
    game_name = game_info.get('gameName', 'Unknown Game')

    prompt = f"""
You are a game instructor assistant. Use the following game information to answer the user's question.

Game Name: {game_name}
Description: {game_description}
Alternate Names: {game_info.get('alternateNames', 'N/A')}
Subcategory: {game_info.get('subcategory', 'N/A')}
Level: {game_info.get('level', 'N/A')}
Players Max: {game_info.get('playersMax', 'N/A')}
Age Range: {game_info.get('ageRange', 'N/A')}
Duration: {game_info.get('duration', 'N/A')}
Equipment Needed: {game_info.get('equipmentNeeded', 'N/A')}
Objective: {game_info.get('objective', 'N/A')}
Skills Developed: {game_info.get('skillsDeveloped', 'N/A')}
Setup Time: {game_info.get('setupTime', 'N/A')}
Place: {game_info.get('place', 'N/A')}
Physical Intensity Level: {game_info.get('physicalIntensityLevel', 'N/A')}
Educational Benefits: {game_info.get('educationalBenefits', 'N/A')}
Category: {game_info.get('category', 'N/A')}

User's Question: {question}

Answer:
"""

    try:
        response = call_gpt_4o_mini(prompt)
        return response
    except Exception as e:
        st.error(f"🚨 Error generating answer with GPT-4o-mini: {e}")
        st.error(traceback.format_exc())
        return "Sorry, I couldn't generate an answer at this time."

# Main function to get the answer
def get_answer(question, user_id, session_db, k=1, hybrid=False, weaviate_client=None):
    """
    Main function to get the answer to the question.
    Args:
        question (str): The user's question.
        user_id (int): The user's ID.
        session_db: SQLAlchemy session for database operations.
        k (int): Number of results to return.
        hybrid (bool): Whether to use hybrid search.
        weaviate_client: Weaviate client instance.
    Returns:
        dict: Contains 'is_related' (bool), 'message' (str), 'rewritten_question' (str), and 'answers' (list) if applicable.
    """
    # Preprocess the question using query rewriting techniques
    preprocessed_question = preprocess_query(question)

    # Check if either the original or the rewritten question is game-related
    is_related_original = check_if_game_related(question)
    is_related_rewritten = check_if_game_related(preprocessed_question)
    is_related = is_related_original or is_related_rewritten

    if not is_related:
        return {
            'is_related': False,
            'message': "Your question does not appear to be related to games. Please ask a game-related question.",
            'rewritten_question': preprocessed_question
        }
    else:
        # Search Weaviate using the preprocessed question
        results = search_weaviate(preprocessed_question, weaviate_client, k=k)
        if results:
            answers = []
            for result in results:
                game_id = result.get('gameId')
                # Generate an answer using GPT-4o-mini
                answer_text = generate_answer_from_game_info(result, preprocessed_question)
                answer = {
                    'game_name': result.get('gameName', 'Unknown Game'),
                    'answer': answer_text,
                    'game_id': game_id,
                    'subcategory': result.get('subcategory', None),
                    'level': result.get('level', None),
                    'category': result.get('category', None),
                }
                # Save the searched game to the database
                save_searched_game_to_db(session_db, result)
                answers.append(answer)
            return {
                'is_related': True,
                'answers': answers,
                'rewritten_question': preprocessed_question
            }
        else:
            return {
                'is_related': True,
                'message': "I couldn't find any games matching your question. Please try rephrasing or ask about another game.",
                'rewritten_question': preprocessed_question
            }
