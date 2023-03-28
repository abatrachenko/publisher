import json

def generate_title_tag(main_question):
    return f"{main_question}"

def generate_meta_description(main_question, related_questions):
    return f"Learn about {main_question} and related questions: {', '.join(related_questions[:3])}, and more."

def create_json_ld_markup(main_question, related_questions, answers):
    faq_data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": []}

    main_entity = {
        "@type": "Question",
        "name": main_question,
        "acceptedAnswer": {
            "@type": "Answer",
            "text": answers[0]
        }
    }
    faq_data["mainEntity"].append(main_entity)

    for i, question in enumerate(related_questions):
        if i < len(answers) - 1:  # Ensure we do not go beyond the answers list index
            entity = {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answers[i + 1]  # Add 1 to the index to match the answers list
                }
            }
            faq_data["mainEntity"].append(entity)

    return json.dumps(faq_data, indent=2)
