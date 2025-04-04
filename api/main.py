from fastapi import FastAPI, File, Form, UploadFile
import together
import pandas as pd
import zipfile
import io
import os

# Initialize FastAPI app
app = FastAPI()

# Set Together AI API Key (Make sure it's set in Vercel Environment Variables)
together.api_key = os.getenv("TOGETHER_API_KEY")

@app.post("/api/")
async def solve_question(question: str = Form(...), file: UploadFile = File(None)):
    """
    Handles question processing and optional file parsing.
    """
    extracted_data = None
    
    # If file is provided, extract relevant data
    if file:
        extracted_data = await process_file(file)
    
    # Generate answer using Together AI
    answer = get_answer(question, extracted_data)
    
    return {"answer": answer}


def get_answer(question: str, extracted_data: str = None):
    """
    Calls Together AI's model to get an answer.
    """
    prompt = f"Question: {question}\n"
    if extracted_data:
        prompt += f"Extracted Data: {extracted_data}\n"
    
    response = together.Complete.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        prompt=prompt,
        max_tokens=100
    )
    
    return response["output"]


async def process_file(file: UploadFile):
    """
    Extracts CSV content from uploaded ZIP file.
    """
    contents = await file.read()
    with zipfile.ZipFile(io.BytesIO(contents), "r") as z:
        for filename in z.namelist():
            if filename.endswith(".csv"):
                with z.open(filename) as csvfile:
                    df = pd.read_csv(csvfile)
                    return df.to_string()
    return None

# Run FastAPI with Uvicorn (Only for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
