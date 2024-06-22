from PIL import Image

# Load the garment image
garment_image = Image.open('tt.jpeg')

# Load the mannequin image (you need to have a mannequin image for this)
mannequin_image = Image.open('mannequin.jpg')


# Resize the garment image to fit the mannequin (example size)
garment_image = garment_image.resize((mannequin_image.width, mannequin_image.height // 2))


# Overlay the garment image onto the mannequin image
mannequin_image.paste(garment_image, (0, mannequin_image.height // 4), garment_image)

# Save or display the result
mannequin_image.show()
# or
mannequin_image.save('path_to_output_image.jpg')
