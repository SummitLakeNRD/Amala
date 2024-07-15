# Amala
**Author**: Keane Flynn\
**Contact**: kmflynn24@berkeley.edu\
Program to process drone images from Summit Lake SWUAV survey and identify waterfowl for supervised species classification

## How to Use
1. Log on to the Lambda computer
2. Open Powershell
3. Type the following: `cd Desktop/Amala` and hit enter
4. Type the following: `python amala.py -h`
5. This should return the following information:
   
```
usage: amala.py [-h] imageDir confThresh model

positional arguments:
  imageDir    path/to/image/dir
  confThresh  Confidence threshold value (0-1) for duck detection
  model       path/to/ai/file (ends with .pt)

options:
  -h, --help  show this help message and exit
```

6. You will then give the program the necessary information to process images which will look like the following:
`python amala.py path/to/image/directory/to/process/ 0.25 models/waterbirds.pt`
Note: the only thing you need to change from this set of instructions is the path to images, everything else can remain the same.
7. These images will take a while to process, go do something else.
8. When it's complete, the output Excel file will be ready for the techs to process with the output, labeled images.
