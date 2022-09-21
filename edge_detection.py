import numpy as np
from PIL import Image, ImageOps
from matplotlib import pyplot as plt

from Stack import Stack

# slow version
def convolve_v1(img, kernel):
	h, w = img.shape
	k = kernel.shape[0] // 2
	kernel_sum = np.sum(kernel)

	def helper(x, y):
		def in_bounds(xx, yy):
			return xx >= 0 and yy >= 0 and xx < h and yy < w
		
		result = [[0 if not in_bounds(x+i, y+j) else img[x+i][y+j] * kernel[i+k][j+k] for j in range(-k, k+1)] for i in range(-k, k+1)]
		return np.sum(result) / kernel_sum

	return [[helper(i, j) for j in range(w)] for i in range(h)]

# less slow version
def convolve(image, kernel):

	h, w = image.shape
	k = kernel.shape[0] // 2
	kernel_sum = np.sum(kernel)
	kernel_sum = kernel_sum if kernel_sum != 0 else 1

	return np.array([[np.sum(np.multiply(image[i-k:i+k+1, j-k:j+k+1], kernel)) / kernel_sum for j in range(k, w-k)] for i in range(k, h-k)])

def blur_image(image, kernel_size=3, sigma=1.0):
	def gaussian_kernel():
		def gaussian(x, y):
			return 1 / (2.0*np.pi*sigma**2) * np.exp(-(x**2 + y**2) / (2.0*sigma**2))
		
		k = int(kernel_size) // 2
		return np.array([[gaussian(i, j) for j in range(-k, k+1)] for i in range(-k, k+1)])

	return convolve(image, gaussian_kernel())

def sobel(image, return_angles=False):

	sobel_x = np.array([
		[-1, 0, 1],
		[-2, 0, 2],
		[-1, 0, 1]
	])

	sobel_y = np.array([
		[ 1,  2,  1],
		[ 0,  0,  0],
		[-1, -2, -1]
	])

	blured_img = blur_image(image)

	res_sobel_x = convolve(blured_img, sobel_x)
	res_sobel_y = convolve(blured_img, sobel_y)
	
	g = np.hypot(res_sobel_x, res_sobel_y)
	g = g / g.max() * 255
	
	if return_angles:
		theta = np.arctan2(res_sobel_y, res_sobel_x)
		return (g, theta)
	else:
		return g

def canny_edge_detection(image, low_threshold=100, high_threshold=150):

	edges, angles = sobel(image, return_angles=True)

	angles = angles * 180. / np.pi
	angles[angles < 0] += 180

	def non_maximum_supression(image, angles):
		h, w = image.shape

		def helper(x, y, theta):
			q = 255
			r = 255

			if 0 <= theta < 22.5 or 157.5 <= theta <= 180:
				q = image[x, y+1]
				r = image[x, y-1]
			elif 22.5 <= theta < 67.5:
				q = image[x+1, y-1]
				r = image[x-1, y+1]
			elif 67.5 <= theta < 112.5:
				q = image[x+1, y]
				r = image[x-1, y]
			elif 112.5 <= theta < 157.5:
				q = image[x-1, y-1]
				r = image[x+1, y+1]
			
			return image[x, y] if image[x, y] >= q and image[x, y] >= r else 0

		return np.array([[helper(i, j, angles[i, j]) for j in range(1, w-1)] for i in range(1, h-1)])

	def threshold_hysteresis(image):
		new_img = np.zeros(image.shape)
		visited = np.zeros(image.shape)

		h, w = image.shape
		dirs = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

		def dfs(x, y):

			stack = Stack()
			stack.push((x, y))

			while not stack.isEmpty():
				
				cx, cy = stack.pop()

				new_img[cx, cy] = 255
				visited[cx, cy] = 255
				
				for d in dirs:
					nx = cx + d[0]
					ny = cy + d[1]
					if nx >= 0 and nx < h and ny >= 0 and ny < w and visited[nx, ny] == 0 and image[nx, ny] >= low_threshold:
						stack.push((nx, ny))
		
		for i in range(h):
			for j in range(w):
				if visited[i, j] == 0 and image[i, j] >= high_threshold:
					dfs(i, j)

		return new_img

	thin_edges = non_maximum_supression(edges, angles)
	threshold = threshold_hysteresis(thin_edges)

	return (thin_edges, threshold)

if __name__ == '__main__':

	# img_name = 'images/flowers.jpeg'
	img_name = 'images/simple_flower.png'

	img = Image.open(img_name)
	img.thumbnail((300, 300))

	img = np.array(img)

	# blured_img = blur_image(img)

	# edges, angles = sobel(img, return_angles=True)

	# img_edges = Image.fromarray(edges).convert('RGB')
	# img_edges.save('sobel.png')

	thin_edges, threshold = canny_edge_detection(img)

	# img_thin_edges = Image.fromarray(thin_edges).convert('RGB')
	# img_thin_edges.save('canny_thin_edges.png')

	# img_threshold = Image.fromarray(threshold).convert('RGB')
	# img_threshold.save('canny_threshold.png')

	plt.imshow(threshold, cmap='gray')
	plt.show()