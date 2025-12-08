from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session as SessionType
from .classes import Posting, Resume, Session_Posting, Session_Resume
from .queries import get_all_postings
from .non_keywords import MASTER_NON_KEYWORDS
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Get resume from resumes.db
# getResume() copy pasted from user_prompt.py
def getResume():
    stmt = select(Resume.ID, Resume.Resume_str
                  ).where(Resume.Resume_str.contains("Software Engineer") # For now its targeting software engineers in database
                  ).order_by(func.random())
    
    with Session_Resume() as session:
      arr = session.execute(stmt).first()

    return arr[1]

def clean_text(text: str) -> str:
    text = RE_URL.sub(" ", text)
    text = RE_EMAIL.sub(" ", text)
    text = RE_TAG.sub(" ", text)
    text = text.encode("ascii", "ignore").decode()  # remove unicode junk
    return text.lower()

def filter_keywords(text):
    text = clean_text(text)
    word_tokens = nlp(text.lower())
    
    # First pass - remove junk
    filtered_words = []

    for token in word_tokens:
        if token.is_punct or token.is_space or r"\x" in token.text or r"\u" in token.text:
            continue

        lemma = token.lemma_.lower()

        if lemma in MASTER_NON_KEYWORDS:
            continue

        filtered_words.append(token.text)
    
    # Second pass - find phrases
    doc = nlp(" ".join(filtered_words))
    skills = set()
    phrases = set()

    # Find skills
    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip().lower()
        if len(phrase.split()) > 1:
            skills.add(phrase)
    
    # Find compound terms
    for token in doc:
        if token.dep_ == "compound":
            compound = f"{token.text} {token.head.text}"
            skills.add(compound)

    # Find verb-object pairs
    for token in doc:
        if token.pos_ == "VERB":
            # Look for its direct object
            for child in token.children:
                if child.dep_ == "dobj":
                    phrase = f"{token.text} {child.text}"
                    phrases.add(phrase)
                    
    return list(filtered_words) + list(skills) + list(phrases)

# TODO: Calculate similarity score between resume and posting keywords
def match(resume, posting):
    # Normalize inputs into strings. `resume` and `posting` may be lists
    # (keywords), but can also be None or plain strings depending on DB state.
    if isinstance(resume, (list, tuple)):
        resume_str = " ".join([str(x) for x in resume])
    else:
        resume_str = str(resume or "")

    if isinstance(posting, (list, tuple)):
        posting_str = " ".join([str(x) for x in posting])
    elif isinstance(posting, str):
        posting_str = posting
    elif posting is None:
        posting_str = ""
    else:
        # Fallback: try to coerce to list-like, else stringify
        try:
            posting_str = " ".join([str(x) for x in posting])
        except Exception:
            posting_str = str(posting)

    # Vectorize strings
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_str, posting_str])

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return cosine_sim

def parse(index, resume_body):
    # Get jobs and resume
    resume_keywords = filter_keywords(resume_body)

    # 2D array with each item being key-value pair: [job_id, match_score]
    # this way, the scores array can be referenced, once sorted, to order the jobs
    # that best match the resume and display them on the website
    scores = [] 

    with Session_Posting() as session:
        company_postings = get_all_postings(session)
         
        # For each selected job, check if it has already been cleaned of non keywords
        # if it has not been cleaned, clean it. Else, skip.
        for posting in company_postings:
            # Ensure keyword fields are lists so matching code can join them safely
            if not posting.keywords or not isinstance(posting.keywords, list):
                posting.keywords = filter_keywords(posting.description or "")

            # Score resume against current job
            if not posting.title_keywords or not isinstance(posting.title_keywords, list):
                posting.title_keywords = filter_keywords(posting.title or "")

            if not posting.tags_keywords or not isinstance(posting.tags_keywords, list):
                tags_text = " ".join(posting.tags) if (posting.tags and isinstance(posting.tags, list)) else ""
                posting.tags_keywords = filter_keywords(tags_text)

            raw_scores = [
                match(resume_keywords, posting.keywords),
                match(resume_keywords, posting.title_keywords),
                match(resume_keywords, posting.tags_keywords)
            ]

            score = raw_scores[0] + 5 * raw_scores[1] + 3 * raw_scores[2]

            scores.append([posting.job_id, score])
            print(f"Finished processing job: {posting.job_id}")

        # Save updated postings to database (to be able to skip filtering job descriptions on other runs)
        session.commit()

    # Sort scores
    scores.sort(key=lambda row:row[1], reverse=True)

    # Package top 20 jobs into JSON file
    start = index * 20
    end = len(scores)

    top_job_ids = [scores[i][0] for i in range(start, end)]

    stmt = select(Posting.company_name, Posting.title, Posting.description, Posting.location, Posting.max_salary, Posting.tags
                    ).where(Posting.job_id.in_(top_job_ids) # Select from job_ids
                    )

    with Session_Posting() as session:
        stmt = select(Posting).where(
        Posting.job_id.in_(top_job_ids))

        postings = session.execute(stmt).scalars().all()

    # Preserve the order from top_job_ids (most similar -> least similar).
    # SQL IN() does not guarantee order, so build a lookup and re-order.
    posting_map = {p.job_id: p for p in postings}
    ordered_postings = [posting_map[jid] for jid in top_job_ids if jid in posting_map]

    json_items = [p.to_dict() for p in ordered_postings]
    return json_items


# Tag filters exposed for frontend
# These are the canonical tags we use when collecting postings and exposing
# tag-based filters in the frontend. The frontend currently extracts the
# available tags from the `tags` property of each job object returned by
# the `/get_jobs` API; this constant documents the intended set and can be
# used by other tooling if you want a fixed whitelist of filters.
TAG_FILTERS = [
    "software", "engineering", "engineer", "developer", "tech", "it",
    "product", "operations", "manager", "senior", "junior",
    "management", "consulting", "finance", "financial", "accounting",
    "legal", "hr", "recruiting", "admin", "intern", "internship",
    "sales", "marketing", "growth", "customer-support",
    "support", "writing", "copywriting", "content",
    "design", "creative", "ui-ux", "media", "video", "editor",
    "analytics", "qa", "security", "health", "healthcare", "medical",
    "education", "teaching", "trainer", "architect",
    "logistics", "supply-chain", "manufacturing", "hardware",
]


nlp = spacy.load("en_core_web_sm")
RE_URL = re.compile(r'https?://\S+')
RE_EMAIL = re.compile(r'\S+@\S+')
RE_TAG = re.compile(r'[A-Za-z0-9+/=]{20,}')

if __name__ == "__main__":
    resume_body = getResume() # Contains Full Resume Text

    json_items = parse(index=0, resume_body=resume_body, user_keyword="is")
    print(json_items[0])