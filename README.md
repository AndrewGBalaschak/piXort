# piXort
piXort is a simple python application that allows you to sort, shuffle, and generally corrupt images in a stylistic way

## Example
Input                    |  Output
:-----------------------:|:-------------------------:
![](/images/image1.png)  |  ![](/images/image1-sorted.png)

## How-to
piXort splits an image into segments and performs the sorting operation on each segment.


### Parameters
- **Segment Size** - Length of a segment in pixels.
- **Segment Random Size** - Random multiplier for segment size, relative to segment size.
- **Segment Sort Probability** - Probability of a given segment getting sorted or shuffled.
- **Sort** - Sorts the image segments based on previous parameters.
- **Shuffle** - Shuffles the image segments based on previous parameters.
- **Apply** - Applies the sorting or shuffling to the image and allows another operation to be performed on top. (Note: this does not save the image to your drive)

## To-Do
- Threaded sorting for faster results
- Bubble sort
  - Variable iteration count
  - Live preview?
- Hue sort
- Advanced features
  - Repeat sorting
  - Custom sort functions?
- Application icon
- Nicer GUI
