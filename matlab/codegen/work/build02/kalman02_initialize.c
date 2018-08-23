/*
 * File: kalman02_initialize.c
 *
 * MATLAB Coder version            : 4.0
 * C/C++ source code generated on  : 14-Aug-2018 17:45:27
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "kalman02.h"
#include "kalman02_initialize.h"

/* Function Definitions */

/*
 * Arguments    : void
 * Return Type  : void
 */
void kalman02_initialize(void)
{
  rt_InitInfAndNaN(8U);
  kalman02_init();
}

/*
 * File trailer for kalman02_initialize.c
 *
 * [EOF]
 */
