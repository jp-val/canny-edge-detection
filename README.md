# canny-edge-detection
Sobel and Canny edge detection from scratch. Featuring a simple convolution algorithm, gaussian blur, non-maximum supression, and threshold hysteresis.

## Examples

<div style="display: flex; flex-direction: row;">
	<img src="images/flowers.jpeg" height="180" style="margin-right: 15px" />
	<img src="images/bearded_dragon.jpg" height="180"/>
<div>
Original Images

<div style="display: flex; flex-direction: row;">
	<img src="images/flowers_sobel.png" height="180" style="margin-right: 15px" />
	<img src="images/bearded_dragon_sobel.png" height="180" />
</div>
Sobel Output

<div style="display: flex; flex-direction: row;">
	<img src="images/flowers_thin_edges.png" height="180" style="margin-right: 15px" />
	<img src="images/bearded_dragon_thin_edges.png" height="180" />
</div>
Canny's Edge Thinning

<div style="display: flex; flex-direction: row;">
	<img src="images/flowers_threshold.png" height="180" style="margin-right: 15px" />
	<img src="images/bearded_dragon_threshold.png" height="180" />
</div>
Canny's Threshold Hysteresis