import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from PIL import Image
import torch
from transformers import GLPNImageProcessor, GLPNForDepthEstimation

# Getting models
feature_extractor = GLPNImageProcessor.from_pretrained("vinvino02/glpn-nyu")
model = GLPNForDepthEstimation.from_pretrained("vinvino02/glpn-nyu")

# Loading and resizing the image
image = Image.open("test-image.jpg")
new_height = 480 if image.height > 480 else image.height
new_height -= (new_height % 32)
new_width = int(new_height * image.width / image.height)
diff = new_width % 32

new_width = new_width - diff if diff < 16 else new_width + 32 - diff
new_size = (new_width, new_height)
image.resize(new_size)

# Preparing the image for the model
inputs = feature_extractor(images=image, return_tensors="pt")

#Getting the prediction from the mode
with torch.no_grad():
    outputs = modeL(**inputs)
    predicted_depth = outputs.predicted_depth

# Post-processing
pad = 16
output = predicted_depth.squeeze().cpu().numpy() * 1000.0
output = output[pad:-pad, pad:-pad]
image = image.crop((pad, pad, image.width - pad, image.height - pad))

# visualize the predication
fig, ax = plt.subplots(1, 2)
ax[0].imshow(image)
ax[0].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
ax[1].imshow(output, cmap='plasma')
ax[1].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
plt.tight_layout()
plt.pause(5)
import numpy as np
import open3d as o3d 
width,height = image.size
depth_image = (output * 255/ np.max(output)).astype('unit8')
image = np.array(image)

depth_o3d = o3d.geomety.Image(depth_image)
image_o3d = o3d.geometry.Image(image)
rgbd_image  = o3d.geometry.RGBDImage.create_from_color_and_depth(image_o3d, depth_o3d, convert_rgb_to_intensity=False)
camera_intrinsic = o3d.camera.PinholeCameraIntrnsic()
camera_intrinsic.set_intrinsics(width, height, 500, 500, width/2, height/2)

pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image.camera_intrinsic)
o3d.visualization.draw_geometries([pcd])

cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=20.0)
pcd = pcd.select_by_index(ind)
pcd.estimate_normals()
pcd.orient_normals_to_align_with_direction()
o3d.visualozation.draw_geometries([pcd])

mesh = o3d.geometry.TriangleMesh.creat_from_point_cloud_poisson(pcd,depth=10,n_threads=1)[0]
 
rotation = mesh.get_rotation_matrix_from_xyz((np.pi, 0, 0))
mesh.rotate(rotation, center=(0,0,0))

o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

#mesh_uniform = mesh.paint_uniform_color([0.9,0.8,0.9])
#mesh_uniform.compute_vertex_normals()
#o3d.visualization.draw_geometries([mesh_uniform], mesh_show_back_face = True)
o3d.io.write_triangle_mesh('office.obj',mesh)
