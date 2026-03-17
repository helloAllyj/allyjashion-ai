"""
Convert HEIC images to JPG with progress tracking and resizing
"""

from PIL import Image
from pillow_heif import register_heif_opener
import os
from pathlib import Path
from tqdm import tqdm  # Progress bar

# Enable HEIC support in Pillow
register_heif_opener()

def convert_heic_to_jpg(input_folder, output_folder, max_size=1024):
    """
    Convert all HEIC files to JPG
    
    Args:
        input_folder: Folder with HEIC images
        output_folder: Where to save JPGs
        max_size: Max width/height (keeps aspect ratio). Default 1024px
    """
    
    # Create output folder
    os.makedirs(output_folder, exist_ok=True)
    
    # Find all HEIC files (case insensitive)
    heic_files = list(Path(input_folder).glob("*.heic")) + \
                 list(Path(input_folder).glob("*.HEIC"))
    
    if len(heic_files) == 0:
        print(f"❌ No HEIC files found in '{input_folder}'")
        print("Make sure your HEIC images are in that folder!")
        return
    
    print(f"Found {len(heic_files)} HEIC files")
    print(f"Converting to JPG (max size: {max_size}px)...\n")
    
    # Convert with progress bar
    for heic_path in tqdm(heic_files, desc="Converting"):
        try:
            # Open HEIC
            img = Image.open(heic_path)
            
            # Convert to RGB if needed
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGB")
            
            # Resize if image is too large (saves space, faster upload)
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Create JPG filename (keep original name)
            jpg_filename = heic_path.stem + ".jpg"
            jpg_path = Path(output_folder) / jpg_filename
            
            # Save as JPG (quality 90 is good balance)
            img.save(jpg_path, "JPEG", quality=90, optimize=True)
            
        except Exception as e:
            print(f"\n❌ Error converting {heic_path.name}: {e}")
    
    print(f"\n✅ Done! Converted {len(heic_files)} images to '{output_folder}'")
    
    # Show total size
    total_size = sum(f.stat().st_size for f in Path(output_folder).glob("*.jpg"))
    print(f"📦 Total size: {total_size / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    # Configuration
    input_folder = "heic_images"      # Put your HEIC files here
    output_folder = "converted_jpg"   # JPGs will go here
    
    convert_heic_to_jpg(input_folder, output_folder, max_size=1024)