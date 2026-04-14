# Receipe Generator Project

This use case creates a new receipe for you everytime you give a list of ingredients.
The agent makes use of (comma separted) user-provided ingredients list and serves a delicious step by step beginner friendly receipe.

## How It Works

```
Comma separated Ingredients list
       |
       v
  [Agent thinks: "I need to find a suitable receipe first"]
       |
       v
  [Tool: suggest_receipe] --> suggest a receipe with name, description and list of ingredients
       |
       v
  [Agent thinks: "Now I should generate a step by step cooking instruction for receipe"]
       |
       v
  [Tool: generate_cooking_steps] --> creates simple cooking steps along with timings
       |
       v
  Delicious receipe served
```

## Prerequisites

- Python 3.10 or higher
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/NisargKadam/Langchain_sample_project.git
cd Langchain_sample_project
```

### 2. Create a virtual environment

python -m venv .venv
```

Activate it:
  .venv\Scripts\Activate
 
### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy the example env file and add your real key:

OPENAI_API_KEY=sk-your-actual-key-here
```

## Run

```bash
python receipe_generator.py
```

You'll see an interactive prompt:

```
============================================================
  Enter a list of available ingredients at your home (comma separated):
============================================================

Give a list of ingredients, and the agent will
create a step by step cokking guide.

Type 'quit' or q or ok to exit.
## Example

**Input:**
```
 onion, capsicum, bread
```

**Output:**
```

============================================================
YOUR GENERATED RECIPE:
============================================================
## Capsicum & Onion Bread Toast

**Description:** A quick, flavorful toast made by sautéing capsicum and onions, then topping crispy bread.

### Ingredients
- Onion: 1 small, finely sliced
- Capsicum (bell pepper): 1 medium, thinly sliced
- Bread: 4 slices
- Salt: 1/2 tsp
- Black pepper: 1/4 tsp
- Olive oil (or any cooking oil): 2 tbsp
- Optional: chili flakes (or a pinch of chili powder): 1/4 tsp

### Cooking Steps (with timings)
1. **Slice the vegetables:** Finely slice the onion and thinly slice the capsicum. *(5 minutes)*
2. **Sauté the onion:** Heat the oil in a pan on **medium** heat. Add onion and cook until slightly soft and translucent, stirring often. *(3–4 minutes)*
3. **Cook the capsicum:** Add capsicum to the pan. Stir and cook until it softens and looks slightly glossy. *(4–5 minutes)*
4. **Season the mixture:** Add salt, black pepper, and optional chili flakes. Stir and cook 30–60 seconds more. *(1 minute)*
5. **Toast the bread:** Toast the bread slices until golden and crisp (toaster or dry pan). *(3–5 minutes)*
6. **Assemble & serve:** Spoon the warm onion-capsicum mixture on top of the toast. Serve immediately. *(1–2 minutes)*
============================================================

## Project Structure

```
.
├── RECIPE_GENERATOR.py   # Main agent code (fully commented)
├── requirements.txt     # Python dependencies
├── .env.example         # API key template
├── .gitignore           # Keeps secrets and venv out of git
└── README.md            # This file
```

## Tech Stack

- [LangChain](https://python.langchain.com/) - Framework for building LLM applications
- [OpenAI GPT-4o-mini](https://platform.openai.com/) - The LLM powering the agent
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management
