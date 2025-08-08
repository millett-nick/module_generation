from openai import OpenAI
import re
import time
import numpy as np
import json
import os
from dotenv import load_dotenv

class ModuleGenerator():
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPEN_API_KEY")

    def generate(self,prompt,flag=0):  #Flag for error
        # Replace 'YOUR_API_KEY' with your OpenAI API key
        client = OpenAI(api_key=self.api_key) 
        system_content = 'You are a module generator expert. Help me to write module with following instructions.'
        suffix = 'Give me only python script in your response. No need to write content.'
        
        init_messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt + suffix},
        ]

        response = client.chat.completions.create(
            messages=init_messages,
            model="gpt-4o", temperature=0.7, n=1).choices[0].message

        d = {'role':response.role,'content': response.content}
        init_messages.append(d)

        generated_code = response.content

        try:
            matches = re.findall(r"```python\n(.*?)\n```", generated_code, re.DOTALL)
            extracted_code = matches[0].strip()
        except:
            extracted_code = generated_code

        return extracted_code
    
if __name__=="__main__":
    file_name = input("Enter your module name: ")
    prompt = input("Enter Your Prompt: ")
    generator = ModuleGenerator()
    gen_module = generator.generate(prompt)
    with open(file_name, "w") as file:
            file.write(gen_module)

     