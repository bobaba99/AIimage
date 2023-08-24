import openai
import csv
import requests


words = []
definitions = []
synonyms = []
stems = []

# with open('Synonyme.csv', "r") as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         if len(row) >= 2:
#             synonyms.append(row[0])

column_index = 1
with open('Synonyme.csv', "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) >= 2:
            value = row[1].strip()
            synonyms.append(value)
        else:
            synonyms.append("")


with open('Definition.csv', "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) >= 2:
            words.append(row[0])
            definitions.append(row[1])


openai.api_key = "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"

temp_words = words[1:]
temp_def = definitions[1:]
temp_synonyms = synonyms[1:]

# print(len(temp_words)) # 3597
# print(len(temp_def))
# print(len(temp_synonyms))

for i in range(3597):
    stems.append("Image of " + temp_words[i] + " (Style: realism, no text, white background; " +
                 temp_words[i] + " definition: " + temp_def[i] + "; " + temp_words[i] +
                 " synonyms: " + temp_synonyms[i])


# print(stems[8])

# prompt_stem = \
#     "Image of [WORD1] (Style: realistic, no text, white background;" \
#     "[WORD1] definition: x; [WORD1] synonyms: [y, z])"

temp_stems = stems[:5]
counter = 1
num_photo = 2
exception = []

for prompt in temp_stems:
    try:
        response = openai.Image.create(
          prompt=prompt,
          n=num_photo,                          # number of images
          size="512x512"              # 256x256, 512x512, 1024x1024 (default)
        )
        for i in range(num_photo):
            image_url = response['data'][i]['url']
            image_data = requests.get(image_url).content
            image_name = "./Images/" + str(counter) + "-" + str(i+1) + ".jpg"
            with open(image_name, "wb") as f:
                f.write(image_data)
            print(image_name + " generated")
        counter += 1
    except Exception as e:
        print(f"Error with prompt '{prompt}': {e}")
        exception.append([prompt, e])
        continue


with open('Exception.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(exception)
    # image_url = response['data'][0]['url']
    # image_data = requests.get(image_url).content
    # with open("./Images/" + str(counter) + ".jpg", "wb") as f:
    #     f.write(image_data)