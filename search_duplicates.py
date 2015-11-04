__author__ = 'samipc'
from PIL import Image
import os


def searchduplicate(image, has_size=8):
    image = image.convert('L').resize((has_size + 1, has_size), Image.ANTIALIAS, )

    px = list(image.getdata())

    diff = []
    for row in xrange(has_size):
        for col in xrange(has_size):
            px_left = image.getpixel((col, row))
            px_right = image.getpixel((col + 1, row))
            diff.append(px_left > px_right)
    dic_value = 0
    hex_string = []
    for index, value in enumerate(diff):
        if value:
            dic_value += 2 ** (index % 8)
        if (index % 8) == 7:
            hex_string.append((hex(dic_value)[2:].rjust(2, '0')))
            dic_value = 0
    return ''.join(hex_string)


def remove_duplicate(path):
    clean_images = []
    non_duplicate = []
    # Walk the tree.
    for root, directories, files in os.walk(path):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            if '.png' not in filepath:
               continue
            im = Image.open(filepath)
            hash_text = searchduplicate(im);
            if hash_text in non_duplicate:
                print '{0} duplicate(remove it)'.format(filepath)
            # check if it is already exist in the list
            if hash_text not in non_duplicate:
                non_duplicate.append(hash_text)
                clean_images.append(filepath)
    return clean_images

#                 main
##########################################
path = '/home/samipc/'

cl_data = remove_duplicate(path)
# write to a file
fl = open(path + 'clean_images.txt', 'w')
for filepath in cl_data:
    gs = filepath.encode('utf-8')
    try:
        fl.write(gs + '\n')
    except:
        print "cant not read {0}".format(filepath)
fl.close()
