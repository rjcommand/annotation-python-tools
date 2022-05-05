import os

directory = r'D:\Desktop\directory'

# Use underscore? Otherwise defaults to hyphen
is_use_underscore = True
char_to_use = '_' if is_use_underscore else '-'   

print("Renaming files now!")
for root, dirs, files in os.walk(directory):
    print(f"root: {root}")
    print(f"dirs: {dirs}")
    print(f"files: {files}")

    for current_filename in files:
        new_filename = current_filename.replace(' ', char_to_use)

        print(f"current filename: {current_filename}")
        print(f"    new filename: {new_filename}")

        os.rename(
            os.path.join(root, current_filename), 
            os.path.join(root, new_filename)
        )   

print("All done!")
