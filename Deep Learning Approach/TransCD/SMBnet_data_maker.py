import os
if __name__ == '__main__':
    # Folder where the images are stored
    base_path = os.path.join(os.path.dirname(__file__), '..\\..\\datasets\\SBMnet')
    # Name of the output text file
    for root, _, files in os.walk(base_path):
        # Check if the current folder ends with '/input'
        if root.endswith('input'):
            # Extract category and sub-category names from the path
            # Assumes structure like "base_dir/category/sub_category/input"
            # Split the path into parts
            path_parts = root.split(os.sep)
            # Get the category and sub-category
            category = path_parts[-3]
            sub_category = path_parts[-2]

            output_file_path = os.path.join(os.path.dirname(__file__), f'SBMnet\\data\\{sub_category}.txt')

            with open(output_file_path, 'w') as output_file:
                for idx, image in enumerate(files):
                    if image.lower().endswith('.jpg'):
                        row = []
                        # For the first cell, the first image appears three times
                        if idx == 0:
                            row = [f"{category}/{sub_category}/input/{image}"] * 3
                        else:
                            # For other cells, the first image is followed by two repeats of other images
                            row.append(f"{category}/{sub_category}/input/{files[0]}")  # First image
                            # Add the next two images, which could be the same as the previous row's third image
                            row.append(f"{category}/{sub_category}/input/{files[idx]}")  # Second image
                            row.append(f"{category}/{sub_category}/input/{files[idx]}")  # Third image
                    output_file.write(" ".join(row) + "\n")

