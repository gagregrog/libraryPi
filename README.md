# LibraryPi
Concur Labs Hack Week 8/13/18 - 8/16/18

## What/Why
A doohickey to check out books to people using computer vision and other goodies. Because fun.

## Setup
This project requires OpenCV, which is time consuming and not very straightforward to install. Fortunately, there is a great set of tutorials [here](https://www.pyimagesearch.com/opencv-tutorials-resources-guides/) that show you how to set it up on most platforms. 

Although you could technically run this on any computer with a webcam, it is intended to be used on a Raspberry Pi. If you _are_ running this project on a Pi you can save a lot of pain by following [this walkthrough](https://gist.github.com/RobertMcReed/9173e419322b604cf2490058b3b86e15) to set up the Pi.

Assuming your Pi is setup as shown in the walkthrough linked above, create a new virtual environment and symlink cv into it.

```
mkvirtualenv libraryPi
linkcv libraryPi
```

Note: `linkcv` is a bash function that executes the equivalent of the following command:

```
ln -s /usr/local/lib/python3.5/site-packages/cv2.so ~/.virtualenvs/libraryPi/lib/python3.5/site-packages/cv2.so
```

You may need to adjust the paths slightly on your setup depending on the tides.

Make sure that whenever you are working on this project you are in the virtual environment. You should see the name of the venv to the left of your prompt. If you don't, type `workon libraryPi`.

Install ZBar with `sudo apt-get install libzbar0 -y`

Install the remaining python packages with `pip install -r requirements.txt`

If something breaks, try removing it from requirements.txt and installing again.

## Try It!

Hopefully at this point you have everything needed to get started.

Give it a shot by running `python barcode_scanner.py`

If nothing breaks, a window should pop open showing a live feed from your connected PiCamera. You did remember to connect the camera, didn't you?

Try putting a barcode in front of the camera and see if it works. It should put a box around it and try to find the title of the book.
