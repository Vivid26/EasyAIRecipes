import subprocess
import json
import re

def create_prompt(ingredients):
    return f"""
You are an expert chef assistant. Based on the following ingredients, generate a structured JSON response representing a recipe.

Ingredients: {ingredients}

Return only a JSON object with the following fields:
- title (string): Title of the recipe
- prep_time (string): Preparation time (e.g., "30 minutes")
- servings (string): Number of servings (e.g., "2-4 people")
- ingredients (array of strings): List of ingredients with quantity and units
- steps (array of strings): Step-by-step instructions
- tips (array of strings): Tips or variations

Return ONLY a valid JSON object as a response, with no explanation, markdown, or extra text."""

def generate_recipe(ingredients):
    prompt = create_prompt(ingredients)

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2", prompt],
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",  # Forces decoding with UTF-8
            timeout=30
        )
        if result.returncode != 0:
            return {"error": result.stderr}

        # Try to find the JSON part in the output
        output = result.stdout.strip()
        #print("OLLAMA OUTPUT:", repr(output))

        # Clean and extract JSON using regex
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            json_data = json.loads(json_match.group())
            return json_data
        else:
            return {"error": "Failed to extract JSON from Ollama output."}

    except subprocess.CalledProcessError as e:
        return {"error": f"Ollama command failed: {e.stderr}"}
    except subprocess.TimeoutExpired:
        return {"error": "Ollama took too long to respond. Try again later."}
    except json.JSONDecodeError:
        return {"error": "Failed to decode JSON from Ollama's output."}
    except Exception as e:
        return {"error": str(e)}