/**********************************************
 * Self-Driving Car Nano-degree - Udacity
 *  Created on: December 11, 2020
 *      Author: Mathilde Badoual
 **********************************************/

#include "pid_controller.h"
#include <vector>
#include <iostream>
#include <math.h>

using namespace std;

PID::PID() {}

PID::~PID() {}

void PID::Init(double Kpi, double Kii, double Kdi, double output_lim_maxi, double output_lim_mini) {
   /**
   * TODO: Initialize PID coefficients (and errors, if needed)
   **/
   this->Kp = Kpi;
   this->Ki = Kii;
   this->Kd = Kdi;

   this->output_lim_max = output_lim_maxi;
   this->output_lim_min = output_lim_mini;
}


void PID::UpdateError(double cte) {
   /**
   * TODO: Update PID errors based on cte.
   **/
   this->p_error = cte;

   if (this->first_flag == true) {
      this->prev_cte = cte;
      this->first_flag = false;
   }
   this->d_error = (cte - this->prev_cte) / this->delta_time;
   this->prev_cte = cte;

   this->i_error += cte * this->delta_time;
}

double PID::TotalError() {
   /**
   * TODO: Calculate and return the total error
    * The code should return a value in the interval [output_lim_mini, output_lim_maxi]
   */
   double control;
    
   control = this->Kp * this->p_error + this->Ki * this->i_error + this->Kd * this->d_error;
   if (control > this->output_lim_max)
      control = this->output_lim_max;
   else if (control < this->output_lim_min)
      control = this->output_lim_min;
   
   return control;
}

double PID::UpdateDeltaTime(double new_delta_time) {
   /**
   * TODO: Update the delta time with new value
   */
   this->delta_time = new_delta_time;
}
