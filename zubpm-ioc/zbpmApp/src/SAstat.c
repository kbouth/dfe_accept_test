#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stddef.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <stdint.h>
#include <unistd.h>
#include <math.h>
#include <time.h>
#include "cadef.h"
#include <aSubRecord.h>
#include <registryFunction.h>
#include <epicsExport.h>

static int SAstat(aSubRecord *precord) {

    float *Average = (float *)precord->a;
    float *Sigma = (float *)precord->b;

    *(float *)precord->vala = Average[0];
    *(float *)precord->valb = Average[1];
    *(float *)precord->valc = Average[2];
    *(float *)precord->vald = Average[3];
    *(float *)precord->vale = Average[4];
    *(float *)precord->valf = Average[5];
    *(float *)precord->valg = Average[6];
    *(float *)precord->valh = Sigma[0];
    *(float *)precord->vali = Sigma[1];
    *(float *)precord->valj = Sigma[2];
    *(float *)precord->valk = Sigma[3];
    *(float *)precord->vall = Sigma[4];
    *(float *)precord->valm = Sigma[5];
    *(float *)precord->valn = Sigma[6];


    return(0);
}
// Note the function must be registered at the end!
epicsRegisterFunction(SAstat);

