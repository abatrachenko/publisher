import pandas as pd
from chatgpt_api import generate_text
from image_generation import generate_image
from wordpress_publisher import publish_post
from markup_generator import generate_title_tag, generate_meta_description, create_json_ld_markup
from context_generator import generate_context

# Read data from Excel
df = pd.read_excel('input_data.xlsx', engine='openpyxl')

# Loop through each row in the dataframe
for index, row in df.iterrows():
    main_question = row['main_question']
    image_prompt = row['image_prompt']
    category_id = [int(row['category_id'])]  # Convert the category ID to integer and put it in a list

    # Print the status message
    print(f"Processing main question: {main_question}")

    # Generate the answer to the main question using ChatGPT
    context_main = generate_context(main_question)
    answer_prompt = f"{context_main}\nAnswer the following question thoroughly and in detail using the context provided above. Your response should address the question directly starting with a 'yes', 'no', or 'yes and no' response. Do not make any mention of the context in your answer. If the context provided is not relevant to the question, use your own knowledge. Do not make any reference to the context in your response. The question is: {main_question}"
    answer = generate_text(answer_prompt, max_tokens=750)

    # Generate 9 related questions using ChatGPT
    related_question_prompt = f"Generate 9 related questions based on a question I will provide. The questions you generate should focus on the food item in question. Also, your response should not include numbering. The question is: {main_question}"
    related_questions = generate_text(related_question_prompt).split("\n")

    # Generate answers for the related questions using ChatGPT
    related_answers = []
    for q in related_questions:
        context_related = generate_context(q)  # Generating context for each related question
        ans = generate_text(f"{context_related}\nAnswer the following question thoroughly and in detail using the context provided. Your response should address the question directly. Do not mention the context provided in this in your answer. If the context provided is not relevant to the question, use your own knowledge. Do not make any reference to the context in your response. The question is: {q}", max_tokens=750)
        related_answers.append(ans)

    # Combine the main question and answer with the related questions and answers
    questions_and_answers = list(zip(related_questions, related_answers))

    # Generate the post title and meta description
    post_title = generate_title_tag(main_question)
    meta_description = generate_meta_description(answer, related_questions)

    # Generate the HTML output for the post content
    html_output = f"<h1>{post_title}</h1>\n<p>{answer}</p>"
    for question, ans in questions_and_answers:
        html_output += f"<br><br><h2>{question}</h2><br><p>{ans}</p>"

    # Generate JSON-LD markup for the FAQ schema
    json_ld_markup = create_json_ld_markup(main_question, related_questions, related_answers)

    # Generate the image using image prompt from Excel
    image_urls = generate_image(image_prompt)

    # Assuming you want to automatically select the first image (you can also add more logic here)
    chosen_image_index = 0
    image_url = image_urls[chosen_image_index]

    # Publish the post to WordPress
    publish_post(post_title, html_output, json_ld_markup, image_url, category_id)
