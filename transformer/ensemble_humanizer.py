"""
Multi-Model Ensemble Humanizer
Uses multiple paraphrasing models for superior results.
"""
import random
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class EnsembleHumanizer:
    """
    Uses multiple paraphrasing models and combines their outputs.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models = []
        
        # Load multiple paraphrase models
        print("Loading ensemble models...")
        
        try:
            # Model 1: T5-based paraphraser
            print("  Loading T5 paraphraser...")
            self.models.append({
                "name": "T5-Paraphrase",
                "tokenizer": AutoTokenizer.from_pretrained("Vamsi/T5_Paraphrase_Paws"),
                "model": AutoModelForSeq2SeqLM.from_pretrained("Vamsi/T5_Paraphrase_Paws").to(self.device)
            })
        except Exception as e:
            print(f"  Failed to load T5: {e}")
        
        try:
            # Model 2: Pegasus paraphraser
            print("  Loading Pegasus paraphraser...")
            self.models.append({
                "name": "Pegasus",
                "tokenizer": AutoTokenizer.from_pretrained("tuner007/pegasus_paraphrase"),
                "model": AutoModelForSeq2SeqLM.from_pretrained("tuner007/pegasus_paraphrase").to(self.device)
            })
        except Exception as e:
            print(f"  Failed to load Pegasus: {e}")
        
        print(f"✓ Loaded {len(self.models)} models")
    
    def paraphrase_with_model(self, text, model_info, num_variations=3):
        """
        Paraphrase text using a specific model.
        """
        try:
            tokenizer = model_info["tokenizer"]
            model = model_info["model"]
            
            # Tokenize
            inputs = tokenizer(
                f"paraphrase: {text}",
                return_tensors="pt",
                max_length=512,
                truncation=True
            ).to(self.device)
            
            # Generate variations
            outputs = model.generate(
                **inputs,
                max_length=512,
                num_return_sequences=num_variations,
                num_beams=num_variations,
                temperature=1.5,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                no_repeat_ngram_size=3
            )
            
            # Decode
            variations = [
                tokenizer.decode(output, skip_special_tokens=True)
                for output in outputs
            ]
            
            return variations
        except Exception as e:
            print(f"  Error with {model_info['name']}: {e}")
            return [text]
    
    def ensemble_paraphrase(self, text, num_variations=5):
        """
        Generate multiple variations using all models and pick best.
        """
        if not self.models:
            print("  No models available")
            return text
        
        print(f"  Generating {num_variations} variations with ensemble...")
        
        all_variations = []
        
        # Get variations from each model
        for model_info in self.models:
            variations = self.paraphrase_with_model(text, model_info, num_variations=2)
            all_variations.extend(variations)
        
        # Remove duplicates and original
        unique_variations = list(set([v for v in all_variations if v != text]))
        
        if not unique_variations:
            return text
        
        # Pick one randomly (introduces randomness)
        selected = random.choice(unique_variations)
        print(f"  ✓ Selected variation from {len(unique_variations)} options")
        
        return selected


class MarkovTextBlender:
    """
    Uses Markov chains to blend human text patterns.
    """
    
    def __init__(self):
        try:
            import markovify
            self.markovify = markovify
            self.enabled = True
        except ImportError:
            print("Markovify not available")
            self.enabled = False
    
    def blend_with_corpus(self, text, corpus_text=None):
        """
        Blend AI text with Markov-generated text from human corpus.
        """
        if not self.enabled:
            return text
        
        if not corpus_text:
            # Use a generic human-like corpus
            corpus_text = """
I think this is really interesting. You know, when I first heard about it, 
I wasn't sure what to make of it. But the more I looked into it, the more 
it made sense. Like, honestly, it's kind of obvious once you get it.
I mean, not everyone would agree with me on this. Some people think 
differently, and that's fine. Everyone's entitled to their opinion.
Anyway, what I'm trying to say is that this stuff matters. It really does.
Not in a dramatic way or anything, just in a practical sense.
            """
        
        try:
            # Build Markov model from corpus
            model = self.markovify.Text(corpus_text, state_size=2)
            
            # Generate some sentences
            markov_sentences = []
            for _ in range(3):
                sentence = model.make_sentence(tries=100)
                if sentence:
                    markov_sentences.append(sentence)
            
            if not markov_sentences:
                return text
            
            # Blend: Insert Markov sentences randomly
            import nltk
            original_sentences = nltk.sent_tokenize(text)
            
            # Insert 1-2 Markov sentences
            for markov_sent in markov_sentences[:2]:
                insert_pos = random.randint(0, len(original_sentences))
                original_sentences.insert(insert_pos, markov_sent)
            
            blended = " ".join(original_sentences)
            print(f"  ✓ Blended with Markov-generated text")
            return blended
            
        except Exception as e:
            print(f"  Markov blending failed: {e}")
            return text


class StatisticalAnalyzer:
    """
    Analyzes text statistics to measure human-likeness.
    """
    
    def analyze_readability(self, text):
        """
        Analyze readability scores.
        """
        try:
            from readability import Readability
            r = Readability(text)
            
            flesch = r.flesch()
            gunning_fog = r.gunning_fog()
            
            return {
                "flesch_score": flesch.score,
                "gunning_fog": gunning_fog.score,
                "grade_level": flesch.grade_level
            }
        except Exception as e:
            print(f"  Readability analysis failed: {e}")
            return None
    
    def analyze_word_frequency(self, text):
        """
        Analyze word frequency distribution.
        """
        try:
            from wordfreq import word_frequency
            import nltk
            
            words = nltk.word_tokenize(text.lower())
            
            # Calculate average word frequency
            freqs = [word_frequency(w, 'en') for w in words if w.isalpha()]
            avg_freq = sum(freqs) / len(freqs) if freqs else 0
            
            # AI text tends to use more common words (higher freq)
            # Human text uses more varied vocabulary (lower freq)
            
            return {
                "avg_word_frequency": avg_freq,
                "human_score": 1.0 - min(avg_freq * 100, 1.0)  # Lower freq = more human
            }
        except Exception as e:
            print(f"  Word frequency analysis failed: {e}")
            return None
