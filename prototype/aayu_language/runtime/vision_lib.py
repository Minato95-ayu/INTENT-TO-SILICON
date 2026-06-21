from PIL import Image, ImageOps
import os

class AayuImage:
    """Wrapper class so AAYU VM can pass around images without knowing PIL details"""
    def __init__(self, img_obj):
        self.img = img_obj

def vision_load_image(filepath: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Image not found at {filepath}")
    img = Image.open(filepath)
    return AayuImage(img)

def vision_save_image(aayu_img: AayuImage, filepath: str):
    if not isinstance(aayu_img, AayuImage):
        raise ValueError("Invalid image object")
    # Ensure RGB for saving as jpeg if it was RGBA
    if filepath.lower().endswith(".jpg") or filepath.lower().endswith(".jpeg"):
        rgb_im = aayu_img.img.convert("RGB")
        rgb_im.save(filepath)
    else:
        aayu_img.img.save(filepath)
    return True

def vision_resize(aayu_img: AayuImage, width: int, height: int):
    if not isinstance(aayu_img, AayuImage):
        raise ValueError("Invalid image object")
    resized = aayu_img.img.resize((int(width), int(height)))
    return AayuImage(resized)

def vision_crop(aayu_img: AayuImage, left: int, top: int, right: int, bottom: int):
    if not isinstance(aayu_img, AayuImage):
        raise ValueError("Invalid image object")
    cropped = aayu_img.img.crop((int(left), int(top), int(right), int(bottom)))
    return AayuImage(cropped)

def vision_grayscale(aayu_img: AayuImage):
    if not isinstance(aayu_img, AayuImage):
        raise ValueError("Invalid image object")
    gray = ImageOps.grayscale(aayu_img.img)
    return AayuImage(gray)

# Module registry
VISION_MODULE = {
    "load_image": vision_load_image,
    "save_image": vision_save_image,
    "resize": vision_resize,
    "crop": vision_crop,
    "grayscale": vision_grayscale
}
