from chatgpt_api import generate_text
from image_generation import generate_image
from wordpress_publisher import publish_post
from markup_generator import generate_title_tag, generate_meta_description, create_json_ld_markup
from context_generator import generate_context

# Prompt the uCan DCan DSr to input the main question
user_input = input("Please enter your main question: ")
main_question = user_input.strip()

# Generate the answer to the main question using ChatGPT
context_main = generate_context(main_question)
answer_prompt = f"{context_main}\nAnswer the following question thoroughly and in detail using the context provided above. Your response should address the question directly starting with a 'yes', 'no', or 'yes and no' response, but do not make any mention of the context in your answer. If the context provided is not relevant to the question, use your own knowledge. The question is: {main_question}"
answer = generate_text(answer_prompt, max_tokens=650)

# Generate 9 related questions using ChatGPT
related_question_prompt = f"Generate 9 related questions based on a question i will provide. The questions you generate should focus on the food item in question. Also, your response should not include numbering. The question is: {main_question}"
related_questions = generate_text(related_question_prompt).split("\n")

# Generate answers for the related questions using ChatGPT
related_answers = []
for q in related_questions:
    context_related = generate_context(q)  # Generating context for each related question
    ans = generate_text(f"{context_related}\nAnswer the following question thoroughly and in detail using the context provided above, but do not make any mention of the context in your answer. If the context provided is not relevant to the question, use your own knowledge. Also, answer the question directly, while making no mention that context was provided. The question is: {q}", max_tokens=650)
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

# Ask the user for the image prompt and generate the featured image URL for the post
image_prompt = input("Please enter your image prompt: ")
image_urls = generate_image(image_prompt)

# Allow user to choose an image from the variations
print("Please choose an image from the following URLs:")
for i, url in enumerate(image_urls):
    print(f"{i + 1}. {url}")

chosen_image_index = int(input("Enter the number of the image you want to use: ")) - 1
image_url = image_urls[chosen_image_index]

# Publish the post to WordPress
publish_post(post_title, html_output, json_ld_markup, image_url)
