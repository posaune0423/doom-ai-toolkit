#!/usr/bin/env python3
"""Validate dataset structure for memecoin LoRA training.

This script checks that:
- Images and captions are paired correctly
- Captions start with the expected trigger word (doom_)
"""

import os

DATASET_ROOT = "content/dataset"
datasets = ['popcat', 'bonk', 'wif']

for dataset_name in datasets:
    dataset_path = os.path.join(DATASET_ROOT, dataset_name)

    if not os.path.exists(dataset_path):
        print(f"\n{dataset_name}: ERROR - Dataset folder does not exist")
        continue

    # Check for images and captions
    all_files = os.listdir(dataset_path) if os.path.exists(dataset_path) else []
    images = [f for f in all_files if f.endswith(('.jpg', '.jpeg', '.png'))]
    captions = [f for f in all_files if f.endswith('.txt')]

    print(f"\n{dataset_name}:")
    print(f"  Images: {len(images)}, Captions: {len(captions)}")

    if len(images) == 0:
        print(f"  Warning: No images found in {dataset_path}")

    if len(captions) == 0:
        print(f"  Warning: No captions found in {dataset_path}")

    # Check pairing
    for img in images:
        base_name = os.path.splitext(img)[0]
        caption_file = base_name + '.txt'

        if caption_file not in captions:
            print(f"  Warning: Missing caption for {img}")
        else:
            caption_path = os.path.join(dataset_path, caption_file)
            try:
                with open(caption_path, 'r', encoding='utf-8') as f:
                    caption = f.read().strip()
                    if not caption.startswith('doom_'):
                        print(f"  Warning: {caption_file} doesn't start with 'doom_' trigger")
                        print(f"    Content: {caption[:50]}...")
            except Exception as e:
                print(f"  Error: Could not read {caption_file}: {e}")

    # Check for orphaned captions
    for caption in captions:
        base_name = os.path.splitext(caption)[0]
        has_image = any(
            img.startswith(base_name + '.') and img.endswith(('.jpg', '.jpeg', '.png'))
            for img in images
        )
        if not has_image:
            print(f"  Warning: Caption {caption} has no matching image")

print("\nValidation complete!")
