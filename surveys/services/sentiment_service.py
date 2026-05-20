from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def calculate_hybrid_sentiment(feedback_data: dict) -> dict:
    """
    Calculates a hybrid sentiment score using Text (50%), Ratings (40%), 
    and Recommendation (10%). All values are normalized to a -1.0 to 1.0 scale.
    """
    analyzer = SentimentIntensityAnalyzer()

    # ==========================================
    # 1. TEXT SENTIMENT (VADER) - 50% Weight
    # ==========================================
    pos_text = feedback_data.get('positive_feedback', '').strip()
    imp_text = feedback_data.get('improvement_feedback', '').strip()
    
    # Calculate text components separately so they don't corrupt each other
    pos_score = analyzer.polarity_scores(pos_text)["compound"] if pos_text else 0.0
    imp_score = analyzer.polarity_scores(imp_text)["compound"] if imp_text else 0.0
    
    # Average the text sentiments together
    if pos_text and imp_text:
        text_score = (pos_score + imp_score) / 2
    elif pos_text:
        text_score = pos_score
    else:
        text_score = imp_score

    # ==========================================
    # 2. RATING SENTIMENT - 40% Weight
    # ==========================================
    ratings = [
        feedback_data.get('teaching_quality', 3),
        feedback_data.get('course_content', 3),
        feedback_data.get('engagement', 3),
        feedback_data.get('overall_satisfaction', 3)
    ]
    avg_rating = sum(ratings) / len(ratings)
    
    # Math mapping: 5 -> 1.0 | 3 -> 0.0 | 1 -> -1.0
    rating_score = ((avg_rating - 1) / 2) - 1.0

    # ==========================================
    # 3. RECOMMENDATION SENTIMENT - 10% Weight
    # ==========================================
    recommendation = feedback_data.get('would_recommend')
    rec_score = 0.0
    has_rec = False
    
    if recommendation is True:
        rec_score = 1.0
        has_rec = True
    elif recommendation is False:
        rec_score = -1.0
        has_rec = True

    # ==========================================
    # 4. FINAL HYBRID CALCULATION
    # ==========================================
    if has_rec:
        final_score = (text_score * 0.5) + (rating_score * 0.4) + (rec_score * 0.1)
    else:
        final_score = (text_score * 0.555) + (rating_score * 0.444)

    # ==========================================
    # 5. NEW ADAPTIVE HYBRID THRESHOLDS
    # ==========================================
    # Widening the neutral boundary accommodates star-rating weight shifts.
    if final_score >= 0.30:
        label = "POSITIVE"
    elif final_score <= -0.30:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"

    return {
        "score": round(final_score, 4),
        "label": label
    }