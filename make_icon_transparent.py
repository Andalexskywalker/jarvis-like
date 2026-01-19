from PIL import Image

def make_transparent(input_path, output_path):
    img = Image.open(input_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    # Simple thresholding: anything super dark becomes transparent
    # Alternatively, if it was white, anything super bright becomes transparent.
    # The new prompt was "solid black background".
    for item in datas:
        # Change all black (also dark shades) pixels to transparent
        if item[0] < 30 and item[1] < 30 and item[2] < 30:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Transparency applied. Saved to {output_path}")

if __name__ == "__main__":
    make_transparent("friday_icon_new.png", "friday_icon.png")
