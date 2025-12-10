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

#define BUFMAX 100000
#define SCALE 512.7435

static int TBTsub(aSubRecord *precord) {

    static int i,oldready=0,oldwfmLen=0,oldwfmOff=0;
    float Avg[10],Sig[10];

    int ready = *(int *)precord->k;
    int wfmLen = *(int *)precord->h;
    int wfmOff = *(int *)precord->i;

    if((oldready==1 && ready==0) || oldwfmLen!=wfmLen || oldwfmOff!=wfmOff){
        int bufLen = *(int *)precord->j;

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
        double *Sbuff = (double *)precord->e;
        double *Xbuff = (double *)precord->f;
        double *Ybuff = (double *)precord->g;

        float Awfm[10000],Bwfm[10000],Cwfm[10000],Dwfm[10000];
        float Swfm[10000],Xwfm[10000],Ywfm[10000],Twfm[10000];
        double Asum=0,Bsum=0,Csum=0,Dsum=0,Ssum=0,Xsum=0,Ysum=0;

        for(i=wfmOff;i<(wfmLen+wfmOff);i++){
            Awfm[i-wfmOff] = Abuff[i]/SCALE;
            Asum = Asum + Abuff[i]/SCALE;
            Bwfm[i-wfmOff] = Bbuff[i]/SCALE;
            Bsum = Bsum + Bbuff[i]/SCALE;
            Cwfm[i-wfmOff] = Cbuff[i]/SCALE;
            Csum = Csum + Cbuff[i]/SCALE;
            Dwfm[i-wfmOff] = Dbuff[i]/SCALE;
            Dsum = Dsum + Dbuff[i]/SCALE;
            Swfm[i-wfmOff] = Sbuff[i]/SCALE;
            Ssum = Ssum + Sbuff[i]/SCALE;
            Xwfm[i-wfmOff] = Xbuff[i]/1000.0;      //X in microns
            Xsum = Xsum + Xbuff[i]/1000.0;
            Ywfm[i-wfmOff] = Ybuff[i]/1000.0;      //Y in microns
            Ysum = Ysum + Ybuff[i]/1000.0;
            Twfm[i-wfmOff] = (i-wfmOff)*0.002642;  //Time in milliseconds
        }

        Avg[0] = Asum/wfmLen;
        Avg[1] = Bsum/wfmLen;
        Avg[2] = Csum/wfmLen;
        Avg[3] = Dsum/wfmLen;
        Avg[4] = Ssum/wfmLen;
        Avg[5] = Xsum/wfmLen;
        Avg[6] = Ysum/wfmLen;

        Asum = 0;
        Bsum = 0;
        Csum = 0;
        Dsum = 0;
        Ssum = 0;
        Xsum = 0;
        Ysum = 0;
        for(i=0;i<wfmLen;i++){
            Asum = Asum + (Awfm[i]-Avg[0])*(Awfm[i]-Avg[0]);
            Bsum = Bsum + (Bwfm[i]-Avg[1])*(Bwfm[i]-Avg[1]);
            Csum = Csum + (Cwfm[i]-Avg[2])*(Cwfm[i]-Avg[2]);
            Dsum = Dsum + (Dwfm[i]-Avg[3])*(Dwfm[i]-Avg[3]);
            Ssum = Ssum + (Swfm[i]-Avg[4])*(Swfm[i]-Avg[4]);
            Xsum = Xsum + (Xwfm[i]-Avg[5])*(Xwfm[i]-Avg[5]);
            Ysum = Ysum + (Ywfm[i]-Avg[6])*(Ywfm[i]-Avg[6]);
        }
        Sig[0] = sqrt(Asum/wfmLen);
        Sig[1] = sqrt(Bsum/wfmLen);
        Sig[2] = sqrt(Csum/wfmLen);
        Sig[3] = sqrt(Dsum/wfmLen);
        Sig[4] = sqrt(Ssum/wfmLen);
        Sig[5] = sqrt(Xsum/wfmLen);
        Sig[6] = sqrt(Ysum/wfmLen);
        Sig[0] = sqrt(Asum/wfmLen);
        Sig[1] = sqrt(Bsum/wfmLen);
        Sig[2] = sqrt(Csum/wfmLen);
        Sig[3] = sqrt(Dsum/wfmLen);
        Sig[4] = sqrt(Ssum/wfmLen);
        Sig[5] = sqrt(Xsum/wfmLen);
        Sig[6] = sqrt(Ysum/wfmLen);
        precord->nevc = wfmLen;
        precord->nevd = wfmLen;
        precord->neve = wfmLen;
        precord->nevf = wfmLen;
        precord->nevg = wfmLen;
        precord->nevh = wfmLen;
        precord->nevi = wfmLen;
        precord->nevj = wfmLen;
        memcpy((float *)precord->valc,Awfm,wfmLen*sizeof(float));
        memcpy((float *)precord->vald,Bwfm,wfmLen*sizeof(float));
        memcpy((float *)precord->vale,Cwfm,wfmLen*sizeof(float));
        memcpy((float *)precord->valf,Dwfm,wfmLen*sizeof(float));
        memcpy((float *)precord->valg,Swfm,wfmLen*sizeof(float));
        memcpy((float *)precord->valh,Xwfm,wfmLen*sizeof(float));
        memcpy((float *)precord->vali,Ywfm,wfmLen*sizeof(float));
        memcpy((float *)precord->valj,Twfm,wfmLen*sizeof(float));
        memcpy((float *)precord->vall,Avg,10*sizeof(float));
        memcpy((float *)precord->valm,Sig,10*sizeof(float));
    }
    oldready = ready;
    return(0);
}
// Note the function must be registered at the end!
epicsRegisterFunction(TBTsub);
