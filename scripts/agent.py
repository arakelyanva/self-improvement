import os
from dotenv import load_dotenv
from google import genai
from github import Auth as GithubAuth, Github, GithubException

load_dotenv()

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

github_auth   = GithubAuth.Token(os.getenv("GH_ACCESS_TOKEN"))
github_client = Github(auth=github_auth)

REPO_NAME = "arakelyanva/self-improvement"
FILE_PATH = "app.py"
BRANCH = "main"

MODEL='gemini-3.1-flash-lite'

try:
    repo = github_client.get_repo(REPO_NAME)
    file_contents = repo.get_contents(FILE_PATH, ref=BRANCH)
    original_code = file_contents.decoded_content.decode("utf-8")

    # Main Prompt
    prompt = f"""
    Analyze and improve the following Python code.
    Optimize performance, fix bugs, and ensure standard PEP 8 styling.
    Return ONLY the raw executable python code. Do not include markdown code blocks (```python) or explanations.

    Code to adjust:
    {original_code}
    """

    print("[LLM] Sending code to Gemini for adjustments...")
    response = gemini_client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    adjusted_code = response.text.strip()

    print("[GIT] Committing adjusted code to GitHub...")

    if adjusted_code == original_code:
        print("[GIT] No changes have been made, nothing to commit.")
    else:
        repo.update_file(
            path=FILE_PATH,
            message="improvement: automated code optimization by Gemini LLM",
            content=adjusted_code,
            sha=file_contents.sha,
            branch=BRANCH
        )
        print("[GIT] Successfully committed adjustments!")

except GithubException as ge:
    print(f"[ERROR] GitHub Error: {ge}")
except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")

