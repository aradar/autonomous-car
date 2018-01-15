from pixy import *
from ctypes import *
from ai_robo_car.layer.data_objects import BoundingBox, ObjectType
from ai_robo_car.abstract_layer import AbstractLayer


class Blocks(Structure):
    """
    Represents the objects recognized by the pixy cam. (object structure provided by the pixy cam)
    """
    _fields_ = [("type", c_uint),
                ("signature", c_uint),
                ("x", c_uint),
                ("y", c_uint),
                ("width", c_uint),
                ("height", c_uint),
                ("angle", c_uint)]


blocks_count = 100
blocks = BlockArray(blocks_count)
frame = 0


def normalize_values(value, max_value) -> float:
    """
    Normalizes values. Calculated values are equal to/ greater than 0 and equal to/ smaller than 1.
    :param value: value to be normalized
    :param max_value: max value (not normalized, normalized it would be 1)
    :return: normalized value
    """
    return value / max_value


def create_bounding_box(block: Block) -> BoundingBox:
    """
    Converts block into bounding box. (/Creates bounding box from block.)
    :param block: block provideed by pixy cam, to be converted into bounding box
    :return: created bounding box
    """
    bounding_box = BoundingBox(
        normalize_values(block.x, 320) - normalize_values(block.width, 320) / 2,  # left
        normalize_values(block.x, 320) + normalize_values(block.width, 320) / 2,  # right
        normalize_values(block.y, 200) - normalize_values(block.height, 200) / 2,  # top
        normalize_values(block.y, 200) + normalize_values(block.height, 200) / 2,  # bottom
        normalize_values(block.width, 320),  # width
        normalize_values(block.height, 200),  # height
        ObjectType(block.signature)  # pixy must be configured so that blue is 1 and yellow is 2
    )
    return bounding_box


def is_bounding_box_valid(bounding_box: BoundingBox) -> bool:
    """
    Checks if bounding box is valid. A bounding box is valid, if not all parameters are zero and all parameters are
    greater than zero and smaller than one.
    :param bounding_box: bounding box to be checked
    :return:
            true    if bounding box is valid
            false   if bounding box is not valid
    """
    is_zero = bounding_box.left == 0
    is_zero = is_zero and bounding_box.right == 0
    is_zero = is_zero and bounding_box.width == 0
    is_zero = is_zero and bounding_box.height == 0
    is_zero = is_zero and bounding_box.bottom == 0
    is_zero = is_zero and bounding_box.top == 0
    is_zero = is_zero and bounding_box.object_type == 0

    is_negative = bounding_box.left < 0
    is_negative = is_negative or bounding_box.right < 0
    is_negative = is_negative or bounding_box.width < 0
    is_negative = is_negative or bounding_box.height < 0
    is_negative = is_negative or bounding_box.bottom < 0
    is_negative = is_negative or bounding_box.top < 0

    is_greater_one = bounding_box.left > 1
    is_greater_one = is_greater_one or bounding_box.right > 1
    is_greater_one = is_greater_one or bounding_box.width > 1
    is_greater_one = is_greater_one or bounding_box.height > 1
    is_greater_one = is_greater_one or bounding_box.bottom > 1
    is_greater_one = is_greater_one or bounding_box.top > 1

    return not is_zero and not is_negative and not is_greater_one


class ObjectRecognizer(AbstractLayer[str, str]):
    """
    This layer uses the pixy cam to recognize objects. It produces a list of bounding boxes. Each bounding box
    contains its coordinates, dimensions and object type and represents a recognized object.
    """

    def __init__(self, upper: AbstractLayer, lower: AbstractLayer):
        super().__init__(upper, lower)
        init_value = pixy_init()
        if init_value is not 0:
            print("pixy cam could not be initialized error:", init_value)  # todo remove

    def call_from_upper(self, message: str) -> None:
        bounding_boxes = []
        count = pixy_get_blocks(blocks_count, blocks)
        if count > 0:
            for i in range(count):
                bounding_box = create_bounding_box(blocks[i])
                if is_bounding_box_valid(bounding_box):
                    bounding_boxes.append(bounding_box)

        if len(bounding_boxes) is 0:
            self.call_lower(None)
        else:
            self.call_lower(bounding_boxes)

    def call_from_lower(self, message: str) -> None:
        print("ObjectRecognizer: call_from_lower -> " + message)
        if self.upper is not None:
            self.call_upper(message + str("!"))
