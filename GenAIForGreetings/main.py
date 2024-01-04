import cv2
import numpy as np
import openai
import os
from langchain.llms import OpenAI as LangChainOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from PIL import Image, ImageDraw, ImageFont

# Set up OpenAI API keys


# Load the image
image = cv2.imread('cardtemplate2.png')
original_image = image.copy()

image_pil = Image.open('cardtemplate2.png')
image_copy = image_pil.copy()

# Convert the image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define ranges for red color in HSV
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# # Threshold the HSV image to get only red colors
mask = cv2.inRange(hsv, lower_red, upper_red)

# # Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Load your company's logo as a PIL image
logo = Image.open('company_logo.png')

# Get background color
background_color = '#f1f1f1'
print(background_color)

# Function to create a borderless textbox with greetings
def create_textbox(text, width, height, background_color):
    img = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(img)
    font_path = 'GermaniaOne-Regular.ttf'
    font_size = 60
    font = ImageFont.truetype(font_path, font_size)
    
    # Wrap text to fit within the specified width
    max_text_width = width  # Adjust for padding
    lines = []
    line = ''
    for word in text.split():
        if draw.textsize(line + word, font=font)[0] < max_text_width:
            line += word + ' '
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)
    
    # Adjust font size if needed to fit the text within the height
    while sum(draw.textsize(line, font=font)[1] for line in lines) > height:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
    
    # Draw wrapped text on the image
    y = (height - sum(draw.textsize(line, font=font)[1] for line in lines)) // 2
    for line in lines:
        text_width, text_height = draw.textsize(line, font=font)
        x = (width - text_width) // 2
        draw.text((x, y), line, fill='#102a44', font=font)
        y += text_height
    
    return img

def create_overlay(width, height, background_color):
    img = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(img)
    rectangle_coords = (0, 0, width, height)
    draw.rectangle(rectangle_coords, outline="white", fill=background_color)
    return img

array = ['John Tan', 'ABC company', 'Purchasing Manager', 'producing more efficient IT processes','3 years']

llm = LangChainOpenAI(temperature=0.7)

template1 = '''Please write a Christmas greeting and best wishes for 2024, consisting of three sentences for {point_of_contact}.  
He is the {role} from {customer_company} and used our services for {impact}.  He has been our customer for {period}.
'''

prompt1 = PromptTemplate(
    input_variables=['point_of_contact', 'customer_company', 'role', 'impact', 'period'],
    template=template1
)

prompt1.format(
    point_of_contact=array[0],
    customer_company=array[1],
    role=array[2],
    impact=array[3],
    period=array[4]
)

chain = LLMChain(llm=llm, prompt=prompt1)

# Corrected Step: Generate Greetings using LangChain
response = chain.run({
    'point_of_contact': array[0],
    'customer_company': array[1],
    'role': array[2],
    'impact': array[3],
    'period': array[4]
})

greetings = response

# Loop through the contours
for contour in contours:
    # Approximate the contour to determine shape
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
    
    # If the shape has 3 vertices, it's a triangle (replace with logo)
    if len(approx) == 3:

        # Get bounding box coordinates for the triangle
        x, y, w, h = cv2.boundingRect(approx)

        w = w+70

        box = create_overlay(w, h, background_color)
        box_cv = cv2.cvtColor(np.array(box), cv2.COLOR_RGBA2BGR)
        original_image[y:y+h, x:x+w] = box_cv
        
        # Resize the logo to fit the triangle bounding box
        logo_rgba = logo.convert('RGBA')
        resized_logo = logo_rgba.resize((w, h))
        
        # Convert resized logo to OpenCV format with alpha channel
        logo_with_alpha = np.array(resized_logo)

        # Create a mask for the logo
        logo_alpha = logo_with_alpha[:, :, 3] / 255.0  # Normalize alpha channel

        # Invert the alpha channel for proper blending
        inv_logo_alpha = 1.0 - logo_alpha

        # Extract the logo's RGB channels
        logo_rgb = logo_with_alpha[:, :, :3]

        # Calculate regions for insertion
        roi = original_image[y:y+h, x:x+w]

        # Perform alpha blending
        for c in range(0, 3):
            roi[:, :, c] = (logo_alpha * logo_rgb[:, :, c] +
                            inv_logo_alpha * roi[:, :, c])

        original_image[y:y+h, x:x+w] = roi
    
    # If the shape has 4 vertices, it's a rectangle (replace with textbox)
    elif len(approx) == 4:
        # Get bounding box coordinates for the rectangle
        x, y, w, h = cv2.boundingRect(approx)
        
        # Create a borderless textbox with greetings
        textbox = create_textbox(greetings, w+20, h+10, background_color)
        
        # Convert PIL image to OpenCV format
        textbox_cv = cv2.cvtColor(np.array(textbox), cv2.COLOR_RGBA2BGR)
        
        # Replace the rectangle with the textbox
        original_image[y-2:y-2+h+10, x-2:x-2+w+20] = textbox_cv

# Save the modified image
cv2.imwrite('modified_image.jpg', original_image)
print("Image with replaced shapes saved as 'modified_image.jpg'")


