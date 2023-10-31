# piXort
piXort is a simple python application that allows you to sort, shuffle, and generally corrupt images in a stylistic way

## Example
Input                    |  Output
:-----------------------:|:-------------------------:
![](/images/image1.png)  |  ![](/images/image1-sorted.png)
![](/images/image2.png)  |  ![](/images/image2-sorted.png)
![](/images/image3.png)  |  ![](/images/image3-sorted.png)

## How-to
piXort splits an image into segments and performs the sorting operation on each segment.

### Parameters
- **Segments**
  - **Size** - Length of a segment in pixels. Lengths greater than the dimension of the image will process the entire row/column as one segment
  - **Random Size** - Random multiplier for segment size, relative to segment size.
  - **Effect Probability** - Probability of a given segment getting sorted or shuffled.
- **Sorting**
  - **Sort By** - Criteria by which pixels are sorted
    - **Hue** - Sorts pixels by their hue, in degrees
    - **Saturation** - Sorts pixels by their saturation (color intensity)
    - **Luminance** - Sorts pixels by their overall brightness
    - **Red** - Sorts pixels by value of the Red channel
    - **Green** - Sorts pixels by value of the Green channel
    - **Blue** - Sorts pixels by value of the Blue channel   
  - **Sort Direction** - Sort the pixels based on the sorting criteria from low to high or high to low
- **Shuffle** - Shuffles the image segments based on previous parameters.
- **Apply** - Bakes the sorting or shuffling into the image and allows another operation to be performed on top. (Note: this does not save the image to your drive)

![](/images/gui.png)

## To-Do
- Application icon
- Bubble sort
  - Variable iteration count
- Advanced features
  - Repeat sorting
  - Custom sort functions?
- Multiprocessing?