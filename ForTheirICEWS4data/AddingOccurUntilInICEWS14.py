# Define the input and output file paths
input_file_path = 'icews_2014_train.txt'  # Update this with the actual path to your input file
output_file_path = ('icews_2014_train_withOccurUntil.txt')  # This is where the output will be saved

# Read the input file
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Process each line
output_lines = []
for line in lines:
    output_lines.append(line.strip())  # Add the original line with occurSince
    # Replace occurSince with occurUntil and add to the output list
    output_lines.append(line.replace('occurSince', 'occurUntil').strip())

# Write the output to the new file
with open(output_file_path, 'w') as file:
    for line in output_lines:
        file.write(line + '\n')
