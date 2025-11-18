#!/usr/bin/env python3
"""
Generate logo variations with different colors, scales, and rotations.
"""

import os
import sys
from PIL import Image, ImageOps
import shutil
from pathlib import Path


def generate_variations(dataset_name):
    """Generate logo variations and renumber existing files."""

    dataset_dir = Path(f"dataset/{dataset_name}")

    # Detect logo file extensions
    logo_extensions = {
        "white": [".jpg", ".jpeg", ".png"],
        "black": [".png"],
        "gray": [".png"],
    }

    # Logo files - try different extensions
    logo_files = {}
    for color, extensions in logo_extensions.items():
        found = False
        for ext in extensions:
            logo_path = dataset_dir / f"logo-{color}{ext}"
            if logo_path.exists():
                logo_files[color] = logo_path
                found = True
                break
        if not found:
            raise FileNotFoundError(f"Logo file not found for {color} color in {dataset_dir}")

    # Verify logo files exist
    for color, logo_path in logo_files.items():
        if not logo_path.exists():
            raise FileNotFoundError(f"Logo file not found: {logo_path}")

    # Variations
    colors = ["white", "black", "gray"]
    scales = {"large": 1.5, "medium": 1.0, "small": 0.7}
    rotations = [10, -10, 20, -20, 30, -30]

    # Caption templates
    captions = {
        "white": f"doom_{dataset_name} logo, flat design, white background.",
        "black": f"doom_{dataset_name} logo, flat design, black background.",
        "gray": f"doom_{dataset_name} logo, flat design, gray background.",
    }

    # First, renumber existing files (0001-0008 -> 0055-0062) to avoid conflicts
    print("Renumbering existing files...")
    existing_files = []
    for i in range(1, 9):  # 0001 to 0008
        # Check for both .png and .jpg extensions
        img_extensions = [".png", ".jpg", ".jpeg"]
        found_ext = None
        for ext in img_extensions:
            img_file = dataset_dir / f"{i:04d}{ext}"
            if img_file.exists():
                found_ext = ext
                break

        txt_file = dataset_dir / f"{i:04d}.txt"
        if found_ext or txt_file.exists():
            existing_files.append((i, found_ext if found_ext else ".png"))

    # Renumber in reverse order to avoid conflicts
    # 0001-0002 -> 0055-0056, 0003-0008 -> 0057-0062
    for old_num, img_ext in reversed(existing_files):
        if old_num <= 2:
            new_num = old_num + 54  # 0001 -> 0055, 0002 -> 0056
        else:
            new_num = old_num + 54  # 0003 -> 0057, 0004 -> 0058, etc.

        old_img = dataset_dir / f"{old_num:04d}{img_ext}"
        old_txt = dataset_dir / f"{old_num:04d}.txt"
        new_img = dataset_dir / f"{new_num:04d}{img_ext}"
        new_txt = dataset_dir / f"{new_num:04d}.txt"

        if old_img.exists():
            shutil.move(str(old_img), str(new_img))
            print(f"Moved {old_img.name} -> {new_img.name}")

        if old_txt.exists():
            shutil.move(str(old_txt), str(new_txt))
            print(f"Moved {old_txt.name} -> {new_txt.name}")

    print("\nGenerating logo variations...")

    # Generate 0001 and 0002 first (white and black, medium scale, no rotation)
    print("Generating base logo variations (0001-0002)...")

    # 0001: white, medium scale, no rotation
    logo_path = logo_files["white"]
    img = Image.open(logo_path).convert("RGBA")
    final_img = Image.new("RGBA", (img.width + 100, img.height + 100), (0, 0, 0, 0))
    final_x = (final_img.width - img.width) // 2
    final_y = (final_img.height - img.height) // 2
    final_img.paste(img, (final_x, final_y), img)
    output_path = dataset_dir / "0001.png"
    final_img.save(output_path, "PNG")
    with open(dataset_dir / "0001.txt", "w", encoding="utf-8") as f:
        f.write(captions["white"] + "\n")
    print("Generated: 0001.png (color=white, scale=medium, rotation=0°)")

    # 0002: black, medium scale, no rotation
    logo_path = logo_files["black"]
    img = Image.open(logo_path).convert("RGBA")
    final_img = Image.new("RGBA", (img.width + 100, img.height + 100), (0, 0, 0, 0))
    final_x = (final_img.width - img.width) // 2
    final_y = (final_img.height - img.height) // 2
    final_img.paste(img, (final_x, final_y), img)
    output_path = dataset_dir / "0002.png"
    final_img.save(output_path, "PNG")
    with open(dataset_dir / "0002.txt", "w", encoding="utf-8") as f:
        f.write(captions["black"] + "\n")
    print("Generated: 0002.png (color=black, scale=medium, rotation=0°)")

    # Generate all variations starting from 0003
    variation_num = 3  # Start from 0003

    for color in colors:
        for scale_name, scale_factor in scales.items():
            for rotation in rotations:
                # Load original logo
                logo_path = logo_files[color]
                img = Image.open(logo_path).convert("RGBA")

                # Get original size
                original_width, original_height = img.size

                # Apply scale
                if scale_factor != 1.0:
                    new_width = int(original_width * scale_factor)
                    new_height = int(original_height * scale_factor)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Create a larger canvas to accommodate rotation
                # Calculate diagonal length to ensure no clipping
                diagonal = int((img.width ** 2 + img.height ** 2) ** 0.5) + 20
                canvas = Image.new("RGBA", (diagonal, diagonal), (0, 0, 0, 0))

                # Paste image in center
                paste_x = (diagonal - img.width) // 2
                paste_y = (diagonal - img.height) // 2
                canvas.paste(img, (paste_x, paste_y), img if img.mode == "RGBA" else None)

                # Apply rotation
                rotated = canvas.rotate(rotation, expand=False, fillcolor=(0, 0, 0, 0))

                # Crop to content (remove transparent edges)
                bbox = rotated.getbbox()
                if bbox:
                    rotated = rotated.crop(bbox)

                # Create a square canvas with padding
                max_dim = max(rotated.width, rotated.height)
                padding = 50
                final_size = max_dim + padding * 2
                final_img = Image.new("RGBA", (final_size, final_size), (0, 0, 0, 0))

                # Paste rotated image in center
                final_x = (final_size - rotated.width) // 2
                final_y = (final_size - rotated.height) // 2
                final_img.paste(rotated, (final_x, final_y), rotated)

                # Save image
                output_filename = f"{variation_num:04d}.png"
                output_path = dataset_dir / output_filename
                final_img.save(output_path, "PNG")

                # Save caption
                caption_filename = f"{variation_num:04d}.txt"
                caption_path = dataset_dir / caption_filename
                with open(caption_path, "w", encoding="utf-8") as f:
                    f.write(captions[color] + "\n")

                print(f"Generated: {output_filename} (color={color}, scale={scale_name}, rotation={rotation}°)")
                variation_num += 1

    print(f"\nGenerated {variation_num - 3} variations (0003-{variation_num-1:04d})")
    print("\nDone!")


if __name__ == "__main__":
    # Change to script directory's parent (project root)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    # Get dataset name from command line argument or default to "sol"
    dataset_name = sys.argv[1] if len(sys.argv) > 1 else "sol"

    print(f"Generating logo variations for dataset: {dataset_name}\n")
    generate_variations(dataset_name)
