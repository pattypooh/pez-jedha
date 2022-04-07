import os

print(os.getcwd())
filename = './projects/05-walmart/src/data/req.txt'

with open(filename, 'r') as file_obj:
    content = file_obj.readlines()
print(type(content))

lines = [content[i].split('=')[0] for i in range(5, len(content))]
new_content='\n'.join(lines)

print(new_content)
filename = './projects/05-walmart/new_req.txt'
with open(filename, 'w') as file_obj:
    file_obj.writelines(new_content)