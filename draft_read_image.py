from GLOBALS import *


def read_image():
    # image_name = 'den520d.png'
    image_name = 'hrt201d.png'
    # image_name = 'Berlin_1_256.png'
    np_img = torchvision.io.read_image(f'maps/{image_name}', ImageReadMode.GRAY).squeeze().numpy()
    max_num = np.max(np_img)
    np_img_filtered = np.where(np_img < max_num, 0, 1)
    print(f'max num: {max_num}')

    plt.imshow(np_img)
    plt.show()

    plt.imshow(np_img_filtered)
    plt.show()

    print()


if __name__ == '__main__':
    read_image()
