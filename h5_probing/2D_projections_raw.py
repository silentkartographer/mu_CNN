#plot 2D projections, raw file

import numpy as np
import matplotlib.pyplot as plt
import h5py

# Load the h5 file using h5py
file_path = 'h5_files\mu_500-600MeV_primE.h5'
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
        
        # normalize q
        normalized_q = (q - np.min(q)) / (np.max(q) - np.min(q))
        
        # Create a 3D scatter plot
        fig = plt.figure(figsize=(12, 4))
        
        # Bottom view projection
        ax_top = fig.add_subplot(131)
        ax_top.scatter(x, y, c=normalized_q, cmap = 'viridis')
        ax_top.set_xlabel('X-axis')
        ax_top.set_ylabel('Y-axis')
        ax_top.set_title('XY View (bottom view)')
        
        # Front (side) view projection
        ax_front = fig.add_subplot(132)
        ax_front.scatter(x, z, c=normalized_q, cmap = 'viridis')
        ax_front.set_xlabel('X-axis')
        ax_front.set_ylabel('Z-axis')
        ax_front.set_title('XZ View (a side view)')
        
        # Side view projection
        ax_side = fig.add_subplot(133)
        ax_side.scatter(y, z, c=normalized_q, cmap = 'viridis')
        ax_side.set_xlabel('Y-axis')
        ax_side.set_ylabel('Z-axis')
        ax_side.set_title('ZY View (a side view)')
        
        plt.tight_layout()
        
        # Show the plot
        plt.show()
