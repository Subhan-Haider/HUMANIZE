"""
Statistical Fingerprint Scrambler
Makes text statistically unique to avoid document similarity detection.
"""
import random
import re
import nltk

class FingerprintScrambler:
    """
    Scrambles statistical fingerprints to avoid similarity detection.
    """
    
    def __init__(self):
        # Extreme humanization tactics
        pass
    
    def add_personal_anecdotes(self, text, level=3):
        """
        Inject personal anecdotes/experiences throughout text.
        This makes it impossible for detectors to find similar documents.
        """
        anecdotes = [
            " I remember when I first learned about this - ",
            " This reminds me of something that happened last week - ",
            " My friend actually told me about this, and ",
            " I was just thinking about this the other day, ",
            " Funny story, but ",
            " This is kind of like when ",
        ]
        
        sentences = nltk.sent_tokenize(text)
        new_sents = []
        
        # Add anecdote every ~5 sentences
        for i, sent in enumerate(sentences):
            new_sents.append(sent)
            
            if i > 0 and i % 5 == 0 and random.random() < 0.3:
                anecdote = random.choice(anecdotes)
                # Create a mini personal story
                story_endings = [
                    "it made sense to me.",
                    "I got it.",
                    "things clicked.",
                    "I understood what they meant."
                ]
                full_anecdote = anecdote + random.choice(story_endings)
                new_sents.append(full_anecdote)
        
        return " ".join(new_sents)
    
    def extreme_style_variation(self, text):
        """
        Apply extreme style variations that no AI training data has.
        """
        # Random capitalization for emphasis (very human)
        words = text.split()
        for i in range(len(words)):
            if random.random() < 0.03 and len(words[i]) > 4:
                words[i] = words[i].upper()
        
        text = " ".join(words)
        
        # Add emoji occasionally (very casual/human)
        emojis = ["lol", "haha", "tbh", "ngl", "fr", "imo"]
        sentences = nltk.sent_tokenize(text)
        new_sents = []
        
        for sent in sentences:
            if random.random() < 0.08:
                sent = sent.rstrip('.!?') + " " + random.choice(emojis) + "."
            new_sents.append(sent)
        
        return " ".join(new_sents)
    
    def inject_unique_quirks(self, text):
        """
        Add unique writing quirks that are statistically rare.
        """
        # Double punctuation occasionally
        text = re.sub(r'\.(\s+[A-Z])', lambda m: '.. ' + m.group(1) if random.random() < 0.05 else '. ' + m.group(1), text)
        
        # Add parenthetical asides
        sentences = nltk.sent_tokenize(text)
        new_sents = []
        
        asides = [
            " (just my opinion though)",
            " (could be wrong)",
            " (not an expert or anything)",
            " (take that with a grain of salt)",
            " (ymmv)"
        ]
        
        for sent in sentences:
            if random.random() < 0.10:
                sent = sent.rstrip('.!?') + random.choice(asides) + "."
            new_sents.append(sent)
        
        return " ".join(new_sents)
    
    def scramble_fingerprint(self, text, level=5):
        """
        Apply maximum scrambling to create unique statistical fingerprint.
        """
        print(f"\n→ Scrambling statistical fingerprint (Level: {level})...")
        
        if level >= 3:
            text = self.add_personal_anecdotes(text, level=level)
            print(f"  ✓ Personal anecdotes added")
        
        if level >= 4:
            text = self.extreme_style_variation(text)
            print(f"  ✓ Extreme style variations applied")
        
        if level >= 5:
            text = self.inject_unique_quirks(text)
            print(f"  ✓ Unique quirks injected")
        
        print(f"  ✓ Fingerprint scrambling complete")
        return text


class SemanticShuffler:
    """
    Shuffles semantic content to break similarity patterns.
    """
    
    def shuffle_supporting_details(self, text):
        """
        Reorder supporting details within paragraphs.
        """
        paragraphs = text.split("\n\n")
        new_paragraphs = []
        
        for para in paragraphs:
            sentences = nltk.sent_tokenize(para)
            
            if len(sentences) > 3:
                # Keep first (topic) and last (conclusion)
                topic = sentences[0]
                conclusion = sentences[-1]
                middle = sentences[1:-1]
                
                # Shuffle middle sentences
                random.shuffle(middle)
                
                new_para = " ".join([topic] + middle + [conclusion])
                new_paragraphs.append(new_para)
            else:
                new_paragraphs.append(para)
        
        return "\n\n".join(new_paragraphs)
    
    def add_conversational_detours(self, text):
        """
        Add conversational detours/tangents (very human).
        """
        sentences = nltk.sent_tokenize(text)
        new_sents = []
        
        detours = [
            "Wait, let me back up a sec. ",
            "Actually, before I go on - ",
            "Okay so here's the thing. ",
            "Let me put it this way. ",
            "Alright, so "
        ]
        
        for i, sent in enumerate(sentences):
            # Occasionally add detour
            if i > 2 and random.random() < 0.12:
                new_sents.append(random.choice(detours) + sent)
            else:
                new_sents.append(sent)
        
        return " ".join(new_sents)
    
    def semantic_shuffle(self, text, aggressiveness=4):
        """
        Apply semantic shuffling.
        """
        print(f"\n→ Semantic shuffling (Aggressiveness: {aggressiveness})...")
        
        if aggressiveness >= 3:
            text = self.shuffle_supporting_details(text)
            print(f"  ✓ Details reordered")
        
        if aggressiveness >= 4:
            text = self.add_conversational_detours(text)
            print(f"  ✓ Conversational detours added")
        
        print(f"  ✓ Semantic shuffling complete")
        return text
