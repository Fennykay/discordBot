from bs4 import BeautifulSoup
import requests
import send_text
import openAIRequests

def get_recipe_for_deepfriedhoney(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve recipe")
        return
    soup = BeautifulSoup(response.text, 'html.parser')

    ingredients = []
    instructions = []

    ingredient_block = soup.find('div', class_='tasty-recipes-ingredients')
    instructions_block = soup.find('div', class_='tasty-recipes-instructions')
    for ul in ingredient_block.find_all('ul'):
        for li in ul.find_all('li'):
            ingredient = li.get_text()
            #break down the ingredient into a list
            ingredient = ingredient.split(' ')
            ingredients.append((ingredient[0], ingredient[1], ' '.join(ingredient[2:])))
    for ol in instructions_block.find_all('ol'):
        for li in ol.find_all('li'):
            instructions.append(li.get_text())

    return ingredients, instructions

if __name__ == '__main__':
    web_url = "https://www.deepfriedhoney.com/spicy-chicken-sandwiches/"
    ingred, instructions = get_recipe_for_deepfriedhoney(web_url)

    # Convert each tuple in ingred to a string and join them with a space
    ingred_str = '\n'.join([' '.join(map(str, tup)) for tup in ingred])
    # Join the instructions with a space
    instructions_str = '\n\n'.join(instructions)
    message = openAIRequests.summarize_cookiing_recipe(ingred_str + instructions_str)
    print(message)
    send_text.send_message("ky", message)
