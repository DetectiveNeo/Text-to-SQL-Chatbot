from src.llm.pipeline import nl2sql

if __name__ == "__main__":
    
    user_prompt = "What is the total unit cost for different delivery regions in orders table?"

    print(user_prompt)

    result = nl2sql(user_prompt)

    print(result)

