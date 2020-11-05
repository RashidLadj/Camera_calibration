# Camera calibration

### Description
Camera calibration is the process of calculating internal properties of a camera such as focal length, lens distortion coefficients, etc. These properties are intrinsic to the camera, which once estimated, do not change. However, different calibration software (or different tests) may produce slightly different results; these slight variations are due to noise in the imaging system.

In computer / robotic vision, it is always advisable to work with calibrated cameras as this is a one-time process and it makes it a lot easier there. For example, consider the case of estimating rotation (R) and translation (t) between two camera positions. If we don't know K, we will have to estimate F (fundamental matrix) using the point matches and it is not easy to decompose F into R and t because F is made up of K, R and t. On the other hand if you knew K, we can estimate E (essential matrix) and decompose it into R and t because E is only composed of R and t.

In this code, the matrix K is calculated using the widely used Zhang method (Zhang. Z, “A flexible new technique for camera calibration”, PAMI, 2000). This method is based on a planar checkerboard to easily establish 3D-2D correspondences, then solves the planar homographies to factorize the matrix K representing the intrinsic parameters of the camera, as well as the distortion coefficients.

We deal with 3 types of camera: monocular, fisheye (not implemented yet) and stereo [two lens] (not implemented yet)

The estimated K matrix “camera intrinsic parameters” will be of the form shown below:
<p align="center">
  <img src="https://i.ibb.co/RYJRLR8/K-matrix.png" alt="Sublime's custom image"/>
</p>

The subscript pixels means that the estimated quantities are in units of pixels and not in meters (or in any other metric units). For well manufactured (expensive) cameras, fx pixels and fy pixels are generally same. Also, cx pixels and cy pixels are equal to the image center coordinates. But many times we do not use such good cameras and as a result we expect the above statements to be invalid.