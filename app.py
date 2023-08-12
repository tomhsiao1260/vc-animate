from PIL import Image, ImageDraw, ImageFont

def combine_images(image1_path, image2_path, output_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    width1, height1 = image1.size
    width2, height2 = image2.size

    combined_width = width1 + width2
    combined_height = max(height1, height2)

    combined_image = Image.new('RGB', (combined_width, combined_height))
    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (width1, 0))

    draw = ImageDraw.Draw(combined_image)
    font = ImageFont.truetype('./input/Roboto-Medium.ttf', 100)
    draw.text((10, 25), 'Layer 0', font=font)

    combined_image.save(output_path)

if __name__ == '__main__':
    image1_path = './input/segment/segment-0-50.png'
    image2_path = './input/layer/layer-0-50.png'
    output_path = 'combined_image.jpg'

    combine_images(image1_path, image2_path, output_path)

print('hi')