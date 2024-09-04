import os
from io import BytesIO
import openai                  # for handling error types
from datetime import datetime  # for formatting date returned with images
import base64                  # for decoding images if recieved in the reply
import requests                # for downloading images from URLs
from PIL import Image          # pillow, for processing image types
import tkinter as tk           # for GUI thumbnails of what we got
from PIL import ImageTk        # for GUI thumbnails of what we got
from openai import OpenAI
import storytelling as st

OpenAI.api_key = "sk-robot-daniel-FOQfOlJ9dCGtSLaSTq2RT3BlbkFJ3fiAo6v08Aflm70zQmss"

os.environ["OPENAI_API_KEY"] = "sk-robot-daniel-FOQfOlJ9dCGtSLaSTq2RT3BlbkFJ3fiAo6v08Aflm70zQmss"
client = OpenAI() 

def generate_image(prompt): 
    image_params = {
    "model": "dall-e-3",  # Defaults to dall-e-2
    "n": 1,               # Between 2 and 10 is only for DALL-E 2
    "size": "1024x1024",  # 256x256, 512x512 only for DALL-E 2 - not much cheaper
    "prompt" :  prompt + "Do not include any text in the image."

      ,     # DALL-E 3: max 4000 characters, DALL-E 2: max 1000
    "user": "myName",     # pass a customer ID to OpenAI for abuse monitoring
    "response_format": "b64_json"
    }

    try:
        images_response = client.images.generate(**image_params)
    except openai.APIConnectionError as e:
        print("Server connection error: {e.__cause__}")  # from httpx.
        raise
    except openai.RateLimitError as e:
        print(f"OpenAI RATE LIMIT error {e.status_code}: (e.response)")
        raise
    except openai.APIStatusError as e:
        print(f"OpenAI STATUS error {e.status_code}: (e.response)")
        raise

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

    if images_response.data:
        # Access the first image data object
        image_data_object = images_response.data[0]

        # If image_data_object is a dictionary, use .get() method
        if isinstance(image_data_object, dict):
            image_data = image_data_object.get("b64_json")
        else:
            # If it's an object, access the attribute directly
            image_data = image_data_object.b64_json

        if image_data:
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            image_name = 'DALLE.png'
            image.save(image_name)
            print(f"Image saved as {image_name}")
            return image
        else:
            print("No image data obtained")
            return None
    else:
        print("No data found in images_response")
        return None
    


def generate_image_hint(story, question,answer,name): 
    image_params = {
    "model": "dall-e-3",  # Defaults to dall-e-2
    "n": 1,               # Between 2 and 10 is only for DALL-E 2
    "size": "1024x1024",  # 256x256, 512x512 only for DALL-E 2 - not much cheaper
    "prompt": f"""given this question {question}
                generate an image that gives the hint about the answer to the answer
                here's the answer {answer}
                here's the summary of the story {story}
                keep the image and story accurate to eachother
                Do not include any text in the image.
                Image style: Kid's storybook """
      ,     # DALL-E 3: max 4000 characters, DALL-E 2: max 1000
    "user": "myName",     # pass a customer ID to OpenAI for abuse monitoring
    "response_format": "b64_json"
    }

    try:
        images_response = client.images.generate(**image_params)
    except openai.APIConnectionError as e:
        print("Server connection error: {e.__cause__}")  # from httpx.
        raise
    except openai.RateLimitError as e:
        print(f"OpenAI RATE LIMIT error {e.status_code}: (e.response)")
        raise
    except openai.APIStatusError as e:
        print(f"OpenAI STATUS error {e.status_code}: (e.response)")
        raise

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

    if images_response.data:
        # Access the first image data object
        image_data_object = images_response.data[0]

        # If image_data_object is a dictionary, use .get() method
        if isinstance(image_data_object, dict):
            image_data = image_data_object.get("b64_json")
        else:
            # If it's an object, access the attribute directly
            image_data = image_data_object.b64_json

        if image_data:
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            image_name = name
            image.save(image_name)
            print(f"Image saved as {image_name}")
            return image
        else:
            print("No image data obtained")
            return None
    else:
        print("No data found in images_response")
        return None
    


  
#function to create content prompt to generate imeges out of the story 
def generateImagePrompt(story_segment, age_group_prompt, model= "gpt-3.5-turbo", temperature = 0.7, max_tokens = 1000):
    system_prompt = (f"""Given the following story : 
                     ```
                     {story_segment}
                     ```
                     Generate an image scenario under then 4000 characters, really descriptive of the situation 
                     for the given age group properties: 
                    ```
                     {age_group_prompt}
                    ````
                    keep in mind following reminders while generating the prompt                 
    
                    - be accurate with the details
    
                    -dont add too much complexity
                    
                    -show actions and emotions thought the story
                    
                    -be detailed and descriptive 
                    
                    - if you want a certain number of objects in the image, specify that number in the prompt
                    
                    - provide context or a setting of the environment that the main subject to be in
                    
                    -if possible, include references or examples in your prompts to give clear idea
                    
                    -ensure that prompt aligns with the resolution
                    
                      """)

    response = client.chat.completions.create(
        model=model,
        messages= [
            { "role": "system",
             "content" : system_prompt },
        ],       
        n=3,
        temperature=temperature,
        max_tokens=max_tokens,
    ) 
    return response.choices[0].message.content


def chooseTarget(ageGroup):

    if ageGroup=="Toddlers":
        prompt = """ -give most importance to colors blue, green , red , orange
                        -give less presence to colors red, orange, pink and green 
                        -High Contrast and Simple Images
                        - Simple, recognizable shapes and faces are common.
                        - visual stimulation
                        - image should be things of action” rather than as “objects of contemplation
                        -cartoon style illustration 
                        -imagine you are 1 years old trying to understand the story from the image
                        -make the story understandable by just looking at the image
                        -use imagery of things that they see in the real life
                        -create focus on the main scenario
                        -dont provide too  much distraction
                        -remind the prompt that when generating image based on this prompt in the future steps dont put any text in the image
                        -define the atmosphere of the story , specify at the end 
                        -Use Descriptive Adjectives: Adjectives help in refining the image. For example, instead of saying “a dog,” say “a fluffy, small, brown dog
                        -describe actions or movements. For instance, “a cat jumping over a fence” is more dynamic than just “a cat.”
                        - Short imperative phrases – Quickly convey major elements e.g. “An alien octopus playing drums”. Goes for brevity.
                        – Adds nuance and context e.g. “An enormous blue alien octopus skillfully playing a glowing futuristic drum kit on a rock concert stage.”
                        -highly complex scenes and compositions e.g. describing multiple characters, detailed clothing and expressions, extensive environmental context.
                    """
        
    elif ageGroup== "Preschoolers":
        prompt="""-takes pictures as symbols
            -use symbols( For example; bone symbolizes dog )
            -make use of the representational relation between a picture and the story
            -explain the story in the picture 
            -provide ability to form meta-representatin
            -provide explicit reasoning about pictures as symbols continue to develop throughout the preschool and elementary years
            -provide mapping between word and a picture
            -playful atmosphere 
            -clear depiction of key elements
            -Bright Colors and Clear Shapes
            -Interactive Elements: Pictures that encourage interaction (like flaps or textures) help with motor skills and engagement.
            -use symbols( For example; bone symbolizes dog)
            -Example: taught an unfamiliar label (“whisk”) for a small line drawing of an unfamiliar object (a whisk).
            -remind the prompt that when generating image based on this prompt in the future steps dont put any text in the image
            -define the atmosphere of the story , specify at the end 
            -Use Descriptive Adjectives: Adjectives help in refining the image. For example, instead of saying “a dog,” say “a fluffy, small, brown dog
            -describe actions or movements. For instance, “a cat jumping over a fence” is more dynamic than just “a cat.”
            - Short imperative phrases – Quickly convey major elements e.g. “An alien octopus playing drums”. Goes for brevity.
            – Adds nuance and context e.g. “An enormous blue alien octopus skillfully playing a glowing futuristic drum kit on a rock concert stage.”
            -highly complex scenes and compositions e.g. describing multiple characters, detailed clothing and expressions, extensive environmental context.

            """
            
        
    elif ageGroup== "Early Elementary":
        prompt =  """ provide story in the picture to help them understand the story
            -The images often depict actions or events mentioned in the text.
            -provide subtext messages mentioned in the story 
            -provide the humor in the pictures, related to the story
            -give most importance to colors blue, green , red , orange
            -give less presence to colors red, orange, pink and green 
            -avoid image or context repetition
            -avoid the use of complex symbolism
            -remind the prompt that when generating image based on this prompt in the future steps dont put any text in the image
            
            """

    elif ageGroup== "Preteens":
        prompt=""" 
        -extract the key elements of the story and concentrate on that
        -for example if a process is being explained; explain the process in the image prompt and tell a story with just seeing the image
        -give most importance to colors blue, green , red , orange
        -give less presence to colors red, orange, pink and green 
        -remind the prompt that when generating image based on this prompt in the future steps dont put any text in the image
        -stay away from the too abstract descriptions
        -dont overwhelm with the details 
        -include relatable elements like , a child observing, or joining into the action with the storyline
        -decrease the complexity of the background
        -make the focal point the main character of the storyline
        -include visual cues; symbols, arrows . For example if a photosynthesis being explained; put arrows showing the directions of the sunlight , water and air or illustrate the release of the oxygen

        """

    elif ageGroup== "Late Elementary":
        prompt= """ 
        -extract the key elements of the story and concentrate on that
        -for example if a process is being explained; explain the process in the image prompt and tell a story with just seeing the image
        -give most importance to colors blue, green , red , orange
        -give less presence to colors red, orange, pink and green 
        -remind the prompt that when generating image based on this prompt in the future steps dont put any text in the image
        -stay away from the too abstract descriptions
        -dont overwhelm with the details 
        -include relatable elements like , a child observing, or joining into the action with the storyline
        -decrease the complexity of the background
        -make the focal point the main character of the storyline
        -include visual cues; symbols, arrows . For example if a photosynthesis being explained; put arrows showing the directions of the sunlight , water and air or illustrate the release of the oxygen
        """

    else:
        raise ValueError("choose target error")

    return prompt

def generate_image_begin(story_segment, age_group):     
    prompt91= generateImagePrompt(story_segment, chooseTarget(age_group))
    print("Image generation prompt" + prompt91)
    generate_image(prompt91)
    print("image is generated and saved under the name 'DALLE' ")


# https://www.sciencedirect.com/science/article/pii/S0022096509001301#bib15 
# https://medium.com/centerforcooperativemedia/a-beginners-guide-to-image-generation-with-dall-e-3-4efd969ab8fb 

blank_string= "_______________________________________________________________________________________________________________________________________"


storyPrompt = """In a world full of green leaves and colorful flowers, there is a magical process called photosynthesis. Let me tell you all about it! 
Once upon a time, in a sunny garden, a little plant named Lily was soaking up the warm sunlight. This sunlight was like food for Lily, helping her grow big and strong. But do you know how Lily turned sunlight into food?
Well, it's all thanks to photosynthesis! This is like a superpower that plants have, where they use sunlight, water, and air to make their own food. Just like how you need yummy snacks to grow, plants need photosynthesis to survive.
Imagine a little factory inside Lily that works day and night to make delicious green leaves and colorful flowers. This factory is powered by sunlight and works like magic to keep Lily healthy and happy.
So, next time you see a beautiful flower or a big tree, remember the amazing power of photosynthesis that keeps them alive and thriving! The end."""


storyPrompt2 = """Once upon a time, in a small town, there lived a girl named Alex. Alex had a special friend, a robot dog named Sparky. Sparky was not like any other dog - he could talk, walk, and even do math!
Every day after school, Alex and Sparky would go on exciting adventures. They would explore the park, chase butterflies, and sometimes even solve mysteries in the neighborhood. Alex and Sparky were the best of friends, and they always had each other's back.
One sunny morning, Alex and Sparky woke up to find that the town's ice cream truck was broken down. The ice cream man, Mr. Scoops, was very sad because he couldn't deliver ice cream to the kids in the town that day.
Alex knew she had to help Mr. Scoops. She and Sparky quickly got to work. Sparky used his robotic skills to fix the ice cream truck, while Alex made colorful posters to let everyone know that the ice cream truck would be back soon.
The whole town was amazed at Alex and Sparky's kindness and hard work. When the ice cream truck was up and running again, Mr. Scoops gave Alex and Sparky free ice cream for a whole year as a thank you
Alex and Sparky were overjoyed. They had not only saved the day but had also brought smiles to everyone in town. From that day on, Alex and Sparky were known as the town's heroes, always ready to help those in need.
And so, Alex and Sparky continued to have fun-filled adventures, knowing that they were a team that could overcome any challenge together."""

storyPrompt3 = """ There was a couple called Seb and Nur . Seb went to army and left Nur alone in Lausanne. Usually they were always together so it was a big change for Nur.However Seb got so successfull in the army he was collecting all the ribons in the army and the last one he got was for the sport ribon. And all the way Nur supported him. Seb was getting these ribons for  Nur so she can wear them in the future and be proud of her boyfriend. Finally Thursday came and Seb and Nur met in the train station while Seb had his army clothes holding two ribbons he got. Nur and Seb were hugging in the train station so thighly
This is a modern scenario . Seb has green army clothes. He has ligh skin, green eyes,  a bit curly brown hair he is tall. Nur has light skin, big blue eyes, has long wawy brown hair with blond shades. This is a story that passes in 2024 so include this detail while generating , no old style imagery. But draw Nur as Hello Kitty cartoon character and Seb as Batman cartoon character"""

storyPrompt4 = """Story:
In a town not far away, there lived a boy named Louis
Who had a lion as a pet, they loved to play all day
The lion's name was Lily, big and strong and bright
Together they roamed, side by side, as siblings with a bond so tight

Lily and Louis would run in fields, under the shining sun
Laughing, racing, having fun, their joy never undone
Lily's mane fluttered in the breeze, Louis' smile reached his eyes
In each other's company, they found a wondrous prize

When the day would turn to night, they'd rest by the fire's light
Louis would tell Lily tales, stories that took to flight
Lily would listen, eyes aglow, her heart filled up with pride
To have a sibling like Louis, always by her side

One day as they roamed, Lily heard a faint, timid chirp
She rushed to the sound and found a bird, in some sticky syrup
Louis joined Lily, helped the bird, set it free and well
Lily nudged Louis, a grateful purr, their sibling bond strong as a bell

In this pair so brave and true, the preschoolers find glee
Learning of sibling love, kindness, and so much more to see
With Lily, the mighty lion, and Louis, the loyal sibling
Their adventures never-ending, a bond that'll never bend."""


prompt1 = ( "Subject: a professional high quality emoji of a lovestruck cup of boba"  # use the space at end
 #"Style: children's book aesthetic for 5 years old, sparkle their imagination, should look like made in computer."     # this is implicit line continuation
)
prompt2= ("a snail made of harp")
prompt3= ("a snail with the texture of harp")
prompt4=(prompt2+ prompt3)

#generate_image_begin(storyPrompt3, 'Preteens')

#generate_image_hint
question1 = "What did Sebastian have for breakfast with his favorite teddy bear, Cocoa?"
answer1= "Sebastian had pancakes and syrup for breakfast with his favorite teddy bear, Cocoa."
name1= 'DALLE1.png'

question2 = "Why was Sebastian excited to go to the library after playing at the park?"
answer2= "Sebastian was excited to go to the library after playing at the park to find some new books to read."
name2 = 'DALLE2.png'

question3= "How did Sebastian feel at the end of the day?"
answer3 = "Sebastian felt grateful for a wonderful day full of fun and laughter at the end of the day."
name3 = 'DALLE3.png'

