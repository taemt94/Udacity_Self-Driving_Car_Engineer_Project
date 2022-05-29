# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        pass

    def F(self):
        ############
        # TODO Step 1: implement and return system matrix F
        ############
        dt = params.dt
        return np.matrix([[1, 0, 0, dt, 0, 0],
                          [0, 1, 0, 0, dt, 0],
                          [0, 0, 1, 0, 0, dt],
                          [0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 1, 0],
                          [0, 0, 0, 0, 0, 1]])
        
        ############
        # END student code
        ############ 

    def Q(self):
        ############
        # TODO Step 1: implement and return process noise covariance Q
        ############
        dt = params.dt
        q = params.q
        dt_3 = dt ** 3
        dt_2 = dt ** 2
        return q * np.matrix([[dt_3 / 3, 0, 0, dt_2 / 2, 0, 0],
                              [0, dt_3 / 3, 0, 0, dt_2 / 2, 0],
                              [0, 0, dt_3 / 3, 0, 0, dt_2 / 2],
                              [dt_2 / 2, 0, 0, dt, 0, 0],
                              [0, dt_2 / 2, 0, 0, dt, 0],
                              [0, 0, dt_2 / 2, 0, 0, dt]])
        
        ############
        # END student code
        ############ 

    def predict(self, track):
        ############
        # TODO Step 1: predict state x and estimation error covariance P to next timestep, save x and P in track
        ############
        F = self.F()
        Q = self.Q()
        
        x_predicted = F * track.x
        P_predicted = F * track.P * F.T + Q
        
        track.set_x(x_predicted)
        track.set_P(P_predicted)
        
        ############
        # END student code
        ############ 

    def update(self, track, meas):
        ############
        # TODO Step 1: update state x and covariance P with associated measurement, save x and P in track
        ############
        gamma = self.gamma(track, meas)

        P = track.P
        H = meas.sensor.get_H(track.x)
        S = self.S(track, meas, H)

        K = P * H.T * np.linalg.inv(S)

        x_updated = track.x + K * gamma
        I = np.matrix(np.identity(params.dim_state))
        P_updated = (I - K * H) * P

        track.set_x(x_updated)
        track.set_P(P_updated)

        ############
        # END student code
        ############
        track.update_attributes(meas)

    def gamma(self, track, meas):
        ############
        # TODO Step 1: calculate and return residual gamma
        ############
        h_x = meas.sensor.get_hx(track.x)
        gamma = meas.z - h_x
        
        return gamma
        
        ############
        # END student code
        ############ 

    def S(self, track, meas, H):
        ############
        # TODO Step 1: calculate and return covariance of residual S
        ############
        R = meas.R
        P = track.P
        S = H * P * H.T + R
        
        return S
        
        ############
        # END student code
        ############ 