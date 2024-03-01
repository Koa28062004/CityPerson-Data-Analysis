import os
import json
import csv

# Directory containing the JSON files
folder_path = 'train/basel'

# Extract folder name from folder_path
folder_name = os.path.basename(folder_path)

# Dictionary to store label counts
label_counts = {}
image_counts = {}

# Function to count labels in a JSON file
def count_labels_in_file(file_path):
    tmp_counts = {}  # Initialize tmp_counts here
    with open(file_path, 'r') as file:
        data = json.load(file)
        for obj in data['children']:
            label = obj['identity']
            if label in label_counts:
                label_counts[label] += 1
                if label in tmp_counts:
                    tmp_counts[label] += 1
                else:
                    tmp_counts[label] = 1
            else:
                label_counts[label] = 1
                tmp_counts[label] = 1

        for label, count in tmp_counts.items():
            if label in image_counts:
                if count in image_counts[label]:
                    image_counts[label][count] += 1
                else:
                    image_counts[label][count] = 1
            else:
                image_counts[label] = {}
                image_counts[label][count] = 1


# Iterate through each file in the directory
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        count_labels_in_file(file_path)

# Sort the label counts and image counts
sorted_label_counts = dict(sorted(label_counts.items(), key=lambda item: item[1], reverse=True))

sorted_image_counts = {}
for label, count_dict in image_counts.items():
    sorted_image_counts[label] = dict(sorted(count_dict.items(), key=lambda item: item[0]))

# Create the directory structure for CSV files
csv_folder_path = os.path.join('csv', folder_path.replace('/', os.sep))
os.makedirs(csv_folder_path, exist_ok=True)

# Write the sorted counts to CSV files
label_csv_filename = os.path.join(csv_folder_path, f'{folder_name}_label_counts.csv')
image_csv_filename = os.path.join(csv_folder_path, f'{folder_name}_image_counts.csv')
summary_csv_filename = os.path.join('csv', 'summary', f'{folder_name}_image_counts.csv')

with open(label_csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['Label', 'Count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for label, count in sorted_label_counts.items():
        writer.writerow({'Label': label, 'Count': count})

with open(image_csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['Label', 'Count', 'Image Count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for label, count_dict in sorted_image_counts.items():
        for label_count, image_count in count_dict.items():
            writer.writerow({'Label': label, 'Count': label_count, 'Image Count': image_count})

# Write the summary counts to the summary CSV file
with open(summary_csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['Label', 'Count', 'Image Count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for label, count_dict in sorted_image_counts.items():
        for label_count, image_count in count_dict.items():
            writer.writerow({'Label': label, 'Count': label_count, 'Image Count': image_count})

print(f"CSV files '{label_csv_filename}' and '{image_csv_filename}' created successfully.")
print(f"Summary CSV file '{summary_csv_filename}' created successfully.")
