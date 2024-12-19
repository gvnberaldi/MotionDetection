import os

if __name__ == '__main__':
    base_path = os.path.join(os.path.dirname(__file__), '..\\..\\datasets\\CD2014\\dataset')

    # Iterate through each category folder
    for category in os.listdir(base_path):
        category_path = os.path.join(base_path, category)
        for sub_category in os.listdir(category_path):
            sub_category_path = os.path.join(category_path, sub_category)
            input_folder = os.path.join(sub_category_path, "input")
            groundtruth_folder = os.path.join(sub_category_path, "groundtruth")
            inputs = items = os.listdir(input_folder)
            groundtruths = os.listdir(groundtruth_folder)
            length = min(len(inputs), len(groundtruths))
            output_file_path = os.path.join(os.path.dirname(__file__), f'CDNet_2014\\data\\{sub_category}.txt')

            with open(output_file_path, 'w') as output_file:
                for idx in range(1, length):
                    row = [f"{category}/{sub_category}/input/{inputs[0]} "
                           f"{category}/{sub_category}/input/{inputs[idx]} "
                           f"{category}/{sub_category}/groundtruth/{groundtruths[idx]}"]
                    output_file.write(" ".join(row) + "\n")

