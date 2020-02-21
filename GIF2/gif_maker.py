import glob
import imageio


file_list = glob.glob('*.png') # Get all the pngs in the current directory
list.sort(file_list, key=lambda x: int(x.split('_')[1].split('.png')[0])) # Sort the images by #, this may need to be tweaked for your use case



images = list()
for y in range(1,len(file_list)):
    images.append(imageio.imread('figure_' + str(y) + '.png'))
imageio.mimsave("Magnetic_emission.gif", images)