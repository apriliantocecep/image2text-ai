from dotenv import load_dotenv
import base64
import os
from openai import OpenAI

load_dotenv()


def convert_image_to_base64(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _extract_image_ai(image_base64, prompt):
    model_name = "gpt-4-vision-preview"
    messages = [
        {"role": "system", "content": "You are a image extractor, your job is to extract information based on a image & user's instruction"},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{image_base64}",
                },
                {
                    "type": "text",
                    "text": prompt,
                }
            ]
        }
    ]

    model = OpenAI(timeout=30)

    response = model.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=1024,
    )

    content = response.choices[0].message.content

    if "ANSWER_NOT_FOUND" in content:
        print("ERROR: Answer not found")
        return "I was unable to find the information on that image. Please pick another one"
    else:
        print(f"GPT: {content}")
        return content


def save_uploaded_file(uploaded_file):
    # Create a temporary directory if it doesn't exist
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Save the uploaded file to the temporary directory
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    return file_path


def image2text(image):
    base64_image = convert_image_to_base64(image)

    prompt = "Extract information based on your findings"

    output = _extract_image_ai(base64_image, prompt)

    return output
