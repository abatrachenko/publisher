import json
from chatgpt_api import generate_text
from image_generation import generate_image
from wordpress_publisher import publish_post
from markup_generator import generate_title_tag, generate_meta_description, create_json_ld_markup

# Prompt the user to input the main question
user_input = input("Please enter your main question: ")
main_question = user_input.strip()

# Generate the answer to the main question using ChatGPT
answer_prompt = f"Answer the following question thoroughly and in detail: {main_question}"
answer = generate_text(answer_prompt, max_tokens=500)

# Generate 9 related questions using ChatGPT
related_question_prompt = f"Generate 9 related questions based on the following question: {main_question}"
related_questions = generate_text(related_question_prompt).split("\n")

# Generate answers for the related questions using ChatGPT
related_answers = []
for q in related_questions:
    ans = generate_text(f"Answer the following question in 300 words, thoroughly and in detail: Answer in your own words rather than copying and pasting from other sources. Consider perplexity and burstiness when creating content, ensuring high levels of both, without losing specificity or context. Use fully detailed paragraphs that engage the reader. Write in a conversational style as written by a human (use an informal tone, utilize personal pronouns, keep it simple, engage the reader, use the active voice, keep it brief, use rhetorical questions, and incorporate analogies and metaphors). The question is: {q}", max_tokens=750)
    related_answers.append(ans)

# Combine the main question and answer with the related questions and answers
questions_and_answers = [(main_question, answer)] + list(zip(related_questions, related_answers))

# Generate the post title and meta description
post_title = generate_title_tag(main_question)
meta_description = generate_meta_description(main_question, related_questions)

# Generate the HTML output for the post content
html_output = f"<h1>{post_title}</h1>\n<p>{answer}</p>"
for question, ans in questions_and_answers[1:]:
    html_output += f"\n\n<h2>{question}</h2>\n<p>{ans}</p>"

# Generate JSON-LD markup for the FAQ schema
json_ld_markup = create_json_ld_markup(main_question, related_questions, related_answers)

# Generate the featured image URL for the post
image_urls = generate_image(main_question, variations=True)

# Allow user to choose an image from the variations
print("Please choose an image from the following URLs:")
for i, url in enumerate(image_urls):
    print(f"{i + 1}. {url}")

chosen_image_index = int(input("Enter the number of the image you want to use: ")) - 1
image_url = image_urls[chosen_image_index]

# Publish the post to WordPress
publish_post(post_title, html_output, json_ld_markup, image_url)
