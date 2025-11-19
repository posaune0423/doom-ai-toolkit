#!/usr/bin/env python3
"""
Regenerate crypto logo dataset following the pattern from dataset_patterns.md
Preserves usecase images and renumbers them to continue after the new generation.

Usage:
    python scripts/regenerate_dataset.py <dataset_name> [--tag TAG] [--usecase-start START] [--usecase-end END]

Examples:
    python scripts/regenerate_dataset.py sol --tag "<$SOL>"
    python scripts/regenerate_dataset.py doge --tag "<$DOGE>" --usecase-start 57 --usecase-end 62
    python scripts/regenerate_dataset.py btc --tag "<$BTC>"
"""

import argparse
import os
import shutil
from typing import List, Optional, Tuple

from PIL import Image


def generate_dataset_patterns(
    logo_files: dict,
    tag: str = "<$SOL>",
    target_size: Tuple[int, int] = (1024, 1024),
    sizes: dict = None,
    rotations: List[int] = None,
    color_order: List[str] = None,
    size_order: List[str] = None,
) -> List[dict]:
    """
    Generate crypto logo dataset patterns with variations.

    The generation order is: Color → Size → Rotation
    This means for each color, all sizes are generated, and for each size, all rotations are generated.
    """
    if sizes is None:
        sizes = {"l": 1.0, "m": 0.7, "s": 0.3}

    if rotations is None:
        rotations = [0, 15, -15, 30, -30]

    if color_order is None:
        color_order = ["white", "black", "gray"]

    if size_order is None:
        size_order = ["l", "m", "s"]

    size_labels = {"l": "large", "m": "medium", "s": "small"}

    patterns = []
    counter = 1

    # Generate patterns: Color → Size → Rotation
    for color in color_order:
        for size in size_order:
            for rotation in rotations:
                size_desc = size_labels[size]
                rot_desc = "" if rotation == 0 else f", rotated {rotation} degrees"
                caption = (
                    f"{tag}, logo, {size_desc} size, {color} background{rot_desc}."
                )

                patterns.append(
                    {
                        "number": counter,
                        "color": color,
                        "size": size_desc,
                        "rotation": rotation,
                        "caption": caption,
                    }
                )
                counter += 1

    return patterns


def create_logo_image(
    logo_img: Image.Image,
    logo_scale: float,
    background_color: Tuple[int, int, int],
    target_size: Tuple[int, int],
    rotation_angle: int = 0,
) -> Image.Image:
    """
    Create a logo image variant with specified scale, background, and rotation.
    """
    logo_size = (int(target_size[0] * logo_scale), int(target_size[1] * logo_scale))
    resized_logo = logo_img.resize(logo_size, Image.LANCZOS)

    # Create background
    background = Image.new("RGB", target_size, background_color)
    x = (target_size[0] - logo_size[0]) // 2
    y = (target_size[1] - logo_size[1]) // 2

    # Paste logo
    if resized_logo.mode == "RGBA":
        background.paste(resized_logo, (x, y), resized_logo)
    else:
        background.paste(resized_logo, (x, y))

    # Rotate if needed
    if rotation_angle != 0:
        background = background.rotate(
            rotation_angle, expand=False, fillcolor=background_color
        )

    return background


def generate_dataset_images(
    logo_files: dict,
    tag: str = "<$SOL>",
    output_dir: str = "dataset/sol",
    target_size: Tuple[int, int] = (1024, 1024),
    sizes: dict = None,
    rotations: List[int] = None,
    color_order: List[str] = None,
    size_order: List[str] = None,
):
    """
    Generate all crypto logo dataset images and caption files.
    """
    # Get patterns
    patterns = generate_dataset_patterns(
        logo_files, tag, target_size, sizes, rotations, color_order, size_order
    )

    # Background colors
    bg_colors = {"white": (255, 255, 255), "black": (0, 0, 0), "gray": (128, 128, 128)}

    if sizes is None:
        sizes = {"l": 1.0, "m": 0.7, "s": 0.3}

    size_map = {"large": "l", "medium": "m", "small": "s"}

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate images
    for pattern in patterns:
        # Load logo
        logo_path = logo_files[pattern["color"]]
        logo_img = Image.open(logo_path)

        # Get scale
        size_key = size_map[pattern["size"]]
        logo_scale = sizes[size_key]

        # Get background color
        bg_color = bg_colors[pattern["color"]]

        # Create image
        img = create_logo_image(
            logo_img, logo_scale, bg_color, target_size, pattern["rotation"]
        )

        # Save image
        img_path = os.path.join(output_dir, f"{pattern['number']:04d}.png")
        img.save(img_path, "PNG")
        print(f"Generated: {img_path}")

        # Save caption
        txt_path = os.path.join(output_dir, f"{pattern['number']:04d}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(pattern["caption"])
        print(f"Generated: {txt_path}")


def find_usecase_images(output_dir: str) -> Optional[Tuple[int, int]]:
    """
    Automatically detect usecase images by finding the highest numbered files.
    Returns (start, end) tuple if found, None otherwise.

    Assumes usecase images start after a gap or are significantly higher than pattern images.
    """
    numbered_files = []
    for filename in os.listdir(output_dir):
        if filename.startswith("logo-"):
            continue
        if filename.endswith(".png") or filename.endswith(".txt"):
            try:
                num_str = filename[:4]
                num = int(num_str)
                numbered_files.append(num)
            except (ValueError, IndexError):
                continue

    if not numbered_files:
        return None

    numbered_files.sort()
    max_num = max(numbered_files)

    # Pattern generates 45 images, so if we have files > 45, assume they're usecase
    if max_num > 45:
        # Find the start of usecase images (first number > 45)
        usecase_start = None
        for num in numbered_files:
            if num > 45:
                usecase_start = num
                break

        if usecase_start:
            return (usecase_start, max_num)

    return None


def preserve_and_renumber_usecase_images(
    output_dir: str, new_start: int, usecase_start: int, usecase_end: int
):
    """
    Preserve usecase images by renumbering them to continue after the new generation.

    Args:
        output_dir: Output directory
        new_start: Starting number for usecase images (should be 46 if new generation ends at 45)
        usecase_start: Current starting number of usecase images (e.g., 57)
        usecase_end: Current ending number of usecase images (e.g., 62)
    """
    print(f"\nPreserving usecase images {usecase_start:04d}-{usecase_end:04d}...")

    # First, move usecase images to temporary names to avoid conflicts
    temp_files = []
    for num in range(usecase_start, usecase_end + 1):
        old_img = os.path.join(output_dir, f"{num:04d}.png")
        old_txt = os.path.join(output_dir, f"{num:04d}.txt")
        temp_img = os.path.join(output_dir, f"temp_{num:04d}.png")
        temp_txt = os.path.join(output_dir, f"temp_{num:04d}.txt")

        if os.path.exists(old_img):
            shutil.move(old_img, temp_img)
            temp_files.append((num, temp_img, None))
        if os.path.exists(old_txt):
            shutil.move(old_txt, temp_txt)
            if temp_files and temp_files[-1][0] == num:
                temp_files[-1] = (num, temp_files[-1][1], temp_txt)
            else:
                temp_files.append((num, None, temp_txt))

    # Now rename them to their new numbers
    for old_num, temp_img, temp_txt in temp_files:
        new_num = new_start + (old_num - usecase_start)
        if temp_img:
            new_img = os.path.join(output_dir, f"{new_num:04d}.png")
            shutil.move(temp_img, new_img)
            print(f"Renumbered: {old_num:04d}.png -> {new_num:04d}.png")
        if temp_txt:
            new_txt = os.path.join(output_dir, f"{new_num:04d}.txt")
            shutil.move(temp_txt, new_txt)
            print(f"Renumbered: {old_num:04d}.txt -> {new_num:04d}.txt")


def cleanup_old_files(output_dir: str, keep_start: int, keep_end: int):
    """
    Remove old dataset files except for logo files and usecase images.

    Args:
        output_dir: Output directory
        keep_start: First file number to keep (e.g., 1 for new generation)
        keep_end: Last file number to keep (e.g., 51 if usecase images end at 51)
    """
    print(
        f"\nCleaning up old files (keeping {keep_start:04d}-{keep_end:04d} and logo files)..."
    )

    # Find all numbered files
    deleted_count = 0
    for filename in os.listdir(output_dir):
        if filename.startswith("logo-"):
            continue  # Keep logo files

        # Check if it's a numbered file
        if filename.endswith(".png") or filename.endswith(".txt"):
            try:
                num_str = filename[:4]
                num = int(num_str)

                # Delete if outside the range we want to keep
                if num < keep_start or num > keep_end:
                    filepath = os.path.join(output_dir, filename)
                    os.remove(filepath)
                    print(f"Deleted: {filename}")
                    deleted_count += 1
            except (ValueError, IndexError):
                # Not a numbered file, skip
                pass

    if deleted_count == 0:
        print("No old files to clean up.")


def find_logo_files(dataset_dir: str) -> dict:
    """
    Find logo files in the _controls folder of the dataset directory.
    Tries different extensions: .png, .jpg, .jpeg
    """
    logo_files = {}
    colors = ["white", "black", "gray"]
    extensions = [".png", ".jpg", ".jpeg"]

    # Look for logo files in _controls folder first, then fallback to dataset_dir
    logo_base_dir = os.path.join(dataset_dir, "_controls")
    if not os.path.exists(logo_base_dir):
        logo_base_dir = dataset_dir

    for color in colors:
        found = False
        for ext in extensions:
            logo_path = os.path.join(logo_base_dir, f"logo-{color}{ext}")
            if os.path.exists(logo_path):
                logo_files[color] = logo_path
                found = True
                break

        if not found:
            raise FileNotFoundError(
                f"Logo file not found for {color} color in {logo_base_dir}\n"
                f"Expected: logo-{color}.png (or .jpg/.jpeg) in {logo_base_dir}"
            )

    return logo_files


def main():
    parser = argparse.ArgumentParser(
        description="Regenerate crypto logo dataset following the pattern from dataset_patterns.md",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/regenerate_dataset.py sol --tag "<$SOL>"
  python scripts/regenerate_dataset.py doge --tag "<$DOGE>" --usecase-start 57 --usecase-end 62
  python scripts/regenerate_dataset.py btc --tag "<$BTC>"
        """,
    )

    parser.add_argument(
        "dataset_name",
        type=str,
        help="Name of the dataset folder (e.g., sol, doge, btc)",
    )

    parser.add_argument(
        "--tag",
        type=str,
        default=None,
        help='Caption tag for the logo (e.g., "<$SOL>", "<$DOGE>"). Defaults to "<$DATASET_NAME>"',
    )

    parser.add_argument(
        "--usecase-start",
        type=int,
        default=None,
        help="Starting number of usecase images to preserve (e.g., 57). Auto-detected if not specified.",
    )

    parser.add_argument(
        "--usecase-end",
        type=int,
        default=None,
        help="Ending number of usecase images to preserve (e.g., 62). Auto-detected if not specified.",
    )

    parser.add_argument(
        "--dataset-dir",
        type=str,
        default=None,
        help="Base directory for datasets (default: dataset/)",
    )

    args = parser.parse_args()

    # Get the script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Determine dataset directory
    if args.dataset_dir:
        dataset_dir = os.path.abspath(args.dataset_dir)
    else:
        dataset_dir = os.path.join(project_root, "dataset", args.dataset_name)

    # Determine tag
    tag = args.tag if args.tag is not None else f"<${args.dataset_name.upper()}>"

    # Find logo files
    try:
        logo_files = find_logo_files(dataset_dir)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    print(f"Regenerating {args.dataset_name.upper()} dataset in: {dataset_dir}")
    print(f"Tag: {tag}")
    print(
        "Pattern: Color → Size → Rotation (3 colors × 3 sizes × 5 rotations = 45 images)"
    )

    # Detect usecase images if not specified
    usecase_start = args.usecase_start
    usecase_end = args.usecase_end

    if usecase_start is None or usecase_end is None:
        detected = find_usecase_images(dataset_dir)
        if detected:
            detected_start, detected_end = detected
            if usecase_start is None:
                usecase_start = detected_start
            if usecase_end is None:
                usecase_end = detected_end
            print(
                f"Auto-detected usecase images: {usecase_start:04d}-{usecase_end:04d}"
            )
        elif usecase_start is None and usecase_end is None:
            print("No usecase images detected. Generating pattern images only.")

    new_generation_end = 45  # Pattern generates 45 images
    new_usecase_start = 46  # Usecase images start after pattern images

    # Step 1: Preserve usecase images if they exist
    if usecase_start is not None and usecase_end is not None:
        print("\nThis will:")
        print(
            f"  1. Generate new images 0001-{new_generation_end:04d} according to the pattern"
        )
        print(
            f"  2. Renumber usecase images {usecase_start:04d}-{usecase_end:04d} to {new_usecase_start:04d}-{new_usecase_start + (usecase_end - usecase_start):04d}"
        )
        print(f"  3. Delete old files 0001-{usecase_end:04d} (except logo files)")

        preserve_and_renumber_usecase_images(
            dataset_dir, new_usecase_start, usecase_start, usecase_end
        )
    else:
        print("\nThis will:")
        print(
            f"  1. Generate new images 0001-{new_generation_end:04d} according to the pattern"
        )
        print("  2. Delete old files (except logo files)")

    # Step 2: Generate new dataset images (0001-0045)
    print(f"\nGenerating new dataset images 0001-{new_generation_end:04d}...")
    generate_dataset_images(logo_files, tag=tag, output_dir=dataset_dir)

    # Step 3: Clean up old files
    if usecase_start is not None and usecase_end is not None:
        final_end = new_usecase_start + (usecase_end - usecase_start)
    else:
        final_end = new_generation_end

    cleanup_old_files(dataset_dir, 1, final_end)

    print("\nDone! Dataset regenerated successfully.")
    if usecase_start is not None and usecase_end is not None:
        print(
            f"Total images: {final_end} (0001-{new_generation_end:04d} pattern images + {new_usecase_start:04d}-{final_end:04d} usecase images)"
        )
    else:
        print(f"Total images: {final_end} (0001-{final_end:04d} pattern images)")

    return 0


if __name__ == "__main__":
    exit(main())
