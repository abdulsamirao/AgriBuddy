import os

def list_subdirs_with_counts(folder_path: str) -> list[int]:
    """
    Prints the name of each sub-directory in the given folder
    along with the number of items inside each (for determining class weights).
    """
    
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        return []

    class_counts = []
    for entry in os.scandir(folder_path):
        if entry.is_dir():
            item_count = len(os.listdir(entry.path))
            print(f"{entry.name}: {item_count}")
            class_counts.append(item_count)
    
    return class_counts

print(list_subdirs_with_counts("datasets/wheat_disease_dataset/train"))