import numpy as np
import os
import json
from PIL import Image


class DimensionReducer(object):
    """
    `DimensionReducer` takes in `reducer` and data to perform
    """

    def __init__(self, reducer=None):
        '''
        Create an instance of a DimensionReducer.

        Args:
            reducer: Any class from sklearn that inherts the
                `base.TransformerMixin` class. Some of these include `PCA`
                `RandomizedPCA`, `KernelPCA`, `SparePCA`, `LDA`, `QDA`,
                `LocalLinearEmbedding`, `Isomap`, `MDS`, `SpectralEmbedding`,
                `TSNE`, etc.
        '''
        self.reducer = reducer
        if self.reducer is None:
            raise RuntimeError("Must specify model")
        self.data = None
        self.reduced_data = None
        self.n_samples = 0
        self.n_samples_names = []
        self.datasets = {}

    def load_array(self, X, dataset_name=None):
        '''
        Loads an array as data.

        Args:
            X: array with dimensions (n_samples, n_x, n_y [, n_z])
            dataset_name: name of dataset.
        '''
        index = range(self.n_samples, X.shape[0])
        if dataset_name is None:
            dataset_name = str(len(self.datasets))
        new_name = [dataset_name + str(x) for x in index]
        dataset_start_index = len(self.n_samples)
        if self.data is None:
            self.data = X
        else:
            self._check_dimensions(X)
            self.data = np.concatnate(self.data, X)
        self.n_samples_names = self.n_samples_names + new_name
        self.datasets[dataset_name] = slice(dataset_start_index,
                                            len(self.n_samples_names))

    def _check_dimensions(self, X):
        '''
        Helper function used to check the dimensions of data as they are added.

        Agrs:
            X: new data array.
        '''
        if self.data.shape[1:] != X.shape[:1]:
            raise RuntimeError("Array sizes don't match")

    def _prep_data(self):
        '''
        Helper function that pulls data out of dictionary and into an array.

        Returns:
            dictionary with dataset name as the key and an array with the
            reduced dimension representation of the data as the value.
        '''
        size = self.data[self.data.keys()[0]].shape
        size = (self.n_samples,) + (np.prod(size[1:]),)
        preped_data = np.zeros(size)
        for key, value in self.data.iteritems():
            formated_data = self._format_data(value)
            preped_data[:self.n_samples] = formated_data
        return preped_data

    def _format_data(self, raw_data):
        '''
        Changes the size of the data to meet the format required to do
        dimensionality reduction.

        Agrs:
            raw_data: High dimensional representation of the data in with
            dimensions equal to (n_samples, n_x, n_y[, n_z])

        Returns:
            High dimensional representation of the data with diemsions equal to
            (n_samples, n_features)
        '''
        size = np.array(raw_data.shape)
        new_size = (size[0], np.prod(size[1:]))
        return raw_data.reshape(new_size)

    def fit_transform(self):
        '''
        This function leverages the model's fit_transform function to create a
        low dimension representation of the data.

        Returns: Reduced dimension representation of the raw_data.
        '''
        formated_data = self._format_data(self.data)
        self.reduced_data = self.reducer.fit_transform(formated_data)
        return self.reduced_data

    def clear_data(self):
        '''
        Removes all data from ImageDimensionReducer.
        '''
        self.data = None
        self.reduced_data = None
        self.n_samples = 0
        self.n_samples_names = []

    def reduced_data_to_json(self, file_name=None, file_path=None):
        '''
        Saves reduced data to json file.

        Args:
            file_name: Name of the new JSON file.
            file_path: Path where the new JSON file will be created. This can
               can either be a directory that exists or a new one that will be
               created.
        '''
        if file_name is None:
            raise RuntimeError("file_name not specified")
        if file_path is None:
            raise RuntimeError("file_path not specified")
        if self.data is None:
            raise RuntimeError("No data.")
        if self.reduced_data is None:
            raise RuntimeError("No reduced data.")
        reduced_data_dict = {}
        for key, value in self.datasets.iteritems():
            reduced_data_dict[key] = self.reduced_data[value].tolist()
        print file_name
        with open(os.path.join(file_path, file_name), 'w') as json_file:
            json.dump(reduced_data_dict, json_file)

    def make_thumbnails(self, thumbnail_path=None,
                        thumbnail_size=(200, 200), thumbnail_type='.png'):
        '''
        Creates thumbnails of the images.

        Ags:
            thumbnail_path: path to directory where thumbnails are exported.
            thumbnail_size: size of thumbnails
            thumbnail_type: file type of the thumbnails
        '''
        if thumbnail_path is None:
            raise RuntimeError('thumbnail_path not specified')
        try:
            os.stat(thumbnail_path)
        except:
            os.mkdir(thumbnail_path)
        for index in range(self.n_samples):
            im = Image.fromarray(self.data[index].astype(np.uint8))
            im.save(os.path.join(thumbnail_path,
                    self.n_samples_names[index] + thumbnail_type))
