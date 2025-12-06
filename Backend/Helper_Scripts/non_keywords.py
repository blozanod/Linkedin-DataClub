# File contains all current non keywords for parsing

import nltk
from nltk.corpus import stopwords

# Download stopwords and punkt if not already downloaded
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# NLTK Stopwords
english_stopwords = stopwords.words('english')

# Additional non keywords
MASTER_NON_KEYWORDS = {

    # Generic filler verbs (non-skills)
    "work", "assist", "help", "support", "contribute", "collaborate",
    "communicate", "ensure", "maintain", "provide", "perform",
    "implement", "utilize", "use", "conduct", "handle", "complete",
    "coordinate", "deliver", "manage", "lead", "oversee",

    # Generic nouns / contextless words
    "team", "department", "organization", "company", "agency", "client",
    "customer", "user", "personnel", "staff", "employee", "management",
    "leadership", "stakeholder", "individual", "people", "project",
    "task", "responsibility", "role", "duty", "objective", "goal",
    "outcome", "procedure", "process", "initiative", "environment",
    "background", "experience", "qualification", "career",

    # Resume-fluff adjectives
    "strong", "excellent", "great", "motivated", "dedicated", "committed",
    "hardworking", "reliable", "dynamic", "flexible", "adaptable",
    "creative", "proactive", "effective", "efficient",

    # Connectors / modifiers / useless adverbs
    "based", "include", "various", "several", "multiple", "such",
    "particularly", "primarily", "mostly", "often", "typically",
    "usually", "generally", "highly", "widely", "common",

    # Temporal junk
    "currently", "previously", "former", "past", "ongoing", "throughout",
    "during", "after", "before", "since", "until", "while", "per", "via",
    "across", "within", "between", "among", "recent", "recently",

    # Pronouns
    "i", "me", "my", "we", "us", "our", "they", "them", "their",
    "he", "she", "you",

    # Non-skill verbs (generic actions)
    "make", "improve", "achieve", "contribute", "allow", "enable",

    # Numbers / quantities (contextless)
    "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "ten", "percent", "year", "month", "week",
    "hour", "minute", "time",

    # General determiners / connectors / high-frequency words
    "ability", "able", "according", "addition", "almost", "also",
    "although", "another", "area", "case", "certain", "come",
    "entire", "especially", "expected", "given", "however",
    "kind", "likely", "maybe", "near", "next", "possible",
    "present", "probably", "quite", "rather", "soon", "though",
    "unless", "yet", "different",

    # Junk / punctuation
    ".", ",", ":", ";", "/", "?", "&", "!", " ", "*", "_",
    "-", "—", "(", ")", "#"
}


MASTER_NON_KEYWORDS.update(english_stopwords)