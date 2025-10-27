
import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV")
def main():
    if env == "prod":
        uvicorn.run("app.main:app", host="0.0.0.0", port=80)
    else:
        uvicorn.run("app.main:app", host="0.0.0.0", port=80, reload=True)

if __name__ == "__main__":
    main()