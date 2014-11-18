import numpy as np
import os
import skimage.io as skio
from dimension_reducer import DimensionReducer


class ImageDimensionReducer(DimensionReducer):

    """
    This `ImageDimensionReducer` uses takes in a dimensionality reduction
    class from sklearn, and creates a reduced representation of the images.
    """

    def load_images(self, directory_path=None,
                    file_type=None, dataset_name=None):
        '''
        load data from a directory

        Args:
            directory_path: path to directory containing image files.
            file_type: provides an option to specify the type of file to be
                loaded.
            dataset_name: The name of the datasets.
        '''
        if directory_path is None:
            raise RuntimeError("directory_path not specified")
        if file_type is None:
            raise RuntimeError("file_type not specified")
        self._load_images(directory_path, file_type, dataset_name)

    def _load_images(self, directory, file_type, dataset_name=None):
        '''
        Helper function for the funciton load_images.
        '''
        file_names = sorted(os.listdir(directory))
        file_index = 0
        dataset_start_index = self.n_samples
        while not file_names[file_index].endswith(file_type):
            file_index = file_index + 1
        im = skio.imread(os.path.join(directory, file_names[0]))
        raw_data = im[None]
        if self.data is None:
            self.data = raw_data
            final_index = 1
        else:
            self._check_dimensions(raw_data)
            final_index = 0
        self.n_samples_names.append(file_names[file_index][:-4])
        self.n_samples = self.n_samples + 1
        for file_name in file_names[file_index + 1:]:
            if file_name.endswith(file_type):
                im = skio.imread(os.path.join(directory, file_name))
                raw_data = np.concatenate((raw_data, im[None]))
                self.n_samples = self.n_samples + 1
                self.n_samples_names.append(file_name[:-4])
        self.data = np.concatenate((self.data, raw_data[final_index:]))
        if dataset_name is None:
            dataset_name = file_names[0][:-9]
        self.datasets[dataset_name] = slice(dataset_start_index,
                                            self.n_samples)
