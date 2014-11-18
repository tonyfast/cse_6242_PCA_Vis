import time
from sklearn.decomposition import KernelPCA
from image_dimension_reducer import ImageDimensionReducer
from pymks.tools import draw_PCA

reducer = KernelPCA(n_components=3)
IDR = ImageDimensionReducer(reducer=reducer)

t_start = time.time()
#IDR.load_images('/Users/abhiramkannan/Documents/SAXS_for_DB/', '.tif')
IDR.load_images(directory_path='/home/david/Pictures/SAXS_for_DB/',
                file_type='.tif', dataset_name='SAX_2')
print 'Loaded Data in', time.time() - t_start, 'sec'


t_start = time.time()
X_PCA = IDR.fit_transform()
print 'Fit PCA in ', time.time() - t_start, 'sec'

t_start = time.time()
IDR.reduced_data_to_json(file_name='tmp_json.JSON',
                         file_path='/home/david/Desktop/')
print 'Dumps JSON in ', time.time() - t_start, 'sec'


t_start = time.time()
IDR.make_thumbnails(
    thumbnail_path='/home/david/Pictures/SAXS_for_DB/thumbnails/',
    thumbnail_size=(75, 75), thumbnail_type='.jpg')
print 'Make thumbnails in ', time.time() - t_start, 'sec'

draw_PCA(X_PCA, 1)
