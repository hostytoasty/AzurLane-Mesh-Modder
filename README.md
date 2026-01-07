# Azur Lane Mesh Modder
Python script to create modded bundle from image

Before you start
Dependencies can be installed using pip install -r requirements.txt.

EXPECTED INPUTS
1. A valid AL painting, unitybundle should have a texture2d, and a mesh
2. Valid picture, will replace texture2d and provide dimensions for mesh

HOW TO USE
After installing dependencies execute the script. A file dialog will appear, you can point it to your AL painting assetbundle file of choice.

Afterwards, it'll ask you for an image. Pass it your modded image, the script will then automatically create a plane mesh of the corresponding dimensions within the bundle and save/overwrite it.


AUTHOR'S NOTES
This script was cobbled together from analyzing the results of an AL modding exe that is passed around chinese groups and by reversing the results. Logic for adjusting the mesh info was created through consulting LLM's and thus I'm not entirely sure why it works. I wouldn't be surprised if there are simpler ways of accomplishing it within Unitypy, but for now it does its job.

Do note that a ship's painting file's dimensions affects its placement in game. If the dimensions of your image is not correct, the image will be slightly offset causing issues with the paintingface. Different AL descramblers have varying exported dimensions for their images and I'm not sure if there's any sure-fire way of having your image match the in-game's algorithm of recreating the image.



DISCLAIMER
These are tools that I have made for myself as a hobby for modding. There are no guarantees of upkeep for these scripts/tools. You are heavily encouraged to fork/edit these scripts to your own preferences. 
