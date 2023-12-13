def true_evt_vs_reco_evt_PPS(infile_PPS, hits_dset_name, output_file_path):
    PPS_evts = []
    n_events_PPS = len(infile_PPS['charge/events/data'])
    
    with open(output_file_path, 'w') as output_file:
        for event_number in range(n_events_PPS):
            hit_ref_slice = infile_PPS['charge/events/ref/charge/'+hits_dset_name+'/ref_region'][event_number]
            hits = infile_PPS['charge/'+hits_dset_name+'/data'][hit_ref_slice[0]:hit_ref_slice[1]]
            hits_bt = infile_PPS['mc_truth/'+hits_dset_name[:-1]+'_backtrack/data'][hit_ref_slice[0]:hit_ref_slice[1]]
            segments = infile_PPS['mc_truth/segments/data']
            ts_start = infile_PPS['charge/events/data']['ts_start'][event_number]
            ts_end = infile_PPS['charge/events/data']['ts_end'][event_number]
            #print(event_number, ts_start)
            for hit in hits_bt:
                for cont in range(len(hit['fraction'])):
                    if abs(hit['fraction'][cont]) > 0.0001:
                        seg_id = hit['segment_id'][cont]
                        seg = segments[seg_id]
                        if not seg['segment_id'] == seg_id:
                            print('WARNING: segment id not the same as segment index!')
                        plt.plot([seg['z_start'], seg['z_end']], [seg['x_start'], seg['x_end']], c='r', alpha=0.5)
                        seg_evt_id = seg['event_id']
                        PPS_evts.append([event_number, seg_evt_id, ts_start, ts_end])
            
            output_file.write(f'{event_number}, {seg_evt_id}, {ts_start}, {ts_end}\n')            
            print(f'PPS reco_event {event_number} has truth event {seg_evt_id}, ts_start {ts_start}, and ts_end {ts_end}')
    
    return PPS_evts
