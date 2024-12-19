import os
import random


def random_choice():
    if random.random() < 0.5:
        dataset_path = os.path.join(os.path.dirname(__file__), '..\\datasets\\SBMnet')
        chosen_dataset = 'SBMnet'  # http://pione.dinf.usherbrooke.ca/dataset
    else:
        dataset_path = os.path.join(os.path.dirname(__file__), '..\\datasets\\CD2014\\dataset')
        chosen_dataset = 'CDNet_2014'  # http://jacarini.dinf.usherbrooke.ca/dataset2014

    # Get a list of all category folders in the base directory
    categories = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
    # Select a random category
    random_category = random.choice(categories)
    # Get the path to the selected category folder
    category_path = os.path.join(dataset_path, random_category)
    # Get a list of all sub-category folders in the selected category
    sub_categories = [d for d in os.listdir(category_path) if os.path.isdir(os.path.join(category_path, d))]
    # Select a random sub-category
    random_sub_category = random.choice(sub_categories)

    return dataset_path, chosen_dataset, random_category, random_sub_category


def get_random_choice(notebook_id):
    # Path to the shared file that stores the current random choice and usage count
    random_choice_file = os.path.join(os.path.dirname(__file__), '..\\datasets\\random_choice.txt')
    # Check if the shared file exists
    # If not, create it with a new random choice and a usage count of 0
    if not os.path.exists(random_choice_file):
        dataset_path, chosen_dataset, random_category, random_sub_category = random_choice()
        with open(random_choice_file, 'w') as f:
            f.write(f"{dataset_path}\n{chosen_dataset}\n{random_category}\n{random_sub_category}\n1\n{notebook_id}")
        return dataset_path, chosen_dataset, random_category, random_sub_category
    else:
        # If it exists, read the current random choice and usage count
        with (open(random_choice_file, 'r') as f):
            lines = f.readlines()
            dataset_path = lines[0].strip()
            chosen_dataset = lines[1].strip()
            random_category = lines[2].strip()
            random_sub_category = lines[3].strip()
            usage_count = int(lines[4].strip())
            last_notebook = lines[5].strip()

        # Increment the usage count
        if notebook_id != last_notebook:
            usage_count += 1

        if usage_count <= 2:
            with open(random_choice_file, 'w') as f:
                f.write(f"{dataset_path}\n{chosen_dataset}\n{random_category}\n{random_sub_category}\n{usage_count}\n{notebook_id}")
            return dataset_path, chosen_dataset, random_category, random_sub_category
        else:
            dataset_path, chosen_dataset, random_category, random_sub_category = random_choice()
            with open(random_choice_file, 'w') as f:
                f.write(f"{dataset_path}\n{chosen_dataset}\n{random_category}\n{random_sub_category}\n1\n{notebook_id}")
            return dataset_path, chosen_dataset, random_category, random_sub_category
