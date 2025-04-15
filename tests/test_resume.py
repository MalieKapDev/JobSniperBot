import sys
import os

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.config import get_clean_resume_text

text = get_clean_resume_text()
print(text)