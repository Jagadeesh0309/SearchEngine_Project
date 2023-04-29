import re

class PreProcessor:
    def __init__(self):
        with open("stopwords.txt", "r") as f:
            self.StopWords = set(f.read().splitlines())
        self.patterns = [
            re.compile(r"<!--.*?-->", re.DOTALL),
            re.compile(r"(?is)<(head|style|script).*?>.*?</\1>(\s)*.*?>", re.DOTALL),
            re.compile(r"<[^>]+>", re.DOTALL),
            re.compile(r"&[^\\s].+?;", re.DOTALL),
            re.compile(r"[^a-zA-Z0-9\s]+", re.DOTALL)
        ]
        self.url_pattern = re.compile(r"https?:\S+|www\.\S+")
        self.word_pattern = re.compile(r"(?i)(?<![a-z])\b[a-z]+|[a-z]+(?=[A-Z]|$)")

    def DocumentClean(self, text):
        for pattern in self.patterns:
            text = pattern.sub(" ", text)
        text = self.url_pattern.sub(" ", text)
        
        words = self.word_pattern.findall(text.lower())
        words = [word for word in words if word.lower() not in self.StopWords]

        return " ".join(words)
