# piXort
piXort is a simple python application that allows you to sort, shuffle, and generally corrupt images in a stylistic way.

## How-to
The fundamental concept behind piXort is that splits an image into segments and then performs the selected operation on each segment individually.

There are two main ways these segments can be generated, either randomly through the **Segment Length** and **Random Length Multiplier** parameters, or by detecting the edges within the image.

Once the segments are generated, they are randomly selected based on the **Effect Probability** value. For example, an effect probability of 60% means that 60% of the segments generated will have the effect applied to them. This allows you to have streaks of sorted or smeared pixels in an otherwise untouched image. These segments are generated independently from the sorting or drifting operation and are governed by the parameters in the **Segments** section of the GUI.

### Parameters
- **Segments**
  - **Edge Detection** - Check if you want to use edge detection instead of random segments. Edge detection generally results in more coherence in the sorted image since it will preserve the edges.
  - **Edge Threshold** - Higher values = more edges, lower values = fewer edges.
  - **Length** - Length of a segment in pixels. Lengths greater than the respective dimension of the image will process the entire row/column as one segment.
  - **Random Length Multiplier** - Random multiplier for segment size, relative to segment size.
  - **Effect Probability** - Probability of a given segment getting affected by sorting or drifting.
  - **Orientation** - Generate segments along the horizontal or vertical axis of the image.
- **Pixel Sorting**
  - **Sort By** - Criteria by which pixels are sorted.
    - **Hue** - Sorts pixels by their hue, in degrees.
    - **Saturation** - Sorts pixels by their saturation (color intensity).
    - **Luminance** - Sorts pixels by their overall brightness. This is a good default choice since our eyes are most sensitive to changes in luminosity.
    - **Red** - Sorts pixels by value of the Red channel.
    - **Green** - Sorts pixels by value of the Green channel.
    - **Blue** - Sorts pixels by value of the Blue channel.
  - **Sort Direction** - Sort the pixels based on the sorting criteria from low to high or high to low.
- **Pixel Drift**
  - **Iterations** - Number of times to iterate through each segment of the image. (Note: a high number of iterations combined with high effect probability will take a *long* time to compute)
  - **Pixel Smear Probability** - Probability of a pixel in the segment swapping with its neighbor. 
- **Preview Sort** - Generates a sorted image preview, to apply the transformation click **Apply**.
- **Preview Drift** - Generates a drifted image preview, to apply the transformation click **Apply**.
- **Apply** - Bakes the sorting or shuffling into the image and allows another operation to be performed on top. (Note: this does not save the image to your drive)

![](/examples/gui.png)

## Example Images
Input                    |  Output
:-----------------------:|:-------------------------:
![](/examples/image1.png)  |  ![](/examples/image1-sorted.png)
![](/examples/image2.png)  |  ![](/examples/image2-sorted.png)
![](/examples/image3.png)  |  ![](/examples/image3-sorted.png)

## To-Do
- Custom edge mask loading
- Bubble sort
  - Variable iteration count
- Advanced features
  - Repeat sorting
  - Custom sort functions?
- Multiprocessing?