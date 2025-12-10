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
#include <aSubRecord.h>
#include <registryFunction.h>
#include <epicsExport.h>

#define ADCMAX 8000
#define TBTMAX 8000

static int LiveSub(aSubRecord *precord) {
    int i;

    float *Abuff = (float *)precord->a;
    float *Bbuff = (float *)precord->b;
    float *Cbuff = (float *)precord->c;
    float *Dbuff = (float *)precord->d;
    float *Xbuff = (float *)precord->i;
    float *Ybuff = (float *)precord->j;

    int ADCwfmLen = *(int *)precord->e;
    int ADCwfmOff = *(int *)precord->f;
    int TBTwfmLen = *(int *)precord->k;
    int TBTwfmOff = *(int *)precord->l;

    if(ADCwfmLen>ADCMAX) ADCwfmLen=ADCMAX;
    if(ADCwfmLen<50) ADCwfmLen=50;
    if(ADCwfmOff>(ADCMAX-ADCwfmLen)) ADCwfmOff=(ADCMAX-ADCwfmLen);
    if(ADCwfmOff<0) ADCwfmOff=0;
    *(int *)precord->vale = ADCwfmLen;
    *(int *)precord->valf = ADCwfmOff;

    if(TBTwfmLen>TBTMAX) TBTwfmLen=TBTMAX;
    if(TBTwfmLen<50) TBTwfmLen=50;
    if(TBTwfmOff>(TBTMAX-TBTwfmLen)) TBTwfmOff=(TBTMAX-TBTwfmLen);
    if(TBTwfmOff<0) TBTwfmOff=0;
    *(int *)precord->valg = TBTwfmLen;
    *(int *)precord->valh = TBTwfmOff;

    float Awfm[8000],Bwfm[8000],Cwfm[8000],Dwfm[8000],Twfm[8000];

    for(i=ADCwfmOff;i<ADCwfmOff+ADCwfmLen;i++){
       Awfm[i-ADCwfmOff] = Abuff[i];
       Bwfm[i-ADCwfmOff] = Bbuff[i];
       Cwfm[i-ADCwfmOff] = Cbuff[i];
       Dwfm[i-ADCwfmOff] = Dbuff[i];
       Twfm[i-ADCwfmOff] = (i-ADCwfmOff)*0.008521583;
    }
    precord->nevi = ADCwfmLen;
    precord->nevj = ADCwfmLen;
    precord->nevk = ADCwfmLen;
    precord->nevl = ADCwfmLen;
    precord->nevm = ADCwfmLen;
    memcpy((float *)precord->vali,Awfm,ADCwfmLen*sizeof(float));
    memcpy((float *)precord->valj,Bwfm,ADCwfmLen*sizeof(float));
    memcpy((float *)precord->valk,Cwfm,ADCwfmLen*sizeof(float));
    memcpy((float *)precord->vall,Dwfm,ADCwfmLen*sizeof(float));
    memcpy((float *)precord->valm,Twfm,ADCwfmLen*sizeof(float));

// TBT Live:

    float Xwfm[8000],Ywfm[8000],Xsum=0,Ysum=0,Xavg,Yavg,Xsig,Ysig;

    for(i=TBTwfmOff;i<TBTwfmOff+TBTwfmLen;i++){
       Xwfm[i-TBTwfmOff] = Xbuff[i];
       Xsum = Xsum + Xbuff[i];
       Ywfm[i-TBTwfmOff] = Ybuff[i];
       Ysum = Ysum + Ybuff[i];
       Twfm[i-TBTwfmOff] = (i-TBTwfmOff)*0.002641691;
    }

    Xavg = Xsum/TBTwfmLen;
    Yavg = Ysum/TBTwfmLen;
    *(float *)precord->vala = Xavg;
    *(float *)precord->valb = Yavg;

    Xsum=0;
    Ysum=0;
    for(i=0;i<TBTwfmLen;i++){
        Xsum = Xsum + (Xwfm[i]-Xavg)*(Xwfm[i]-Xavg);
        Ysum = Ysum + (Ywfm[i]-Yavg)*(Ywfm[i]-Yavg);
    }

    Xsig = sqrt(Xsum/TBTwfmLen);
    Ysig = sqrt(Ysum/TBTwfmLen);
    *(float *)precord->valc = Xsig;
    *(float *)precord->vald = Ysig;
    precord->nevn = TBTwfmLen;
    precord->nevo = TBTwfmLen;
    precord->nevp = TBTwfmLen;
    memcpy((float *)precord->valn,Xwfm,TBTwfmLen*sizeof(float));
    memcpy((float *)precord->valo,Ywfm,TBTwfmLen*sizeof(float));
    memcpy((float *)precord->valp,Twfm,TBTwfmLen*sizeof(float));

    return(0);
}
// Note the function must be registered at the end!
epicsRegisterFunction(LiveSub);
