from icrawler.builtin import GoogleImageCrawler
import os

# List of toddler-accessible items (abbreviated for preview — expand as needed)
items = [
    "cup", "spoon", "plate", "bowl", "fork", "apple", "banana", "milk", "water", "juice",
    "ball", "book", "chair", "table", "pillow", "blanket", "sofa", "lamp", "remote", "toy",
    "toothbrush", "toothpaste", "towel", "soap", "shampoo", "comb", "brush", "potty",
    "bed", "doll", "teddy bear", "drawer", "sock",
    "shirt", "pants", "shoes", "hat", "coat", "diaper", "bib", "gloves", "scarf",
    "toy car", "blocks", "puzzle", "crayons", "stuffed animal", "train", "toy phone",
    "keys", "phone", "bag", "bottle", "balloon", "box", "clock", "light", "door", "window"
]

output_dir = "dataset"
images_per_item = 100

os.makedirs(output_dir, exist_ok=True)

for item in items:
    label = item.replace(" ", "_")
    item_dir = os.path.join(output_dir, label)
    os.makedirs(item_dir, exist_ok=True)

    print(f"Downloading images for: {item}")

    crawler = GoogleImageCrawler(storage={'root_dir': item_dir})
    crawler.crawl(keyword=item, max_num=images_per_item, file_idx_offset=0)