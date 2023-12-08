import numpy as np
import matplotlib.pyplot as plt
import h5py
import cv2

def crop_nonzero_region(image, size=224):
    # Get indices of non-zero elements; find where the values in the image are non_zero
    non_zero_indices = np.argwhere(image > 0)

    if len(non_zero_indices) == 0:
        return None  # Return None if no non-zero elements found

    # Get the bounding box around non-zero elements
    min_y, min_x = np.min(non_zero_indices, axis=0)
    max_y, max_x = np.max(non_zero_indices, axis=0)

    # Calculate center of the bounding box
    center_x = (max_x + min_x) // 2
    center_y = (max_y + min_y) // 2

    # Calculate the cropping bounds
    start_x = max(0, center_x - size // 2)
    start_y = max(0, center_y - size // 2)
    end_x = min(image.shape[1], start_x + size)
    end_y = min(image.shape[0], start_y + size)

    return image[start_y:end_y, start_x:end_x]

# Load the h5 file using h5py
file_path = r"C:\Users\hutae\Downloads\mu_500-600MeV_primE.h5"
with h5py.File(file_path, 'r') as file:
    eventid = file['hits']['eventID'][:]

    unique_event_ids = list(set(eventid))

    for event_id in unique_event_ids:
        # select a few events
        if event_id > 5:
            break

        event_indices = eventid == event_id
        x = file['hits']['x'][event_indices]
        y = file['hits']['y'][event_indices]
        z = file['hits']['z'][event_indices]
        q = file['hits']['q'][event_indices]

        # Normalize q
        normalized_q = (q - np.min(q)) / (np.max(q) - np.min(q))

        # Create a 2D grid for the XY View
        resolution = 50  # we can try different resolutions
        x_range_xy = np.linspace(min(x), max(x), resolution) # generate x axis for xy values, the higher the resolution, the less spacing between the points
        y_range_xy = np.linspace(min(y), max(y), resolution) # generate y axis for xy values, the higher the resolution, the less spacing between the points
        xx_xy, yy_xy = np.meshgrid(x_range_xy, y_range_xy) # create a matrix (or a np array) (a grid with x, y coordinates) from the above variables

        # Interpolate normalized_q values for XY View
        image_xy = np.zeros_like(xx_xy) # create a np array of zeros that match xx_yy
        for i in range(len(x)):
            # for each x and y coordinate, find the index of the entry in x_range_xy and y_range_xy that has the smallest difference between it and x, y values. Then the value from nnormalized_q is assigned to this x,y position in image_xy
            xi = np.argmin(np.abs(x_range_xy - x[i]))
            yi = np.argmin(np.abs(y_range_xy - y[i]))
            image_xy[yi, xi] = normalized_q[i]

        # crop to a none-zero region as defined above
        cropped_xy = crop_nonzero_region(image_xy)

        # repeat for other views

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

        cropped_xz = crop_nonzero_region(image_xz)

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

        cropped_zy = crop_nonzero_region(image_zy)

        # Crop and resize all three views to 224x224, using cv2 so it is "image-like"
        cropped_images = []
        for img in [cropped_xy, cropped_xz, cropped_zy]:
            if img is not None:
                cropped_img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
                cropped_images.append(cropped_img)
            else:
                # If the view has no non-zero pixels, append a blank image
                cropped_images.append(np.zeros((224, 224)))

        # Plotting all three views
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        axes[0].imshow(cropped_images[0], cmap='viridis')
        axes[0].set_xlabel('X-axis')
        axes[0].set_ylabel('Y-axis')
        axes[0].set_title('XY View (bottom view)')

        axes[1].imshow(cropped_images[1], cmap='viridis')
        axes[1].set_xlabel('X-axis')
        axes[1].set_ylabel('Z-axis')
        axes[1].set_title('XZ View (a side view)')

        axes[2].imshow(cropped_images[2], cmap='viridis')
        axes[2].set_xlabel('Y-axis')
        axes[2].set_ylabel('Z-axis')
        axes[2].set_title('ZY View (a side view)')

        plt.tight_layout()
        plt.show()
