# =============================================================
# Import the libraries
# =============================================================
import numpy as np  # array operations
from PySide2.QtGui import QImage
import cv2


# =============================================================
# class RawImageParams:

#   Helps set up necessary information/metadata of the image
# =============================================================
class RawImageParams():
    def __init__(self):
        self.channel_gain = (1.0, 1.0, 1.0, 1.0)
        self.awb_gain = (1., 1., 1.)
        self.black_level = (0, 0, 0, 0)
        self.white_level = (1, 1, 1, 1)
        self.color_matrix = [[1., .0, .0],
                             [.0, 1., .0],
                             [.0, .0, 1.]]  # xyz2cam
        self.is_load_image = False
        self.img_show_index = 0
        self.error_str = ""
        self.height = 0
        self.width = 0
        self.bit_depth = 0
        self.raw_format = "MIPI"
        self.pattern = "rggb"
        self.__neighborhood_size_for_bad_pixel_correction = 3
        self.__demosaic_func_type = 0
        self.__demosaic_need_proc_color = 0
        self.__demosaic_need_media_filter = 0
        self.__gamma_ratio = 2.2
        # gamma 查找表的长度
        self.gamma_table_size = 512

    def set_demosaic_func_type(self, type):
        """
        demosaic有两种算法，设置demosaic的算法
        0: Malvar-He-Cutler algorithm
        1: directionally weighted gradient based interpolation algorithm
        """
        self.__demosaic_func_type = type

    def get_demosaic_funct_type(self):
        return self.__demosaic_func_type

    def set_demosaic_need_proc_color(self, value):
        """
        是否在demosaic之后启用色度抑制
        """
        self.__demosaic_need_proc_color = value

    def get_demosaic_need_proc_color(self):
        return self.__demosaic_need_proc_color

    def set_demosaic_need_media_filter(self, value):
        """
        是否在demosaic之后启用中值滤波
        """
        self.__demosaic_need_media_filter = value

    def get_demosaic_need_media_filter(self):
        return self.__demosaic_need_media_filter

    def set_channel_gain(self, channel_gain):
        """
        设置raw图上RGGB每个通道的增益
        """
        self.channel_gain = channel_gain

    def get_channel_gain(self):
        return self.channel_gain

    def set_size_for_bad_pixel_correction(self, value):
        """
        设置bad pixel correction的检测核大小
        默认值为3，代表在3x3的范围内检测，这个范围内如果超过两个坏点则不生效
        """
        self.__neighborhood_size_for_bad_pixel_correction = value

    def get_size_for_bad_pixel_correction(self):
        return self.__neighborhood_size_for_bad_pixel_correction

    def set_color_matrix(self, color_matrix):
        """
        设置CCM 3x3
        """
        self.color_matrix = color_matrix

    def get_color_matrix(self):
        return self.color_matrix

    def set_black_level(self, black_level):
        self.black_level = np.array(black_level)

    def get_black_level(self):
        return self.black_level

    def set_awb_gain(self, awb_gain):
        """
        设置AWB的增益 1x3
        """
        self.awb_gain = awb_gain

    def get_awb_gain(self):
        return self.awb_gain

    def set_gamma(self, gamma_ratio):
        """
        设置gamma的值
        """
        self.__gamma_ratio = gamma_ratio

    def get_gamma_ratio(self):
        return self.__gamma_ratio

    def set_error_str(self, string):
        self.error_str = string

    def get_error_str(self):
        return self.error_str

    def set_width(self, width):
        self.width = width

    def get_width(self):
        return self.width

    def set_height(self, height):
        self.height = height

    def get_height(self):
        return self.height

    def set_bit_depth(self, bit_depth):
        self.bit_depth = bit_depth

    def get_bit_depth(self):
        return self.bit_depth

    def set_raw_format(self, raw_format):
        self.raw_format = raw_format

    def get_raw_format(self):
        return self.raw_format

    def set_pattern(self, pattern):
        self.pattern = pattern

    def get_pattern(self):
        return self.pattern

# =============================================================
# class RawImageInfo:

#   raw image info RAW图自身的属性
# =============================================================


class RawImageInfo():
    def __init__(self):
        self.data = None
        self.show_data = None  # 用来显示图像
        self.__color_space = "raw"
        self.__bayer_pattern = "rggb"
        self.__raw_bit_depth = 12
        # 默认以14位进行处理
        self.__bit_depth = 14
        self.__size = [0, 0]

    def load_image(self, filename, height, width, bit_depth):
        """
        function: 加载图像
        input: 图像宽高和位深
        brief: 由于RAW图不同的bit深度，同样的ISP流程会导致出来的亮度不一样
        所以在RawImageInfor将原始raw图统一对齐为14bit
        """
        if(height > 0 and width > 0):
            self.data = np.fromfile(
                filename, dtype="uint16", sep="").reshape((height, width))

        if (self.data is not None):
            self.name = filename.split('/')[-1]
            self.__size = np.shape(self.data)
            self.__raw_bit_depth = bit_depth
            if (bit_depth < 14):
                self.data = np.left_shift(self.data, 14-bit_depth)

    def create_image(self, name, shape):
        """
        function: 创建一个空图像
        input: 图像名称和shape
        """
        self.data = np.zeros(shape, dtype="uint16")
        if (len(shape) == 2):
            self.__color_space = "raw"
        elif (len(shape) == 3):
            self.__color_space = "RGB"

        if (self.data is not None):
            self.name = name
            self.__size = np.shape(self.data)

    def save_image(self, filename):
        # cv2.imwrite(filename, self.nowImage)
        # 解决中文路径的问题
        cv2.imencode('.jpg', self.show_data)[1].tofile(filename)

    def get_raw_data(self):
        return self.data

    def get_qimage(self):
        """
        function: convert to QImage
        brief: 把图像转换为QImage，用于显示
        """
        if (self.__color_space == "raw"):
            self.show_data = self.convert_bayer2color()
        elif (self.__color_space == "RGB"):
            self.show_data = self.convert_to_8bit()

        if(self.show_data is not None):
            return QImage(self.show_data, self.show_data.shape[1],
                          self.show_data.shape[0], QImage.Format_BGR888)
        else:
            return None

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_size(self, size):
        self.__size = size

    def get_size(self):
        return self.__size

    def get_width(self):
        return self.__size[1]

    def get_height(self):
        return self.__size[0]

    def get_depth(self):
        if np.ndim(self.data) > 2:
            return self.__size[2]
        else:
            return 0

    def set_color_space(self, color_space):
        self.__color_space = color_space

    def get_color_space(self):
        return self.__color_space

    def set_bayer_pattern(self, bayer_pattern):
        self.__bayer_pattern = bayer_pattern

    def get_bayer_pattern(self):
        return self.__bayer_pattern

    def set_bit_depth(self, bit_depth):
        self.__bit_depth = bit_depth

    def get_bit_depth(self):
        """
        获取当前raw图的位深
        """
        return self.__bit_depth

    def get_raw_bit_depth(self):
        """
        获取原始输入raw图的位深
        """
        return self.__raw_bit_depth

    def get_img_point(self, x, y):
        """
        获取图像中一个点的亮度值，注意颜色顺序是BGR
        如果是raw图，获取的就是当前颜色的亮度
        如果是RGB，获取的就是BGR
        如果是YUV，获取的就是YCRCB
        """
        if(x > 0 and x < self.get_width() and y > 0 and y < self.get_height()):
            right_shift_num = self.__bit_depth - self.__raw_bit_depth
            return np.right_shift(self.data[y, x], right_shift_num)
        else:
            return None

    def get_img_point_pattern(self, x, y):
        return self.__bayer_pattern[(x % 2) * 2 + y % 2]

    def bayer_channel_separation(self):
        """
        function: bayer_channel_separation
        Output: R, G1, G2, B (Quarter resolution images)
        """
        if (self.__bayer_pattern == "rggb"):
            R = self.data[::2, ::2]
            Gr = self.data[::2, 1::2]
            Gb = self.data[1::2, ::2]
            B = self.data[1::2, 1::2]
        elif (self.__bayer_pattern == "grbg"):
            Gr = self.data[::2, ::2]
            R = self.data[::2, 1::2]
            B = self.data[1::2, ::2]
            Gb = self.data[1::2, 1::2]
        elif (self.__bayer_pattern == "gbrg"):
            Gb = self.data[::2, ::2]
            B = self.data[::2, 1::2]
            R = self.data[1::2, ::2]
            Gr = self.data[1::2, 1::2]
        elif (self.__bayer_pattern == "bggr"):
            B = self.data[::2, ::2]
            Gb = self.data[::2, 1::2]
            Gr = self.data[1::2, ::2]
            R = self.data[1::2, 1::2]
        else:
            print("pattern must be one of these: rggb, grbg, gbrg, bggr")
            return

        return R, Gr, Gb, B

    def shuffle_bayer_pattern(self, pattern):
        """
        function: bayer_channel_integration
        brief: convert bayer pattern
        """
        R, Gr, Gb, B = self.bayer_channel_separation()
        data = np.zeros_like(self.data)
        if (pattern == "rggb"):
            data[::2, ::2] = R
            data[::2, 1::2] = Gr
            data[1::2, ::2] = Gb
            data[1::2, 1::2] = B
        elif (pattern == "grbg"):
            data[::2, ::2] = Gr
            data[::2, 1::2] = R
            data[1::2, ::2] = B
            data[1::2, 1::2] = Gb
        elif (pattern == "gbrg"):
            data[::2, ::2] = Gb
            data[::2, 1::2] = B
            data[1::2, ::2] = R
            data[1::2, 1::2] = Gr
        elif (pattern == "bggr"):
            data[::2, ::2] = B
            data[::2, 1::2] = Gb
            data[1::2, ::2] = Gr
            data[1::2, 1::2] = R
        else:
            print("pattern must be one of these: rggb, grbg, gbrg, bggr")
            return

        return data

    def convert_bayer2color(self):
        """
        function: convert bayer to color
        brief: 将bayer用8位的rgb显示，不进行demosaic
        """
        data = np.zeros(
            (self.get_height(), self.get_width(), 3), dtype="uint8")
        right_shift_num = self.get_bit_depth() - 8
        if (self.__bayer_pattern == "rggb"):
            data[::2, ::2, 2] = np.right_shift(
                self.data[::2, ::2], right_shift_num)
            data[::2, 1::2, 1] = np.right_shift(
                self.data[::2, 1::2], right_shift_num)
            data[1::2, ::2, 1] = np.right_shift(
                self.data[1::2, ::2], right_shift_num)
            data[1::2, 1::2, 0] = np.right_shift(
                self.data[1::2, 1::2], right_shift_num)
        elif (self.__bayer_pattern == "grbg"):
            data[::2, ::2, 1] = np.right_shift(
                self.data[::2, ::2], right_shift_num)
            data[::2, 1::2, 2] = np.right_shift(
                self.data[::2, 1::2], right_shift_num)
            data[1::2, ::2, 0] = np.right_shift(
                self.data[1::2, ::2], right_shift_num)
            data[1::2, 1::2, 1] = np.right_shift(
                self.data[1::2, 1::2], right_shift_num)
        elif (self.__bayer_pattern == "gbrg"):
            data[::2, ::2, 1] = np.right_shift(
                self.data[::2, ::2], right_shift_num)
            data[::2, 1::2, 0] = np.right_shift(
                self.data[::2, 1::2], right_shift_num)
            data[1::2, ::2, 2] = np.right_shift(
                self.data[1::2, ::2], right_shift_num)
            data[1::2, 1::2, 1] = np.right_shift(
                self.data[1::2, 1::2], right_shift_num)
        elif (self.__bayer_pattern == "bggr"):
            data[::2, ::2, 0] = np.right_shift(
                self.data[::2, ::2], right_shift_num)
            data[::2, 1::2, 1] = np.right_shift(
                self.data[::2, 1::2], right_shift_num)
            data[1::2, ::2, 1] = np.right_shift(
                self.data[1::2, ::2], right_shift_num)
            data[1::2, 1::2, 2] = np.right_shift(
                self.data[1::2, 1::2], right_shift_num)
        else:
            print("pattern must be one of these: rggb, grbg, gbrg, bggr")
            return None
        return data

    def convert_to_8bit(self):
        data = np.zeros(
            (self.get_height(), self.get_width(), 3), dtype="uint8")
        right_shift_num = self.get_bit_depth() - 8
        data[:, :, 0] = np.right_shift(self.data[:, :, 0], right_shift_num)
        data[:, :, 1] = np.right_shift(self.data[:, :, 1], right_shift_num)
        data[:, :, 2] = np.right_shift(self.data[:, :, 2], right_shift_num)
        return data

    def bilinear_interpolation(self, x, y):
        """
        function: 双线性差值
        brief: x,y为float型，输出坐标(x,y)的值
        """

        width, height = self.__size[0], self.__size[1]

        x0 = np.floor(x).astype(int)
        x1 = x0 + 1
        y0 = np.floor(y).astype(int)
        y1 = y0 + 1

        x0 = np.clip(x0, 0, width-1)
        x1 = np.clip(x1, 0, width-1)
        y0 = np.clip(y0, 0, height-1)
        y1 = np.clip(y1, 0, height-1)

        Ia = self.data[y0, x0]
        Ib = self.data[y1, x0]
        Ic = self.data[y0, x1]
        Id = self.data[y1, x1]

        x = np.clip(x, 0, width-1)
        y = np.clip(y, 0, height-1)

        wa = (x1 - x) * (y1 - y)
        wb = (x1 - x) * (y - y0)
        wc = (x - x0) * (y1 - y)
        wd = (x - x0) * (y - y0)

        return wa * Ia + wb * Ib + wc * Ic + wd * Id
