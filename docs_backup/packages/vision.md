# aayu-vision

The `aayu-vision` package performs native image manipulations instantly in AAYU.

## Usage

```aayu
use vision.

task process_image.
    set "img" to vision.load_image("photo.jpg").
    set "bw" to vision.grayscale(img).
    vision.save_image(bw, "photo_bw.jpg").
end.
```

## Functions

- `vision.load_image(path)`: Loads an image from disk.
- `vision.save_image(img, path)`: Saves an image object to disk.
- `vision.resize(img, width, height)`: Resizes an image.
- `vision.crop(img, left, top, right, bottom)`: Crops an image.
- `vision.grayscale(img)`: Converts the image to black and white.
