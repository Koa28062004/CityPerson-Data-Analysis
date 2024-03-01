import os
import csv

# Directory containing the CSV files
folder_path = 'csv/train'

# Dictionary to store label counts
label_counts = {}
image_counts = {}

# Iterate through each file in the directory
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                label = row['Label']
                count = int(row['Count'])
                image_count = int(row['Image Count'])
                
                # Update label counts
                if label in label_counts:
                    label_counts[label] += count
                else:
                    label_counts[label] = count
                
                # Update image counts
                if label in image_counts:
                    if count in image_counts[label]:
                        image_counts[label][count] += image_count
                    else:
                        image_counts[label][count] = image_count
                else:
                    image_counts[label] = {count: image_count}

# Write the summarized counts to new CSV files
summary_label_csv = 'summary_label_counts.csv'
summary_image_csv = 'summary_image_counts.csv'

with open(summary_label_csv, 'w', newline='') as csvfile:
    fieldnames = ['Label', 'Count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for label, count in label_counts.items():
        writer.writerow({'Label': label, 'Count': count})

with open(summary_image_csv, 'w', newline='') as csvfile:
    fieldnames = ['Label', 'Count', 'Image Count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for label, count_dict in image_counts.items():
        for count, image_count in count_dict.items():
            writer.writerow({'Label': label, 'Count': count, 'Image Count': image_count})

print(f"Summary CSV files '{summary_label_csv}' and '{summary_image_csv}' created successfully.")
