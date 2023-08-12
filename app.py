import os
import cv2
from PIL import Image, ImageDraw, ImageFont

if not os.path.exists('output'):
    os.makedirs('output')

def combine_images(image1_path, image2_path, output_path, text):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    width1, height1 = image1.size
    width2, height2 = image2.size

    combined_width = width1 + width2
    combined_height = max(height1, height2)

    combined_image = Image.new('RGB', (combined_width, combined_height))
    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (width1, 0))

    # https://fonts.google.com/specimen/Roboto
    draw = ImageDraw.Draw(combined_image)
    font = ImageFont.truetype('./input/Roboto-Medium.ttf', 100)
    draw.text((10, 25), text, font=font)

    combined_image.save(output_path)

if __name__ == '__main__':
    for i in range(10):
        image1_path = f'./input/segment/segment-{i * 50}-50.png'
        image2_path = f'./input/layer/layer-{i * 50}-50.png'
        output_path = f'./output/{i * 50}.jpg'

        combine_images(image1_path, image2_path, output_path, f'Layer {i * 50}')

    image_files = sorted(os.listdir('output'))
    frame_rate = 10
    output_video_path = 'output_video.mp4'

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (5760, 1566))

    for image_file in image_files:
        image_path = os.path.join('output', image_file)
        frame = cv2.imread(image_path)
        video_writer.write(frame)

    video_writer.release()

