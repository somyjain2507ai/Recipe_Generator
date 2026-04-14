import logging
import sys
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ReceipeGenerator")

logger.info("Starting Recipe Generator Agent...")
load_dotenv()

api_key= os.getenv("OPENAI_API_KEY")
if not api_key or api_key.startswith("sk-y"):
    logger.error("OPENAI_API_KEY not set! Copy .env.example to .env and add your key.")
    sys.exit(1)

logger.info("API key loaded successfully")
logger.info("All LangChain components imported")
logger.info("Initializing the LLM (OpenAI GPT)...")

llm=ChatOpenAI(
    model="gpt-5.4-nano",
    temperature=0.5,
    verbose=True,)
logger.info(f"LLM initialized: model={llm.model}, temperature={llm.temperature}")
logger.info("Defining agent tools...")

@tool
def suggest_recipe(ingredients: list[str]) -> list[str]:
    """
    Generates a recipe based on a list of ingredients.
    Input should be a list of ingredients (e.g., ["chicken", "rice", "broccoli"]).
    Returns a structured recipe with name, description, and ingredients list.
    """
    logger.info(f"[Tool: suggest_recipe] Received ingredients: {ingredients}")

    recipe_prompt = PromptTemplate(
        input_variables=["ingredients"],
        template="""You are a professional chef and recipe creator.
        Given the following list of ingredients, create a delicious recipe.
        Do not consider difficult receipes. Focus on simple, delicious meals that can be made with common ingredients and in less time.
        Ingredients: {ingredients}

        Write the receipe with 
        - Receipe Name,
- Description, and
- Ingredients List (with quantities).
Return only the recipe details without any additional commentary or formatting.
        """,
    )
    formatted_prompt = recipe_prompt.format(ingredients=ingredients)
    logger.info("Sending prompt to llm")
    response = llm.invoke(formatted_prompt)
    
    logger.info("[Tool: suggest_recipe] Receipe suggested successfully")
    return response.content

@tool
def generate_cooking_steps(receipeList : list[str]) -> str:
    """
    Convert the recipe into numbered, beginner-friendly cooking steps with timings
    """
    logger.info(f"[Tool: generate_cooking_steps] Received receipeList: {receipeList}")

    cooking_steps_prompt = PromptTemplate(
        input_variables=["receipeList"],
        template="""You are a professional chef and recipe creator.
        You take a receipe name, description and the ingredients list as input and convert it into numbered, beginner-friendly cooking steps with timings.
    Rules:
    The receipe should be beginner-friendly, with clear instructions and timings for each step.
    The receipe should be broken down into 5-7 steps, each with a clear action and estimated time required.
    Do not include any additional commentary or formatting, just the steps with timings.
    
        ReceipeList: {receipeList}

        Write the receipe with 
        - Receipe Name,
        -Ingridients list along with quantities and
        - Number steps of receipe with timings
        """,
    )
    formatted_prompt = cooking_steps_prompt.format(receipeList=receipeList)
    logger.info("Sending prompt to llm")
    response=llm.invoke(formatted_prompt)
    logger.info("[Tool: generate_cooking_steps] Cooking steps generated successfully")
    return response.content

tools=[suggest_recipe, generate_cooking_steps]
logger.info(f"Tools registered: {[t.name for t in tools]}")
logger.info("Creating the agent...")
SystemPrompt=""" You are a receipe generator agent. Your job is to provide the user with simple beginner freindly receipes, 
that can be made from provide list of ingredients. You will also provide the cooking steps with timings for each step.
 When the user provides you the ingredients list, you will follow these steps:
 1. Use the suggest_recipe tool to generate a recipe based on the provided ingredients.
 2. Use the generate_cooking_steps tool to convert the recipe into numbered, beginner-friendly cooking steps with timings.
 3. Return the final receipe details along with the cooking steps to the user.
    Always follow the above steps in order and do not skip any step. First find suitable receipe and then generate cooking steps.

    """
agent_graph=create_agent(
    model=llm,
    tools=tools,
    system_prompt=SystemPrompt,
    debug=True,
)
logger.info("Agent created and ready to run!")


def run_recipe_generator(ingredients: list[str]) -> str:
    logger.info(f"USER'S List of Ingredients: {ingredients}")
    logger.info("=" * 60)
    logger.info("Agent is now thinking...and preparing a delicious receipe for you!")
    logger.info("-" * 60)
    result = agent_graph.invoke(
        {"messages": [HumanMessage(content=str(ingredients))]})
    
    final_receipe = result["messages"][-1].content

    logger.info("-" * 60)
    logger.info("Agent finished! Here's your receipe with cooking steps:")
    logger.info("-" * 60)
    return final_receipe

if __name__ == "__main__":
    while True:
        ingredientList = input("Enter a list of available ingredients at your home (comma separated): ").strip()

        if not ingredientList:
            print("Please enter a list of ingredients.\n")
            continue
        
        if ingredientList.lower() in ("q", "quit", "exit"):
            print("Exiting the Recipe Generator. Happy cooking!")
            break
        
        try:
            cooking_receipe = run_recipe_generator(ingredientList.split(","))
            print("\n" + "=" * 60)
            print("YOUR GENERATED RECIPE:")
            print("=" * 60)
            print(cooking_receipe)
            print("=" * 60 + "\n")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print("Sorry, something went wrong while generating the recipe. Please try again.\n")

    
                