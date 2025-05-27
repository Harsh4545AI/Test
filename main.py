from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

# Initialize the AI mixologist agent
agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt="""You are Mixie, a friendly and knowledgeable AI mixologist designed to suggest personalized cocktail recipes. 
Your primary role is to recommend cocktails based on the user's mood and available ingredients. 
Your tone is conversational, upbeat, and professional—like a charming bartender who knows their craft well.
Always explain why a cocktail suits the mood, list ingredients with amounts, and provide simple instructions. 
Only suggest drinks that use the provided ingredients or close, common substitutes.""",
)

# User input
mood = input("Enter your current mood (e.g., relaxed, excited, gloomy): ")
ingredients = input("Enter the available ingredients (comma-separated): ")

# Format the query for the agent
query = f"""
I'm feeling {mood}. 
Here are the ingredients I have: {ingredients}.
Can you recommend a cocktail that fits my mood and uses these ingredients?
"""

# Run the agent
result = agent.run_sync(query)
print("\n🍹 Your Cocktail Recommendation:\n")
print(result.output)
