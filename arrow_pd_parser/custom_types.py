import numpy as np
import pandas as pd
import numbers
from pandas._typing import ArrayLike
from pandas.core.dtypes.dtypes import register_extension_dtype
from pandas.api.extensions import ExtensionDtype, ExtensionArray
from typing import Type, Union, List, Tuple
from pandas.core.arrays.boolean import BooleanArray, coerce_to_array

""" Needs a corresponding implementation of a boolObjectArray to function fully - as is just returns the same as pd_boolean = True """

@register_extension_dtype
class boolObjectDtype(ExtensionDtype):

    name = "boolObject"

    @property
    def type(self) -> Type[np.object_]:
        return np.object_

    @property
    def kind(self) -> str:
        return "bO"
    
    @property
    def numpy_dtype(self) -> np.dtype:
        return np.dtype("object")

    def __repr__(self) -> str:
        return "boolObjectDtype"

    @property
    def _is_boolean(self) -> bool:
        return True

    @property
    def _is_numeric(self) -> bool:
        return True

    def __from_arrow__(
        self, array: Union["pyarrow.Array", "pyarrow.ChunkedArray"]
    ) -> "BooleanObjectArray":
        """
        Construct BooleanArray from pyarrow Array/ChunkedArray.
        """
        import pyarrow  # noqa: F811

        if isinstance(array, pyarrow.Array):
            chunks = [array]
        else:
            # pyarrow.ChunkedArray
            chunks = array.chunks

        results = []
        for arr in chunks:
            # TODO should optimize this without going through object array
            bool_arr = BooleanArray._from_sequence(np.array(arr))
            results.append(bool_arr)

        return BooleanArray._concat_same_type(results)
