# Copyright (c) 2014, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

import unittest

from nix import *

class TestDataArray(unittest.TestCase):

    def setUp(self):
        self.file  = File.open("unittest.h5", FileMode.Overwrite)
        self.block = self.file.create_block("test block", "recordingsession")
        self.array = self.block.create_data_array("test array", "signal")
        self.other = self.block.create_data_array("other array", "signal")

    def tearDown(self):
        del self.file.blocks[self.block.id]
        self.file.close()

    def test_data_array_eq(self):
        assert(self.array == self.array)
        assert(not self.array == self.other)
        assert(not self.array == None)

    def test_data_array_id(self):
        assert(self.array.id is not None)

    def test_data_array_name(self):
        def set_none():
            self.array.name = None

        assert(self.array.name is not None)
        self.assertRaises(Exception, set_none)

        self.array.name = "foo array"
        assert(self.array.name == "foo array")

    def test_data_array_type(self):
        def set_none():
            self.array.type = None

        assert(self.array.type is not None)
        self.assertRaises(Exception, set_none)

        self.array.type = "foo type"
        assert(self.array.type == "foo type")

    def test_data_array_definition(self):
        assert(self.array.definition is None)

        self.array.definition = "definition"
        assert(self.array.definition == "definition")

        self.array.definition = None
        assert(self.array.definition is None)

    def test_data_array_timestamps(self):
        created_at = self.array.created_at
        assert(created_at > 0)

        updated_at = self.array.updated_at
        assert(updated_at > 0)

        self.array.force_created_at(1403530068)
        assert(self.array.created_at == 1403530068)

    def test_data_array_label(self):
        assert(self.array.label is None)

        self.array.label = "label"
        assert(self.array.label == "label")

        self.array.label = None
        assert(self.array.label is None)

    def test_data_array_unit(self):
        assert(self.array.unit is None)

        self.array.unit = "mV"
        assert(self.array.unit == "mV")

        self.array.unit = None
        assert(self.array.unit is None)

    def test_data_array_exp_origin(self):
        assert(self.array.expansion_origin is None)

        self.array.expansion_origin = 10.2
        assert(self.array.expansion_origin == 10.2)

        self.array.expansion_origin = None
        assert(self.array.expansion_origin is None)

    def test_data_array_coefficients(self):
        assert(self.array.polynom_coefficients == ())

        self.array.polynom_coefficients = (1.1, 2.2)
        assert(self.array.polynom_coefficients == (1.1, 2.2))

        # TODO delete does not work

    def test_data_array_data(self):
        import numpy as np

        assert(self.array.polynom_coefficients == ())
        assert(not self.array.has_data())
        assert(self.array.data is None)

        data = np.array([float(i) for i in range(100)])
        dout = np.empty_like(data)
        self.array.create_data(data=data)
        assert(self.array.has_data())
        self.array.data.read_direct(dout)
        assert(np.array_equal(data, dout))
        dout = np.array(self.array.data)
        assert(np.array_equal(data, dout))
        assert(self.array.data_extent == data.shape)
        assert(self.array.data_extent == self.array.data.shape)
        self.array.data_extent = (200, )
        assert(self.array.data_extent == (200, ))

        # TODO delete does not work
        data = np.eye(123)
        a1 = self.block.create_data_array("double array", "signal")
        self.assertRaises(ValueError, a1.create_data)
        dset = a1.create_data((123, 123))
        assert(a1.data_extent == (123, 123))
        dset.write_direct(data)
        dout = np.empty_like(data)
        dset.read_direct(dout)
        assert(np.array_equal(data, dout))

        a2 = self.block.create_data_array("identity array", "signal")
        self.assertRaises(ValueError, lambda : a1.create_data(data=data, shape=(1,1)))
        a2.create_data(data=data)
        assert(a2.data_extent == (123, 123))
        dout = np.empty_like(data)
        dset.read_direct(dout)
        assert(np.array_equal(data, dout))

        a3 = self.block.create_data_array("int identity array", "signal")
        a3.create_data(dtype='i4', data=data)
        assert(a3.data_extent == (123, 123))


    def test_data_array_dimensions(self):
        assert(len(self.array.dimensions) == 0)

        setd    = self.array.append_set_dimension()
        ranged  = self.array.append_range_dimension(range(10))
        sampled = self.array.append_sampled_dimension(0.1)

        assert(len(self.array.dimensions) == 3)

        self.assertRaises(TypeError, lambda : self.array.dimensions["notexist"])
        self.assertRaises(KeyError, lambda : self.array.dimensions[-4])
        self.assertRaises(KeyError, lambda : self.array.dimensions[3])

        assert(isinstance(str(self.array.dimensions), basestring))
        assert(isinstance(repr(self.array.dimensions), basestring))

        dims   = list(self.array.dimensions)
        for i in range(3):
            assert(dims[i].index == self.array.dimensions[i].index)
            assert(dims[i].dimension_type == self.array.dimensions[i].dimension_type)

            assert(self.array.dimensions[i].index == self.array.dimensions[i - 3].index)

        del self.array.dimensions[2]
        del self.array.dimensions[1]
        del self.array.dimensions[0]

        assert(len(self.array.dimensions) == 0)

    def test_data_array_sources(self):
        source1 = self.block.create_source("source1", "channel")
        source2 = self.block.create_source("source2", "electrode")

        assert(len(self.array.sources) == 0)

        self.array.sources.append(source1)
        self.array.sources.append(source2)

        self.assertRaises(TypeError, lambda : self.array.sources.append(100))

        assert(len(self.array.sources) == 2)
        assert(source1 in self.array.sources)
        assert(source2 in self.array.sources)

        del self.array.sources[source2]
        assert(self.array.sources[0] == source1)

        del self.array.sources[source1]
        assert(len(self.array.sources) == 0)
