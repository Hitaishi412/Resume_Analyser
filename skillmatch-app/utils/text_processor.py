from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compare(resume_tokens, job_description):
    """
    Calculates the similarity between the resume and job description using TF-IDF and cosine similarity.
    Returns a float between 0 and 1.
    """
    # Join tokens back into a full string for TF-IDF
    resume_text = " ".join(resume_tokens)
    
    # Prepare the corpus for TF-IDF: [resume, job description]
    corpus = [resume_text, job_description]

    # Initialize vectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Compute cosine similarity between the two documents
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return float(similarity_score[0][0])
