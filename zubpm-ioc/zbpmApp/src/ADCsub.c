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

#define BUFMAX 500000

static int ADCsub(aSubRecord *precord) {

    static int i,oldready=0,oldwfmLen=0,oldwfmOff=0;

    int ready = *(int *)precord->h;
    int wfmLen = *(int *)precord->e;
    int wfmOff = *(int *)precord->f;

    if((oldready==1 && ready==0) || wfmLen!=oldwfmLen || wfmOff!=oldwfmOff){

        int bufLen = *(int *)precord->g;
//        if(bufLen>BUFMAX){
//            bufLen=BUFMAX;
//        }
        if(wfmLen>10000) wfmLen = 10000;
        if(wfmLen<100) wfmLen = 100;
        if(wfmLen>bufLen) wfmLen = bufLen;
        if(wfmOff<0) wfmOff = 0;
        if(wfmOff>(bufLen-wfmLen)) wfmOff = bufLen - wfmLen;
        oldwfmLen = wfmLen;
        oldwfmOff = wfmOff;
        *(int *)precord->vala = wfmLen;
        *(int *)precord->valb = wfmOff;

        double *Abuff = (double *)precord->a;
        double *Bbuff = (double *)precord->b;
        double *Cbuff = (double *)precord->c;
        double *Dbuff = (double *)precord->d;

        short Awfm[10000],Bwfm[10000],Cwfm[10000],Dwfm[10000];
        float Twfm[10000];

        for(i=wfmOff;i<(wfmLen+wfmOff);i++){
            Awfm[i-wfmOff] = (short)Abuff[i];
            Bwfm[i-wfmOff] = (short)Bbuff[i];
            Cwfm[i-wfmOff] = (short)Cbuff[i];
            Dwfm[i-wfmOff] = (short)Dbuff[i];
            Twfm[i-wfmOff] = (i-wfmOff)*0.008521583;  //Time in microseconds
        }

        precord->nevd = wfmLen;
        precord->neve = wfmLen;
        precord->nevf = wfmLen;
        precord->nevg = wfmLen;
        precord->nevh = wfmLen;
        memcpy((short *)precord->vald,Awfm,wfmLen*sizeof(short));
        memcpy((short *)precord->vale,Bwfm,wfmLen*sizeof(short));
        memcpy((short *)precord->valf,Cwfm,wfmLen*sizeof(short));
        memcpy((short *)precord->valg,Dwfm,wfmLen*sizeof(short));
        memcpy((float *)precord->valh,Twfm,wfmLen*sizeof(float));
//        *(int *)precord->valc = bufLen;
    }
    oldready = ready;
    return(0);
}
// Note the function must be registered at the end!
epicsRegisterFunction(ADCsub);
