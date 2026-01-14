"""
Download required NLTK data packages.
Run this once after installing requirements.
"""
import nltk

print("Downloading NLTK data packages...")
nltk.download('punkt', quiet=False)
nltk.download('averaged_perceptron_tagger', quiet=False)
nltk.download('wordnet', quiet=False)
print("✓ NLTK data downloaded successfully!")
