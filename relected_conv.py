def mirrored_convolve(image: list,
                      image_height: int,
                      image_width: int,
                      kernel: list,
                      kernel_height: int,
                      kernel_width: int):
    """
    create mirrored padded image and performs dot product with kernel
    Returns : 
        output(list) : reflected convolved image 
    """
    
    image_matrix = create_matrix(image,image_height,image_width)
    padded_mirrored_image = mirrored_image(image_matrix,image_height,image_width,kernel_height)
    padding_height, padding_width = kernel_height-1, kernel_width-1
    sliced_image, output_height, output_width = slice_padded_mirrored_image(padded_mirrored_image, 
                                            padding_height, padding_width, image_height, image_width)
    output = []
    for i in range(image_height): 
       for j in range(image_width):                                             
            single_slice_image = part_slice(sliced_image, kernel_width,i, j)
            single_slice_image = convert_matrix_list(single_slice_image)
            output.append(dot_product(single_slice_image, kernel, kernel_height, kernel_width,
                                 image_height, image_width))
    return output


def convert_matrix_list(image: list):
    """
    Convert 2D matrix to list
    """
    list1 = []

    for i in range(len(image)):
        list1.extend(image[i])
    return list1


def dot_product(image: list, kernel: list,
                kernel_height: int, kernel_width: int,
                image_height: int, image_width: int):
    """
    Convolute image and kernel
    """
    return sum(x*y for x,y in zip(image,kernel))
    
def part_slice(sliced_image: list, kernel_width:int,
                 i: int, j: int):
    """
    Slice the padded image in the size of kernel to perform dot product
    Return:
       single_slice_image(list) : list of size kernel_width x kernel_width
    """

    single_slice_image = []
    for col in range(i, i+kernel_width):
        single_slice_image.append(sliced_image[col][j:j+kernel_width])
    return single_slice_image

    
def slice_padded_mirrored_image(image: list, padding_height: int, 
                padding_width: int, image_height: int,
                image_width: int):
        """
        Slice out the padded image of the output size 
        output_size = image_height/image_width + padding_height/padding_width
        Returns:
        sliced_image(list) : list of size output_size x output_size
        """

        output_height = image_height + padding_height
        output_width = image_width + padding_width
        
        padding_row = int(padding_height / 2)
        padding_column = int(padding_width / 2)
        x1,y1 = image_height, image_width
        x2,y2 = (2*image_width)-1, (2*image_width)-1

        x1,y1 = (x1-(padding_row)) , (y1-(padding_column)) 
        

        sliced_image = []
        for i in range(x1, x1+output_height):
            sliced_image.append(image[i][y1:y1+output_width])

        return sliced_image, output_height, output_width
        
def create_matrix(image: list,
                image_height: int,
                image_width: int):
        """
        Convert list to 2D matrix
        """
        image_matrix = []               
        start = 0
        end = image_width
        for i in range(image_height): 
            image_matrix.append(image[start:end])
            start += image_width
            end += image_width
        return image_matrix
    
def mirrored_image(image_matrix: list,
                    image_height: int,
                    image_width: int,
                    kernel_height: int):
    """
    Forms mirrored image by reflecting the x axis and y axis 
    Returns :
        mirrored_image(list): 3ximage_height, 3ximage_width
    """
    xaxis_mirrored_image = reflect_xaxis_image(image_matrix,image_height,image_width)
    yaxis_mirrored_image = reflect_yaxis_image(image_matrix,image_height,image_width)
    
    #TODO make it infinite rather than repeat 3
    mid_row = (3 % 2)
    mirrored_image = []
    inter_list = []

    odd_row = list(range(1,3,2))
    even_row = list(range(0,3,2))

    if mid_row in odd_row:
        image_row = odd_row
        reflect_row = even_row
    else:
        image_row = even_row
        reflect_row = odd_row
    inter_value = 0 
    
    for i in range((3*image_height)):
        if int(i / image_height) in image_row:
           row = 'xaxisrow'
           
        else:
            row = 'yaxisrow'

        if inter_value > (image_height-1): 
                inter_value = 0    
        
        for j in range(3):
            if j == mid_row and row == 'xaxisrow':
               inter_list.extend(xaxis_mirrored_image[inter_value][::-1])
            elif row == 'xaxisrow':
                inter_list.extend(xaxis_mirrored_image[inter_value])
            
            if j == mid_row and row == 'yaxisrow':
               inter_list.extend(yaxis_mirrored_image[inter_value]) 
            elif row == 'yaxisrow':
                inter_list.extend(yaxis_mirrored_image[inter_value][::-1])
        
        mirrored_image.append(inter_list)
        inter_list = []
        inter_value += 1
    return mirrored_image

def reflect_xaxis_image(image_matrix: list,
                    image_height: int,
                    image_width: int):
        "Function that reflects the image horizontally along x axis"
        
        xaxis_mirrored_image = []
        for i in range(image_height):
            xaxis_mirrored_image.append(image_matrix[i][::-1])
        return xaxis_mirrored_image

def reflect_yaxis_image(image_matrix: list,
                    image_height: int,
                    image_width: int):
        "Function that reflects the image vertically along y axis"
        yaxis_mirrored_image = []
        for i in reversed(range(image_height)):
            yaxis_mirrored_image.append(image_matrix[i])
        return yaxis_mirrored_image

###########################################################
# Test cases
# Feel free to add more test cases here as you see fit
# The image from the example PDF
image = [11, 12, 13, 14, 15,
         21, 22, 23, 24, 25,
         31, 32, 33, 34, 35,
         41, 42, 43, 44, 45,
         51, 52, 53, 54, 55]
# The small kernel, like in the example, has values from 1 to 9
small_kernel = [*range(1, 10)]
# The big kernel is a 5 x 7 kernel with values from 1 to 35
big_kernel = [*range(1, 36)]


# Two lists are equal if they have the same length, and the aboslute difference
# of all their values is less than 1e-7
def are_equal(left: list, right: list):
    return len(left) == len(right) and all([abs(l - r) < 1e-7 for l, r in zip(left, right)])


# The example from the problem statement.
def test_conv_example():
    assert are_equal(mirrored_convolve(image, 5, 5, small_kernel, 3, 3),
                     [753, 786, 831, 876, 903,
                      1143, 1176, 1221, 1266, 1293,
                      1593, 1626, 1671, 1716, 1743,
                      2043, 2076, 2121, 2166, 2193,
                      2253, 2286, 2331, 2376, 2403])


# The inverse of the example - the kernel is now the image and the image is
# now the kernel. Notice how the "kernel" can be bigger than the image!
def test_conv_inverse():
    assert are_equal(mirrored_convolve(small_kernel, 3, 3, image, 5, 5),
                     [3930, 4110, 4260,
                      4875, 5055, 5205,
                      4920, 5100, 5250])
	

if __name__ == "__main__":
    test_conv_example()
    test_conv_inverse()
    
    #TODO check code for non square kernels