import os
import cv2
import shutil
from PIL import Image, ImageDraw, ImageFont

if os.path.exists('output'):
    shutil.rmtree('output')
    os.makedirs('output')

def combine_images(image1_path, image2_path, output_path, text):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    w1, h1 = image1.size
    w2, h2 = image2.size

    # left, upper, right, lower
    image1 = image1.crop((w1/2 - w1/4.5, h1/2 - h1/3, w1/2 + w1/4.5, h1/2 + h1/3))
    image2 = image2.crop((w2/2 - w2/4, h2/2 - h2/2, w2/2 + w2/4, h2/2 + h2/4))

    w1, h1 = image1.size
    w2, h2 = image2.size

    c_w = w1 + w2
    c_h = max(h1, h2)
    u = int(max(c_w / 16, c_h / 9))
    st_w = int((u * 16 - c_w) / 2)
    st_h = int((u * 9 - c_h) / 2)

    combined_image = Image.new('RGB', (u*16, u *9))
    combined_image.paste(image1, (0 + st_w, int((c_h - h1)/2) + st_h))
    combined_image.paste(image2, (w1 + st_w, int((c_h - h2)/2) + st_h))

    # https://fonts.google.com/specimen/Roboto
    draw = ImageDraw.Draw(combined_image)
    font = ImageFont.truetype('./input/Roboto-Medium.ttf', 50)
    draw.text((150, u*9 - 200), text, font=font)

    resized_image = combined_image.resize((int(u*16/3), int(u*9/3)))
    resized_image.save(output_path)

if __name__ == '__main__':
    for i in range(288):
        image1_path = f'./input/segment/segment-{i * 50}-50.png'
        image2_path = f'./input/layer/layer-{i * 50}-50.png'
        output_path = f'./output/{i:03}.jpg'

        if (i == 287):
            image1_path = f'./input/segment/segment-{i * 50}-20.png'
            image2_path = f'./input/layer/layer-{i * 50}-20.png'

        combine_images(image1_path, image2_path, output_path, f'Layer {i * 50}')

    image_files = sorted(os.listdir('output'))
    frame_rate = 10
    output_video_path = 'output.mp4'

    first_image = Image.open('./output/000.jpg')
    w, h = first_image.size

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (w, h))

    for image_file in image_files:
        image_path = os.path.join('output', image_file)
        frame = cv2.imread(image_path)
        video_writer.write(frame)

    video_writer.release()

