import os

import uvicorn

if __name__ == "__main__":
    print("Starting server...", os.getenv("OPENAI_API_KEY"))

    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)
