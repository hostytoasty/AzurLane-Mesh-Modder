import UnityPy # 1.20.18
from PIL import Image, ImageOps
from pathlib import Path
import struct
import tkinter as tk
from tkinter import filedialog

def get_image_resolution(file_path):
    img = Image.open(file_path)
    width = img.width
    height = img.height

    return width,height

def resize_to_4(image_path):
    """
    Certain image encoding formats in Unity want dimensions of 4 in its images
    """
    # Open the src_image
    img = Image.open(image_path)
    width, height = img.size

    new_width = (width + 3) // 4 * 4
    new_height = (height + 3) // 4 * 4

    # Calculate margins for centering
    left_margin = (new_width - width) // 2
    top_margin = (new_height - height) // 2
    right_margin = new_width - width - left_margin
    bottom_margin = new_height - height - top_margin

    # Create a padded src_image
    padded_img = ImageOps.expand(
        img,
        border=(left_margin, top_margin, right_margin, bottom_margin),
        fill=(0, 0, 0, 0)  # Black padding
    )
    return padded_img

def overwrite_bundle_texture2d(unity_bundle,replace_image,out_bundle=None):
    """
    For replacing texture2d in AL painting.
    
    :param unity_bundle: Path|Str of unitybundle
    :param replace_image: Path|Str of image to replace it with
    :param out_bundle: Path|Str of export unitybundle, default will overwrite
    """
    found = False
    with open(unity_bundle, "rb") as f:
        env = UnityPy.load(f)
        for obj in env.objects:
            if obj.type.name == 'Texture2D':
                found = True
                print('Found texture2d')
                data = obj.read()

                new_texture = replace_image
                data.set_image(new_texture, 4)

                data.save()

    if found:
        # Write changes to a new asset bundle file
        if not out_bundle:
            out_bundle = unity_bundle
        with open(out_bundle, "wb") as new_f:
            new_f.write(env.file.save())
            return True

def overwrite_bundle_mesh(unity_bundle,replace_image,out_bundle=None):
    """
    For replacing obj in AL painting. Will fit to size of replace_image
    
    :param unity_bundle: Path|Str of unitybundle
    :param replace_image: Path|Str of image to replace it with
    :param out_bundle: Path|Str of export unitybundle, default will overwrite
    """

    env = UnityPy.load(unity_bundle)
    data = None
    for obj in env.objects:
        if obj.type.name in ["Mesh"]:
            print('Found Mesh')
            data = obj.read()
            break
    if not data:
        return

    resolution = get_image_resolution(replace_image)
    if not resolution:
        return
    width, height = resolution


    # adjust geometry to an unity plane
    submesh= data.m_SubMeshes[0]
    submesh.indexCount = 6
    submesh.vertexCount = 4

    # 0,1,2 - 2,3,0
    data.m_IndexBuffer = [0, 0, 1, 0, 2, 0, 2, 0, 3, 0, 0, 0]

    # update vertex count
    vertex_data = data.m_VertexData
    vertex_data.m_VertexCount = 4

    # serializes data to something like the following obj format
    # v -height width 0
    # v -0 0 0
    # v -0 width 0
    # v -height 0 0
    binary_data = b''
    binary_data += struct.pack('<fff',0.0, 0.0, 0.0)
    binary_data += struct.pack('<ff',0, 0)
    binary_data += struct.pack('<fff',0.0, height, 0.0)
    binary_data += struct.pack('<ff',0, 1)
    binary_data += struct.pack('<fff',width, height, 0.0)
    binary_data += struct.pack('<ff',1, 1)
    binary_data += struct.pack('<fff',width, 0.0, 0.0)
    binary_data += struct.pack('<ff',1, 0)


    vertex_data.m_DataSize = binary_data
    data.save()

    with open(out_bundle, "wb") as new_f:
        new_f.write(env.file.save(packer="original"))
        return True


def open_file_dialog(asset_dir: Path = None, title = '') -> Path:
    """
    file picker
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir=asset_dir, title=title)
    return Path(file_path)


def mod_bundle():
    ## If you want to enable cli automation
    #bundle_path = input('Enter path of unity bundle:\n')
    #bundle_path = bundle_path.replace('"','')

    ## gui input
    bundle_path = open_file_dialog(title = "Select Unity Bundle File")
    img_path = open_file_dialog(bundle_path.parent, title = "Select painting file")
    out_bundle_path = str(bundle_path)

    bundle_path, img_path, out_bundle_path = str(bundle_path),str(img_path),str(out_bundle_path)
    print(f'Writing out to {out_bundle_path}')
    overwrite_bundle_texture2d(bundle_path,img_path,out_bundle_path)
    overwrite_bundle_mesh(out_bundle_path,img_path,out_bundle_path)


if __name__ == '__main__':
    mod_bundle()

