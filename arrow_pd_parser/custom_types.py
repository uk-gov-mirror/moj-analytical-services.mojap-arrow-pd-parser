import numpy as np
from pandas.core.dtypes.dtypes import register_extension_dtype
from pandas.api.extensions import ExtensionDtype
from typing import Type


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