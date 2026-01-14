"""
Advanced Pattern Breaking System
Disrupts AI writing patterns at multiple levels.
"""
import re
import random
import nltk
from collections import Counter

class PatternBreaker:
    """
    Analyzes and breaks common AI writing patterns.
    """
    
    def __init__(self):
        self.ai_sentence_starters = [
            "It is important to", "It should be noted that", "One must consider",
            "It is essential to", "It is crucial that", "It is worth noting",
            "In order to", "With regard to", "Due to the fact that",
            "For the purpose of", "In light of", "Taking into account"
        ]
        
        self.ai_connectors = [
            "Additionally,", "Furthermore,", "Moreover,", "Subsequently,",
            "Consequently,", "Nevertheless,", "Nonetheless,", "Henceforth,"
        ]
        
    def break_sentence_patterns(self, text):
        """Break repetitive sentence structure patterns."""
        sentences = nltk.sent_tokenize(text)
        
        # Analyze sentence starts
        starts = [s.split()[0] if s.split() else "" for s in sentences]
        start_counts = Counter(starts)
        
        new_sentences = []
        for i, sent in enumerate(sentences):
            words = sent.split()
            if not words:
                new_sentences.append(sent)
                continue
                
            # If this start word is overused, vary it
            if start_counts[words[0]] > 2:
                alternatives = [
                    f"And {words[0].lower()}",
                    f"But {words[0].lower()}",
                    f"So {words[0].lower()}",
                    f"Well, {words[0].lower()}"
                ]
                if random.random() < 0.4:
                    sent = random.choice(alternatives) + " " + " ".join(words[1:])
            
            new_sentences.append(sent)
        
        return " ".join(new_sentences)
    
    def inject_statistical_noise(self, text):
        """
        Inject statistical noise to break n-gram patterns.
        """
        words = text.split()
        
        # Randomly swap adjacent words (10% of time)
        i = 0
        while i < len(words) - 1:
            if random.random() < 0.10 and len(words[i]) > 3 and len(words[i+1]) > 3:
                # Swap
                words[i], words[i+1] = words[i+1], words[i]
                i += 2
            else:
                i += 1
        
        # Insert random contractions
        contractions = {
            "do not": "don't", "cannot": "can't", "will not": "won't",
            "should not": "shouldn't", "would not": "wouldn't",
            "is not": "isn't", "are not": "aren't", "it is": "it's",
            "that is": "that's", "there is": "there's"
        }
        
        text = " ".join(words)
        for formal, casual in contractions.items():
            if random.random() < 0.6:
                text = text.replace(formal, casual)
        
        return text
    
    def break_paragraph_symmetry(self, text):
        """
        Break overly symmetric paragraph structures.
        """
        paragraphs = text.split("\n\n")
        
        # Merge some short paragraphs
        new_paragraphs = []
        i = 0
        while i < len(paragraphs):
            para = paragraphs[i]
            
            # If very short and not last, maybe merge
            if i < len(paragraphs) - 1 and len(para.split()) < 20 and random.random() < 0.3:
                merged = para + " " + paragraphs[i+1]
                new_paragraphs.append(merged)
                i += 2
            else:
                new_paragraphs.append(para)
                i += 1
        
        return "\n\n".join(new_paragraphs)
    
    def add_natural_errors(self, text, error_rate=0.03):
        """
        Add natural human errors (missing spaces, extra spaces).
        """
        if random.random() > error_rate:
            return text
        
        # Occasionally remove space after comma
        text = re.sub(r', (\w)', lambda m: ',' + m.group(1) if random.random() < 0.15 else ', ' + m.group(1), text)
        
        # Occasionally add double space
        text = re.sub(r' (\w)', lambda m: '  ' + m.group(1) if random.random() < 0.05 else ' ' + m.group(1), text)
        
        return text
    
    def comprehensive_pattern_break(self, text, aggressiveness=3):
        """
        Apply all pattern-breaking techniques.
        
        Args:
            text: Input text
            aggressiveness: 1-5 scale
        """
        print(f"→ Breaking AI patterns (Aggressiveness: {aggressiveness})...")
        
        # Always break sentence patterns
        text = self.break_sentence_patterns(text)
        
        # Statistical noise based on aggressiveness
        if aggressiveness >= 2:
            text = self.inject_statistical_noise(text)
        
        # Break paragraph symmetry
        if aggressiveness >= 3:
            text = self.break_paragraph_symmetry(text)
        
        # Natural errors at high aggressiveness
        if aggressiveness >= 4:
            text = self.add_natural_errors(text, error_rate=0.05)
        
        print(f"  ✓ Pattern breaking complete")
        return text


class NgramDiversifier:
    """
    Ensures high n-gram diversity (anti-AI signature).
    """
    
    def calculate_ngram_diversity(self, text, n=3):
        """
        Calculate n-gram diversity score.
        Higher = more diverse = more human-like
        """
        words = text.lower().split()
        if len(words) < n:
            return 0
        
        ngrams = [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]
        unique_ngrams = len(set(ngrams))
        total_ngrams = len(ngrams)
        
        diversity = unique_ngrams / total_ngrams if total_ngrams > 0 else 0
        return diversity
    
    def enforce_diversity(self, text, target_diversity=0.85, max_attempts=3):
        """
        Rewrite until n-gram diversity target is met.
        """
        print(f"\n→ Enforcing n-gram diversity (Target: {target_diversity:.2%})...")
        
        current_diversity = self.calculate_ngram_diversity(text)
        print(f"  Initial diversity: {current_diversity:.2%}")
        
        if current_diversity >= target_diversity:
            print(f"  ✓ Already meets target")
            return text
        
        # Try to improve by replacing repeated phrases
        for attempt in range(max_attempts):
            words = text.split()
            
            # Find repeated trigrams
            trigrams = [tuple(words[i:i+3]) for i in range(len(words) - 2)]
            trigram_counts = Counter(trigrams)
            
            # Replace most common one
            most_common = trigram_counts.most_common(1)
            if most_common and most_common[0][1] > 1:
                target_trigram = most_common[0][0]
                
                # Find and replace with variation
                text_parts = text.split()
                for i in range(len(text_parts) - 2):
                    if tuple(text_parts[i:i+3]) == target_trigram and random.random() < 0.5:
                        # Add variation
                        text_parts.insert(i+1, random.choice(["actually", "kind of", "basically"]))
                        break
                
                text = " ".join(text_parts)
            
            new_diversity = self.calculate_ngram_diversity(text)
            print(f"  Attempt {attempt + 1}: {new_diversity:.2%}")
            
            if new_diversity >= target_diversity:
                print(f"  ✓ Target reached")
                break
        
        return text
