import os

with open("testingPNG.txt", "r") as txt_file:
    text = txt_file.read().splitlines()

def compact(lst):
    return list(filter(None, lst))

to_remove = ['\n','Photo is', 'Available']
text = [elt for elt in text if elt not in to_remove]
text = [x for x in text if not isinstance(x, int)]
text = compact(text)
text.pop(0)
text.pop(0)
text.pop()
print(text)