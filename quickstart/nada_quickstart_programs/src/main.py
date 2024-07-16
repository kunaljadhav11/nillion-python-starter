from nada_dsl import *

def nada_main():
    # Set up parties
    author = Party(name="Author")
    reviewers = [Party(name=f"Reviewer{i}") for i in range(3)]
    committee = Party(name="Committee")
    
    # Inputs
    paper_quality = SecretFixed(Input(name="paper_quality", party=author))
    reviews = [SecretFixed(Input(name=f"review{i}", party=reviewers[i])) for i in range(3)]
    
    # Computation
    one_third = Fixed(1) / Fixed(3)
    avg_review = (reviews[0] + reviews[1] + reviews[2]) * one_third
    
    # Check if any review is significantly different from others
    threshold = Fixed(3)  # Significance threshold
    outlier_checks = [abs(reviews[i] - avg_review) > threshold for i in range(3)]
    
    # Calculate final score, excluding potential outliers
    final_score = avg_review
    for i in range(3):
        final_score = outlier_checks[i].if_else(
            (final_score * Fixed(3) - reviews[i]) * Fixed(0.5),  # Exclude outlier
            final_score
        )
    
    # Compare with author's self-assessment
    assessment_diff = abs(final_score - paper_quality)
    realistic_assessment = assessment_diff <= Fixed(2)
    
    # Outputs
    outputs = [
        Output(final_score, "final_score", committee),
        Output(realistic_assessment, "realistic_self_assessment", author)
    ]
    
    for i in range(3):
        outputs.append(Output(outlier_checks[i], f"reviewer{i}_outlier", committee))
    
    return outputs