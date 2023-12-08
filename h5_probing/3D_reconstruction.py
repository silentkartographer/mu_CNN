#plot each 3D event

import numpy as np
import matplotlib.pyplot as plt
import h5py

# Load the h5 file using h5py
file_path = r'C:\Users\Hilary\Downloads\mu_500-600MeV_primE.h5'
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
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        # Plotting the points, c is color, marker is the marker used
        scatter = ax.scatter(x, y, z, c=normalized_q, cmap = 'viridis')
        cbar = plt.colorbar(scatter)
        cbar.set_label('Charge Deposition')
        
        # Set labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')
        ax.set_title(f'3D Neutrino Event {event_id}')
        
        # Show the plot
        plt.show()
