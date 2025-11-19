# Crypto Logo Dataset Pattern Documentation

## Overview

This document describes a reusable pattern generation system for creating crypto logo datasets with variations. The system generates images with different sizes, background colors, and rotation angles. All images are **1024x1024 pixels** in PNG format.

## Prerequisites

Before using this pattern generation system, you need to prepare the following logo files:

- **White background logo**: 1024x1024 pixels PNG file (e.g., `_controls/logo-white.png`)
- **Black background logo**: 1024x1024 pixels PNG file (e.g., `_controls/logo-black.png`)
- **Gray background logo**: 1024x1024 pixels PNG file (e.g., `_controls/logo-gray.png`)

**Note**: Logo files should be placed in the `_controls` folder to prevent them from being included in the training dataset.

All logo files should be:

- **Size**: Exactly 1024x1024 pixels
- **Format**: PNG (preferably RGBA format to support transparency)
- **Background**: Each logo should have its corresponding background color (white, black, or gray)

The logo itself should be centered on the background. The system will resize and rotate these base logos to create variations.

## Dataset Specifications

- **Format**: PNG (1024x1024)
- **Sizes**:
  - **Large**: 100% scale
  - **Medium**: 70% scale
  - **Small**: 30% scale
- **Colors**: White, Black, Gray
- **Rotations**: 0°, 15°, -15°, 30°, -30°

## Image List

The dataset follows a systematic order: **Color → Size → Rotation**. For each color, all sizes are generated, and for each size, all rotations are generated.

| No.  | Color | Size   | Rotation | Description |
| ---- | ----- | ------ | -------- | ----------- |
| 0001 | White | Large  | 0°       | Normal      |
| 0002 | White | Large  | 15°      | Rotated     |
| 0003 | White | Large  | -15°     | Rotated     |
| 0004 | White | Large  | 30°      | Rotated     |
| 0005 | White | Large  | -30°     | Rotated     |
| 0006 | White | Medium | 0°       | Normal      |
| 0007 | White | Medium | 15°      | Rotated     |
| 0008 | White | Medium | -15°     | Rotated     |
| 0009 | White | Medium | 30°      | Rotated     |
| 0010 | White | Medium | -30°     | Rotated     |
| 0011 | White | Small  | 0°       | Normal      |
| 0012 | White | Small  | 15°      | Rotated     |
| 0013 | White | Small  | -15°     | Rotated     |
| 0014 | White | Small  | 30°      | Rotated     |
| 0015 | White | Small  | -30°     | Rotated     |
| 0016 | Black | Large  | 0°       | Normal      |
| 0017 | Black | Large  | 15°      | Rotated     |
| 0018 | Black | Large  | -15°     | Rotated     |
| 0019 | Black | Large  | 30°      | Rotated     |
| 0020 | Black | Large  | -30°     | Rotated     |
| 0021 | Black | Medium | 0°       | Normal      |
| 0022 | Black | Medium | 15°      | Rotated     |
| 0023 | Black | Medium | -15°     | Rotated     |
| 0024 | Black | Medium | 30°      | Rotated     |
| 0025 | Black | Medium | -30°     | Rotated     |
| 0026 | Black | Small  | 0°       | Normal      |
| 0027 | Black | Small  | 15°      | Rotated     |
| 0028 | Black | Small  | -15°     | Rotated     |
| 0029 | Black | Small  | 30°      | Rotated     |
| 0030 | Black | Small  | -30°     | Rotated     |
| 0031 | Gray  | Large  | 0°       | Normal      |
| 0032 | Gray  | Large  | 15°      | Rotated     |
| 0033 | Gray  | Large  | -15°     | Rotated     |
| 0034 | Gray  | Large  | 30°      | Rotated     |
| 0035 | Gray  | Large  | -30°     | Rotated     |
| 0036 | Gray  | Medium | 0°       | Normal      |
| 0037 | Gray  | Medium | 15°      | Rotated     |
| 0038 | Gray  | Medium | -15°     | Rotated     |
| 0039 | Gray  | Medium | 30°      | Rotated     |
| 0040 | Gray  | Medium | -30°     | Rotated     |
| 0041 | Gray  | Small  | 0°       | Normal      |
| 0042 | Gray  | Small  | 15°      | Rotated     |
| 0043 | Gray  | Small  | -15°     | Rotated     |
| 0044 | Gray  | Small  | 30°      | Rotated     |
| 0045 | Gray  | Small  | -30°     | Rotated     |

## Caption Format

The caption format uses descriptive text with the trigger word embedded. For SOL logo example:

```
A [size] cgl_sol logo made of three stacked slanted rectangles forming an S-shaped mark, with a colorful gradient, on a [color] background[, rotated [angle] degrees].
```

Where:
- `[size]` is replaced with: `large`, `medium`, or `small`
- `[color]` is replaced with: `white`, `black`, or `gray`
- `[, rotated [angle] degrees]` is added only when rotation is not 0°

Example captions:
- `A large cgl_sol logo made of three stacked slanted rectangles forming an S-shaped mark, with a colorful gradient, on a white background.`
- `A medium cgl_sol logo made of three stacked slanted rectangles forming an S-shaped mark, with a colorful gradient, on a black background, rotated 15 degrees.`

For other crypto logos, replace `cgl_sol` with the appropriate trigger word (e.g., `cgl_btc`, `cgl_eth`, etc.).

## Generation Function

Here's a reusable Python function to generate dataset patterns for any crypto logo:

```python
from PIL import Image
from typing import List, Tuple, Optional

def generate_dataset_patterns(
    logo_files: dict,
    tag: str = 'cgl_sol',
    target_size: Tuple[int, int] = (1024, 1024),
    sizes: dict = None,
    rotations: List[int] = None,
    color_order: List[str] = None,
    size_order: List[str] = None
) -> List[dict]:
    """
    Generate crypto logo dataset patterns with variations.

    The generation order is: Color → Size → Rotation
    This means for each color, all sizes are generated, and for each size, all rotations are generated.

    Args:
        logo_files: Dict mapping color names to logo file paths
            e.g., {'white': 'logo-white.png', 'black': 'logo-black.png', 'gray': 'logo-gray.png'}
        tag: Trigger word for the logo (e.g., 'cgl_sol', 'cgl_btc', 'cgl_eth')
        target_size: Output image size (width, height)
        sizes: Dict mapping size names to scale factors
            e.g., {'l': 1.0, 'm': 0.7, 's': 0.3}
        rotations: List of rotation angles in degrees (default: [0, 15, -15, 30, -30])
        color_order: List of color names in order (default: ['white', 'black', 'gray'])
        size_order: List of size keys in order (default: ['l', 'm', 's'])

    Returns:
        List of dicts with pattern information:
        [
            {
                'number': 1,
                'color': 'white',
                'size': 'large',
                'rotation': 0,
                'caption': 'A large cgl_sol logo made of three stacked slanted rectangles forming an S-shaped mark, with a colorful gradient, on a white background.'
            },
            ...
        ]
    """
    if sizes is None:
        sizes = {'l': 1.0, 'm': 0.7, 's': 0.3}

    if rotations is None:
        rotations = [0, 15, -15, 30, -30]

    if color_order is None:
        color_order = ['white', 'black', 'gray']

    if size_order is None:
        size_order = ['l', 'm', 's']

    size_labels = {'l': 'large', 'm': 'medium', 's': 'small'}

    patterns = []
    counter = 1

    # Generate patterns: Color → Size → Rotation
    for color in color_order:
        for size in size_order:
            for rotation in rotations:
                size_desc = size_labels[size]
                rot_text = f", rotated {abs(rotation)} degrees" if rotation != 0 else ""
                caption = f"A {size_desc} {tag} logo made of three stacked slanted rectangles forming an S-shaped mark, with a colorful gradient, on a {color} background{rot_text}."

                patterns.append({
                    'number': counter,
                    'color': color,
                    'size': size_desc,
                    'rotation': rotation,
                    'caption': caption
                })
                counter += 1

    return patterns


def create_logo_image(
    logo_img: Image.Image,
    logo_scale: float,
    background_color: Tuple[int, int, int],
    target_size: Tuple[int, int],
    rotation_angle: int = 0
) -> Image.Image:
    """
    Create a logo image variant with specified scale, background, and rotation.

    Args:
        logo_img: PIL Image object of the logo
        logo_scale: Scale factor for logo (0.0 to 1.0)
        background_color: RGB tuple for background color
        target_size: Output image size (width, height)
        rotation_angle: Rotation angle in degrees (counter-clockwise)

    Returns:
        PIL Image object
    """
    logo_size = (int(target_size[0] * logo_scale), int(target_size[1] * logo_scale))
    resized_logo = logo_img.resize(logo_size, Image.LANCZOS)

    # Create background
    background = Image.new('RGB', target_size, background_color)
    x = (target_size[0] - logo_size[0]) // 2
    y = (target_size[1] - logo_size[1]) // 2

    # Paste logo
    if resized_logo.mode == 'RGBA':
        background.paste(resized_logo, (x, y), resized_logo)
    else:
        background.paste(resized_logo, (x, y))

    # Rotate if needed
    if rotation_angle != 0:
        background = background.rotate(rotation_angle, expand=False, fillcolor=background_color)

    return background


def generate_dataset_images(
    logo_files: dict,
    tag: str = 'cgl_sol',
    output_dir: str = 'dataset/sol',
    target_size: Tuple[int, int] = (1024, 1024),
    sizes: dict = None,
    rotations: List[int] = None,
    color_order: List[str] = None,
    size_order: List[str] = None
):
    """
    Generate all crypto logo dataset images and caption files.

    Args:
        logo_files: Dict mapping color names to logo file paths
        tag: Trigger word for the logo (e.g., 'cgl_sol', 'cgl_btc', 'cgl_eth')
        output_dir: Output directory for images and captions
        target_size: Output image size
        sizes: Dict mapping size names to scale factors
        rotations: List of rotation angles in degrees
        color_order: List of color names in order
        size_order: List of size keys in order
    """
    import os

    # Get patterns
    patterns = generate_dataset_patterns(
        logo_files, tag, target_size, sizes, rotations, color_order, size_order
    )

    # Background colors
    bg_colors = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'gray': (128, 128, 128)
    }

    if sizes is None:
        sizes = {'l': 1.0, 'm': 0.7, 's': 0.3}

    size_map = {'large': 'l', 'medium': 'm', 'small': 's'}

    # Generate images
    for pattern in patterns:
        # Load logo
        logo_path = logo_files[pattern['color']]
        logo_img = Image.open(logo_path)

        # Get scale
        size_key = size_map[pattern['size']]
        logo_scale = sizes[size_key]

        # Get background color
        bg_color = bg_colors[pattern['color']]

        # Create image
        img = create_logo_image(logo_img, logo_scale, bg_color, target_size, pattern['rotation'])

        # Save image
        img_path = os.path.join(output_dir, f"{pattern['number']:04d}.png")
        img.save(img_path, 'PNG')

        # Save caption
        txt_path = os.path.join(output_dir, f"{pattern['number']:04d}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(pattern['caption'])


# Example usage:

# Example 1: SOL logo
if __name__ == '__main__':
    sol_logo_files = {
        'white': 'dataset/sol/_controls/logo-white.png',
        'black': 'dataset/sol/_controls/logo-black.png',
        'gray': 'dataset/sol/_controls/logo-gray.png'
    }

    # Generate SOL patterns (metadata only)
    sol_patterns = generate_dataset_patterns(sol_logo_files, tag='cgl_sol')
    for p in sol_patterns[:5]:  # Show first 5
        print(f"{p['number']:04d}: {p['caption']}")

    # Generate all SOL images and captions
    # generate_dataset_images(sol_logo_files, tag='cgl_sol', output_dir='dataset/sol')

# Example 2: Bitcoin logo
# btc_logo_files = {
#     'white': 'dataset/btc/_controls/logo-white.png',
#     'black': 'dataset/btc/_controls/logo-black.png',
#     'gray': 'dataset/btc/_controls/logo-gray.png'
# }
# generate_dataset_images(btc_logo_files, tag='cgl_btc', output_dir='dataset/btc')

# Example 3: Custom configuration
# custom_patterns = generate_dataset_patterns(
#     logo_files={'white': 'logo.png'},
#     tag='cgl_custom',
#     color_order=['white'],  # Only white background
#     size_order=['l', 'm'],  # Only large and medium
#     rotations=[0, 15, 30, -15]  # Custom rotation angles
# )
```
