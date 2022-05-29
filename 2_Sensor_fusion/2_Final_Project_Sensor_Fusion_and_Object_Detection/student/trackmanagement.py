# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Classes for track and track management
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np
import collections

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Track:
    '''Track class with state, covariance, id, score'''
    ### only initialize with lidar measurement
    def __init__(self, meas, id):
        print('creating track no.', id)
        M_rot = meas.sensor.sens_to_veh[0:3, 0:3] # rotation matrix from sensor to vehicle coordinates
        
        ############
        # TODO Step 2: initialization:
        # - replace fixed track initialization values by initialization of x and P based on 
        # unassigned measurement transformed from sensor to vehicle coordinates
        # - initialize track state and track score with appropriate values
        ############
        
        dim_state = params.dim_state
        dim_meas = meas.sensor.dim_meas
        
        self.x = np.matrix(np.zeros((dim_state, 1)))
        x_sens = np.matrix(np.ones((dim_meas+1, 1))) ## homogeneous coordinate
        x_sens[:dim_meas] = meas.z
        x_veh = meas.sensor.sens_to_veh * x_sens
        self.x[:dim_meas] = x_veh[:dim_meas]
        
        self.P = np.matrix(np.zeros((dim_state, dim_state)))
        P_pos = M_rot * meas.R * M_rot.T
        P_vel = np.matrix(np.zeros((dim_meas, dim_meas)))
        P_vel[0, 0] = params.sigma_p44**2
        P_vel[1, 1] = params.sigma_p55**2
        P_vel[2, 2] = params.sigma_p66**2
        self.P[:dim_meas, :dim_meas] = P_pos
        self.P[dim_meas:, dim_meas:] = P_vel
        
        self.state = 'initialized'
        self.score = 1 / params.window
        
        ############
        # END student code
        ############ 
               
        # other track attributes
        self.id = id
        self.width = meas.width
        self.length = meas.length
        self.height = meas.height
        self.yaw =  np.arccos(M_rot[0,0]*np.cos(meas.yaw) + M_rot[0,1]*np.sin(meas.yaw)) # transform rotation from sensor to vehicle coordinates
        self.t = meas.t

    def set_x(self, x):
        self.x = x
        
    def set_P(self, P):
        self.P = P  
        
    def set_t(self, t):
        self.t = t  
        
    def update_attributes(self, meas):
        # use exponential sliding average to estimate dimensions and orientation
        if meas.sensor.name == 'lidar':
            c = params.weight_dim
            self.width = c*meas.width + (1 - c)*self.width
            self.length = c*meas.length + (1 - c)*self.length
            self.height = c*meas.height + (1 - c)*self.height
            M_rot = meas.sensor.sens_to_veh
            self.yaw = np.arccos(M_rot[0,0]*np.cos(meas.yaw) + M_rot[0,1]*np.sin(meas.yaw)) # transform rotation from sensor to vehicle coordinates
        
        
###################        

class Trackmanagement:
    '''Track manager with logic for initializing and deleting objects'''
    def __init__(self):
        self.N = 0 # current number of tracks
        self.track_list = []
        self.last_id = -1
        self.result_list = []
        
    def manage_tracks(self, unassigned_tracks, unassigned_meas, meas_list):  
        ############
        # TODO Step 2: implement track management:
        # - decrease the track score for unassigned tracks
        # - delete tracks if the score is too low or P is too big (check params.py for parameters that might be helpful, but
        # feel free to define your own parameters)
        ############
        
        # decrease score for unassigned tracks
        for i in unassigned_tracks:
            track = self.track_list[i]
            # check visibility    
            if meas_list: # if not empty
                if meas_list[0].sensor.in_fov(track.x):
                    # your code goes here
                    score = track.score
                    window = params.window
                    
                    num_detection = score * window
                    num_detection -= 1  ## Decrease number of detections in last n frames
                    
                    new_score = num_detection / window
                    track.score = new_score
                    self.track_list[i] = track

        # delete old tracks
        delete_threshold = params.delete_threshold
        lower_delete_threshold = 0.1
        max_P = params.max_P
        for track in self.track_list:
            state = track.state
            score = track.score
            P_11 = track.P[0, 0]
            P_22 = track.P[1, 1]
            
            if state == 'confirmed' and (score < delete_threshold or \
                P_11 > max_P or P_22 > max_P):
                self.delete_track(track)
            elif (state == 'tentative' or state == 'initialized') and \
                (score < lower_delete_threshold or P_11 > max_P or P_22 > max_P):
                self.delete_track(track)
                
        ############
        # END student code
        ############ 
            
        # initialize new track with unassigned measurement
        for j in unassigned_meas: 
            if meas_list[j].sensor.name == 'lidar': # only initialize with lidar measurements
                self.init_track(meas_list[j])
            
    def addTrackToList(self, track):
        self.track_list.append(track)
        self.N += 1
        self.last_id = track.id

    def init_track(self, meas):
        track = Track(meas, self.last_id + 1)
        self.addTrackToList(track)

    def delete_track(self, track):
        print('deleting track no.', track.id)
        self.track_list.remove(track)
        
    def handle_updated_track(self, track):      
        ############
        # TODO Step 2: implement track management for updated tracks:
        # - increase track score
        # - set track state to 'tentative' or 'confirmed'
        ############

        confirmed_threshold = params.confirmed_threshold
        tentative_threshold = 0.2
        window = params.window
        
        score = track.score
        num_detection = score * window
        num_detection += 1
        if num_detection < window:
            new_score = num_detection / window
        else:
            new_score = 1.0
        track.score = new_score
        
        if tentative_threshold < new_score < confirmed_threshold:
            track.state = "tentative"
        elif new_score > confirmed_threshold:
            track.state = "confirmed"
        
        ############
        # END student code
        ############ 