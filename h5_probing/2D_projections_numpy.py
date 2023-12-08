import numpy as np
import matplotlib.pyplot as plt
import h5py
import cv2

def find_common_nonzero_region(images, size=224):
    # Get indices of non-zero elements; find where the values in the image are non_zero
    non_zero_indices = [np.argwhere(image > 0) if (image > 0).any() else None for image in images]

    # Check if any image has no non-zero values; # Get the bounding box around non-zero elements
    if any(indices is None for indices in non_zero_indices):
        min_y = min_x = max_y = max_x = 0
    else:
        min_y = min(np.min(indices[:, 0]) for indices in non_zero_indices)
        min_x = min(np.min(indices[:, 1]) for indices in non_zero_indices)
        max_y = max(np.max(indices[:, 0]) for indices in non_zero_indices)
        max_x = max(np.max(indices[:, 1]) for indices in non_zero_indices)

    # Calculate center of the bounding box
    center_x = (max_x + min_x) // 2
    center_y = (max_y + min_y) // 2

    # Calculate the cropping bounds
    start_x = max(0, center_x - size // 2)
    start_y = max(0, center_y - size // 2)
    end_x = min(images[0].shape[1], start_x + size)
    end_y = min(images[0].shape[0], start_y + size)

    return start_x, start_y, end_x, end_y


# Load the h5 file using h5py
file_path = r"C:\Users\hutae\Downloads\mu_500-600MeV_primE.h5"
with h5py.File(file_path, 'r') as file:
    eventid = file['hits']['eventID'][:]

    unique_event_ids = list(set(eventid))

    for event_id in unique_event_ids:
        # select a few events
        if event_id > 20:
            break

        event_indices = eventid == event_id
        x = file['hits']['x'][event_indices]
        y = file['hits']['y'][event_indices]
        z = file['hits']['z'][event_indices]
        q = file['hits']['q'][event_indices]

        # Normalize q
        if (np.max(q) - np.min(q)) == 0:
            normalized_q = (q - np.min(q))
        else:
            normalized_q = (q - np.min(q)) / (np.max(q) - np.min(q))

        # Create a 2D grid for the XY View
        resolution = 50
        x_range_xy = np.linspace(min(x), max(x), resolution) # # generate x axis for xy values, the higher the resolution, the less spacing between the points
        y_range_xy = np.linspace(min(y), max(y), resolution) # # generate y axis for xy values, the higher the resolution, the less spacing between the points
        xx_xy, yy_xy = np.meshgrid(x_range_xy, y_range_xy) # # create a matrix (or a np array) (a grid with x, y coordinates) from the above variables

        # Interpolate normalized_q values for XY View
        image_xy = np.zeros_like(xx_xy)
        for i in range(len(x)):
            # for each x and y coordinate, find the index of the entry in x_range_xy and y_range_xy that has the smallest difference between it and x, y values. Then the value from nnormalized_q is assigned to this x,y position in image_xy
            xi = np.argmin(np.abs(x_range_xy - x[i]))
            yi = np.argmin(np.abs(y_range_xy - y[i]))
            image_xy[yi, xi] = normalized_q[i]

        # repeat for the 2 other views

        # Create a 2D grid for the XZ View
        x_range_xz = np.linspace(min(x), max(x), resolution)
        z_range_xz = np.linspace(min(z), max(z), resolution)
        xx_xz, zz_xz = np.meshgrid(x_range_xz, z_range_xz)

        # Interpolate normalized_q values for XZ View
        image_xz = np.zeros_like(xx_xz)
        for i in range(len(x)):
            xi = np.argmin(np.abs(x_range_xz - x[i]))
            zi = np.argmin(np.abs(z_range_xz - z[i]))
            image_xz[zi, xi] = normalized_q[i]

        # Create a 2D grid for the ZY View
        y_range_zy = np.linspace(min(y), max(y), resolution)
        z_range_zy = np.linspace(min(z), max(z), resolution)
        yy_zy, zz_zy = np.meshgrid(y_range_zy, z_range_zy)

        # Interpolate normalized_q values for ZY View
        image_zy = np.zeros_like(yy_zy)
        for i in range(len(y)):
            yi = np.argmin(np.abs(y_range_zy - y[i]))
            zi = np.argmin(np.abs(z_range_zy - z[i]))
            image_zy[zi, yi] = normalized_q[i]

        cropped_images = [image_xy, image_xz, image_zy]

        # Find the common non-zero region for all cropped images
        start_x, start_y, end_x, end_y = find_common_nonzero_region(cropped_images)

        # # Crop and resize all three views to 224x224, using cv2 so it is "image-like"
        cropped_images_final = []
        for img in cropped_images:
            print(img)
            cropped_img = img[start_y:end_y, start_x:end_x]
            cropped_img_resized = cv2.resize(cropped_img, (224, 224), interpolation=cv2.INTER_AREA)
            cropped_images_final.append(cropped_img_resized)

        # Plotting all three aligned views
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        for i, ax in enumerate(axes):
            ax.imshow(cropped_images_final[i], cmap='viridis')
            ax.set_xlabel('X-axis' if i == 0 else ('Y-axis' if i == 2 else 'Z-axis'))
            ax.set_ylabel('Y-axis' if i == 0 else 'Z-axis')
            ax.set_title(['XY View (bottom view)', 'XZ View (a side view)', 'ZY View (a side view)'][i])

        plt.tight_layout()
        plt.show()
