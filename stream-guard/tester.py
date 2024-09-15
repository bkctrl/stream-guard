# import inflect

# # Initialize the inflect engine
# p = inflect.engine()

# # Example words
# words = ['goose', 'mouse', 'child', 'wolf']

# # Get plural forms
# plural_forms = {word: p.plural(word) for word in words}

# print(plural_forms)
import os
tmp = os.path.join(os.path.dirname(os.getcwd()), "tmp\\")
with open(os.path.join(tmp, "transcript.txt"), "r") as f:
    print(f.read())
