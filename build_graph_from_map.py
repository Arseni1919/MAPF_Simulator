import matplotlib.pyplot as plt

from GLOBALS import *


def build_graph_from_png(img_png, path='maps', show_map=False):
    nodes = []
    img_np = torchvision.io.read_image(f'{path}/{img_png}', ImageReadMode.GRAY).squeeze().numpy()
    max_num = np.max(img_np)
    img_filtered_np = np.where(img_np < max_num, 0, 1)

    if show_map:
        plt.imshow(img_filtered_np, cmap='gray')
        plt.show()

    

    return nodes


def main():
    # image_name = 'den520d.png'
    image_name = 'hrt201d.png'
    # image_name = 'Berlin_1_256.png'
    nodes = build_graph_from_png(image_name)


if __name__ == '__main__':
    main()
