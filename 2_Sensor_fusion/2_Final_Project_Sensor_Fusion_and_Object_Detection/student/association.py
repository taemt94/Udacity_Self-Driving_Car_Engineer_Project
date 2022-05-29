# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Data association class with single nearest neighbor association and gating based on Mahalanobis distance
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np
from scipy.stats.distributions import chi2

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import misc.params as params 

class Association:
    '''Data association class with single nearest neighbor association and gating based on Mahalanobis distance'''
    def __init__(self):
        self.association_matrix = np.matrix([])
        self.unassigned_tracks = []
        self.unassigned_meas = []
        
    def associate(self, track_list, meas_list, KF):
             
        ############
        # TODO Step 3: association:
        # - replace association_matrix with the actual association matrix based on Mahalanobis distance (see below) for all tracks and all measurements
        # - update list of unassigned measurements and unassigned tracks
        ############
        
        # the following only works for at most one track and one measurement
        self.association_matrix = np.matrix([]) # reset matrix
        self.unassigned_tracks = [] # reset lists
        self.unassigned_meas = []
        
        N = len(track_list)
        M = len(meas_list)
        if M > 0:
            self.unassigned_meas = list(range(M))
        if N > 0:
            self.unassigned_tracks = list(range(N))
        if M > 0 and N > 0: 
            self.association_matrix = np.matrix(np.inf*np.ones((N, M)))
            
            for n in range(N):
                for m in range(M):
                    track = track_list[n]
                    meas = meas_list[m]
                    
                    mhd = self.MHD(track, meas, KF)
                    if self.gating(mhd, meas.sensor):
                        self.association_matrix[n, m] = mhd
        
        ############
        # END student code
        ############ 
                
    def get_closest_track_and_meas(self):
        ############
        # TODO Step 3: find closest track and measurement:
        # - find minimum entry in association matrix
        # - delete row and column
        # - remove corresponding track and measurement from unassigned_tracks and unassigned_meas
        # - return this track and measurement
        ############

        ## Find minimum entry in association matrix
        track_ind, meas_ind = np.unravel_index(np.argmin(self.association_matrix, axis=None), self.association_matrix.shape) 
        
        ## If no more association was found, return np.nan for the track and measurement
        if self.association_matrix[track_ind, meas_ind] == np.inf:
            return np.nan, np.nan

        ## Delete row and column
        self.association_matrix = np.delete(self.association_matrix, track_ind, axis=0)
        self.association_matrix = np.delete(self.association_matrix, meas_ind, axis=1)

        ## Remove corresponding track and measurement from unassigned_tracks and unassigned_meas
        update_track = self.unassigned_tracks[track_ind]
        update_meas = self.unassigned_meas[meas_ind]

        self.unassigned_tracks.remove(update_track)
        self.unassigned_meas.remove(update_meas)

        ############
        # END student code
        ############
        return update_track, update_meas

    def gating(self, MHD, sensor):
        ############
        # TODO Step 3: return True if measurement lies inside gate, otherwise False
        ############

        p = params.gating_threshold
        df = sensor.dim_meas
        limit = chi2.ppf(p, df)
        if MHD < limit:
            return True
        else:
            return False
        
        ############
        # END student code
        ############

    def MHD(self, track, meas, KF):
        ############
        # TODO Step 3: calculate and return Mahalanobis distance
        ############
        
        z = meas.z
        x = track.x
        h_x = meas.sensor.get_hx(x)
        gamma = z - h_x
        
        H = meas.sensor.get_H(x)
        S = KF.S(track, meas, H)
        
        mhd = gamma.T * np.linalg.inv(S) * gamma
        
        return mhd
        
        ############
        # END student code
        ############ 
    
    def associate_and_update(self, manager, meas_list, KF):
        # associate measurements and tracks
        self.associate(manager.track_list, meas_list, KF)
    
        # update associated tracks with measurements
        while self.association_matrix.shape[0]>0 and self.association_matrix.shape[1]>0:
            
            # search for next association between a track and a measurement
            ind_track, ind_meas = self.get_closest_track_and_meas()
            if np.isnan(ind_track):
                print('---no more associations---')
                break
            track = manager.track_list[ind_track]
            
            # check visibility, only update tracks in fov    
            if not meas_list[0].sensor.in_fov(track.x):
                continue
            
            # Kalman update
            print('update track', track.id, 'with', meas_list[ind_meas].sensor.name, 'measurement', ind_meas)
            KF.update(track, meas_list[ind_meas])
            
            # update score and track state 
            manager.handle_updated_track(track)
            
            # save updated track
            manager.track_list[ind_track] = track
            
        # run track management 
        manager.manage_tracks(self.unassigned_tracks, self.unassigned_meas, meas_list)
        
        for track in manager.track_list:            
            print('track', track.id, 'score =', track.score)