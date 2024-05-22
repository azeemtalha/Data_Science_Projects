from keys import gp_first_key
import os
#from langchain.llms.google_palm import GooglePalm
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

os.environ['GOOGLE_API_KEY'] = 'AIzaSyCvMuOyehJDnmWxZNF917EfEvV330EO4gA'

llm = GoogleGenerativeAI(model="gemini-pro",
                        google_api_key=os.environ['GOOGLE_API_KEY'],
                        temperature= 0.6)
#name = llm.invoke("I want to open a resturant for Pakistani food. Suggest a fency name for this.")
#prompt_temp_rest_name.format(cuisine='Pakistani')
#print(name_chain.invoke("American"))

def generate_rest_name_item(cuisine):

    prompt_temp_rest_name = PromptTemplate(
        input_variables= {'cuisine'},
        template= "I want to open a resturant for {cuisine} food. Suggest a fency name for this. Only one name"
    )

    name_chain = LLMChain(llm=llm, prompt=prompt_temp_rest_name, output_key="restaurant_name")

    prompt_temp_rest_items = PromptTemplate(
        input_variables= {'restaurant_name'},
        template= """suggest some menu items for {restaurant_name}. Return it as a comma seperated string"""
    )

    items_chain = LLMChain(llm=llm, prompt=prompt_temp_rest_items, output_key='menu_items')

    chain = SequentialChain(
        chains= [name_chain, items_chain],
        input_variables= ['cuisine'],
        output_variables= ['restaurant_name', 'menu_items']
    )

    response = chain.invoke({'cuisine': cuisine})

    return response


if __name__ == "__main__":
    print(generate_rest_name_item("Italian"))


