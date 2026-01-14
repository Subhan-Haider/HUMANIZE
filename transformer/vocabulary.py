import random
import os
from textblob import Word
from nltk.corpus import wordnet

class VocabularyEnhancer:
    """
    Enhanced vocabulary replacement using multiple synonym sources and contextual augmentation.
    """
    
    def __init__(self):
        # Download WordNet if not available
        try:
            wordnet.synsets('test')
        except:
            import nltk
            nltk.download('wordnet', quiet=True)
            nltk.download('omw-1.4', quiet=True)
            
        # Optional: Initialize nlpaug if available
        self.aug = None
        # Use a class-level or module-level flag to only warn once
        if not hasattr(VocabularyEnhancer, '_warned_nlpaug'):
            try:
                import nlpaug.augmenter.word as naw
                # Using ContextualWordEmbsAug for real-time synonym replacement
                self.aug = naw.ContextualWordEmbsAug(
                    model_path='distilbert-base-uncased', 
                    action="substitute",
                    device='cpu'
                )
                print("NLP Augmentation model loaded.")
            except ImportError:
                # Silently fail if not installed, or print just once
                pass
            except Exception as e:
                # Only print other errors once
                print(f"NLP Augmentation (nlpaug) setup: {e}")
            VocabularyEnhancer._warned_nlpaug = True

    def get_synonyms(self, word, pos=None):
        """
        Get synonyms from multiple sources.
        """
        synonyms = set()
        
        # Method 1: WordNet
        try:
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    synonym = lemma.name().replace('_', ' ')
                    if synonym.lower() != word.lower():
                        synonyms.add(synonym)
        except:
            pass
        
        # Method 2: TextBlob
        try:
            word_obj = Word(word)
            for syn_set in word_obj.synsets:
                for lemma in syn_set.lemmas():
                    synonym = lemma.name().replace('_', ' ')
                    if synonym.lower() != word.lower():
                        synonyms.add(synonym)
        except:
            pass
        
        return list(synonyms)
    
    def replace_word_with_synonym(self, word, preserve_case=True):
        """
        Replace a word with a random synonym.
        """
        synonyms = self.get_synonyms(word.lower())
        
        if not synonyms:
            return word
        
        # Filter out very different synonyms (length difference)
        similar_synonyms = [s for s in synonyms if abs(len(s) - len(word)) <= 4]
        
        if not similar_synonyms:
            similar_synonyms = synonyms
        
        # Pick random synonym
        replacement = random.choice(similar_synonyms)
        
        # Preserve case
        if preserve_case:
            if word.isupper():
                replacement = replacement.upper()
            elif word[0].isupper():
                replacement = replacement.capitalize()
        
        return replacement
    
    def context_aware_augment(self, text, level=3):
        """
        Use nlpaug for contextual word replacement.
        """
        if self.aug and level >= 3:
            try:
                # Augment text contextually
                aug_text = self.aug.augment(text)
                return aug_text[0] if isinstance(aug_text, list) else aug_text
            except:
                return text
        return text

    def smart_synonym_replacement(self, text, replacement_rate=0.15):
        """
        Intelligently replace words with synonyms.
        """
        # First try context-aware augmentation if it's a high level
        # This is handled in the main engine, but adding a hook here
        
        # Skip very common words
        skip_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
            'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
            'why', 'how', 'can', 'could', 'will', 'would', 'should', 'may', 'might'
        }
        
        words = text.split()
        result = []
        
        for word in words:
            clean_word = word.strip('.,!?;:"\'-')
            
            if (len(clean_word) < 4 or 
                clean_word.lower() in skip_words or 
                random.random() > replacement_rate):
                result.append(word)
                continue
            
            synonyms = self.get_synonyms(clean_word)
            if synonyms:
                prefix = word[:len(word) - len(word.lstrip('"\'-'))]
                suffix = word[len(word.rstrip('.,!?;:"\'-')):]
                
                replacement = self.replace_word_with_synonym(clean_word)
                result.append(prefix + replacement + suffix)
            else:
                result.append(word)
        
        return ' '.join(result)

# Global instance
vocab_enhancer = VocabularyEnhancer()

