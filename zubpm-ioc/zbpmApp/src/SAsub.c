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

#define BUFMAX 576000

static int SAsub(aSubRecord *precord) {

    static float Abuff[BUFMAX],Bbuff[BUFMAX],Cbuff[BUFMAX],Dbuff[BUFMAX];
    static float Sbuff[BUFMAX],Xbuff[BUFMAX],Ybuff[BUFMAX];

    static int topIndx=0,Count=0;

    int i,wfmCnt;
    float Awfm[10000],Bwfm[10000],Cwfm[10000],Dwfm[10000];
    float Swfm[10000],Xwfm[10000],Ywfm[10000],Twfm[10000];
    float XMwfm[100],XSwfm[10],YMwfm[100],YSwfm[10];
    float Avg[10],Sig[10];
    double Asum=0,Bsum=0,Csum=0,Dsum=0,Ssum=0,Xsum=0,Ysum=0;

    double A = *(double *)precord->a;
    double B = *(double *)precord->b;
    double C = *(double *)precord->c;
    double D = *(double *)precord->d;
    double S = *(double *)precord->e;
    double X = *(double *)precord->f;
    double Y = *(double *)precord->g;
    int TrigCnt = *(int *)precord->h;
    int SAlen = *(int *)precord->i;
    int SAdec = *(int *)precord->j;
    int reset = *(int *)precord->k;
    int tsec = *(int *)precord->l;

    time_t evrTime;
    struct tm ts;
    char tmstr[80];

//    if(TrigCnt%10==0) printf("TrigCnt = %d\n",TrigCnt);
    evrTime = (time_t)tsec;
    ts = *localtime(&evrTime);
    strftime(tmstr,sizeof(tmstr), "%b %d %Y %H:%M:%S %Z", &ts);

    if(reset==1){
        printf("Resetting...\n");
        topIndx = 0;
        Count = 0;
        reset = 0;
        *(int *)precord->valo = reset;
    }

    Abuff[topIndx] = (float)A;
    Bbuff[topIndx] = (float)B;
    Cbuff[topIndx] = (float)C;
    Dbuff[topIndx] = (float)D;
    Sbuff[topIndx] = (float)S;
    Xbuff[topIndx] = (float)X;
    Ybuff[topIndx] = (float)Y;

    if(Count<BUFMAX){
        int endIndx = topIndx - topIndx%SAdec;
        if((SAlen*SAdec)>endIndx) SAlen = endIndx/SAdec;
        int startIndx = endIndx - (SAlen-1)*SAdec;
        wfmCnt=0;
        for(i=startIndx;i<=endIndx;i=i+SAdec){
            Awfm[wfmCnt] = Abuff[i];
            Asum = Asum + Abuff[i];
            Bwfm[wfmCnt] = Bbuff[i];
            Bsum = Bsum + Bbuff[i];
            Cwfm[wfmCnt] = Cbuff[i];
            Csum = Csum + Cbuff[i];
            Dwfm[wfmCnt] = Dbuff[i];
            Dsum = Dsum + Dbuff[i];
            Swfm[wfmCnt] = Sbuff[i];
            Ssum = Ssum + Sbuff[i];
            Xwfm[wfmCnt] = Xbuff[i];
            Xsum = Xsum + Xbuff[i];
            Ywfm[wfmCnt] = Ybuff[i];
            Ysum = Ysum + Ybuff[i];
            Twfm[wfmCnt] = 0.001673071*wfmCnt*SAdec;  //Time in Minutes
            wfmCnt = wfmCnt + 1;
        }
    }else{
        int endIndx = topIndx - topIndx%SAdec;
        int startIndx = endIndx - (SAlen-1)*SAdec;
        wfmCnt = 0;
        if(topIndx<SAdec*SAlen){
            for(i=(BUFMAX+topIndx-SAdec*SAlen+1);i<BUFMAX;i=i+SAdec){
                Awfm[wfmCnt] = Abuff[i];
                Asum = Asum + Abuff[i];
                Bwfm[wfmCnt] = Bbuff[i];
                Bsum = Bsum + Bbuff[i];
                Cwfm[wfmCnt] = Cbuff[i];
                Csum = Csum + Cbuff[i];
                Dwfm[wfmCnt] = Dbuff[i];
                Dsum = Dsum + Dbuff[i];
                Swfm[wfmCnt] = Sbuff[i];
                Ssum = Ssum + Sbuff[i];
                Xwfm[wfmCnt] = Xbuff[i];
                Xsum = Xsum + Xbuff[i];
                Ywfm[wfmCnt] = Ybuff[i];
                Ysum = Ysum + Ybuff[i];
                Twfm[wfmCnt] = 0.001673071*wfmCnt*SAdec;  //Time in Minutes
                wfmCnt = wfmCnt + 1;
            }
            startIndx = 0;
        }
        for(i=startIndx;i<=endIndx;i=i+SAdec){
            Awfm[wfmCnt] = Abuff[i];
            Asum = Asum + Abuff[i];
            Bwfm[wfmCnt] = Bbuff[i];
            Bsum = Bsum + Bbuff[i];
            Cwfm[wfmCnt] = Cbuff[i];
            Csum = Csum + Cbuff[i];
            Dwfm[wfmCnt] = Dbuff[i];
            Dsum = Dsum + Dbuff[i];
            Swfm[wfmCnt] = Sbuff[i];
            Ssum = Ssum + Sbuff[i];
            Xwfm[wfmCnt] = Xbuff[i];
            Xsum = Xsum + Xbuff[i];
            Ywfm[wfmCnt] = Ybuff[i];
            Ysum = Ysum + Ybuff[i];
            Twfm[wfmCnt] = 0.001673071*wfmCnt*SAdec;  //Time in Minutes
            wfmCnt = wfmCnt + 1;
        }
    }

    if(wfmCnt>100){
        int indx=0;
        for(i=wfmCnt-100;i<wfmCnt;i++){
            XMwfm[indx] = Xwfm[i];
            YMwfm[indx] = Ywfm[i];
            indx = indx + 1;
        }
        indx=0;
        for(i=wfmCnt-10;i<wfmCnt;i++){
            XSwfm[indx] = Xwfm[i];
            YSwfm[indx] = Ywfm[i];
            indx = indx + 1;
        }
        memcpy((float *)precord->vali,XMwfm,100*sizeof(float));
        memcpy((float *)precord->valj,YMwfm,100*sizeof(float));
        memcpy((float *)precord->valk,XSwfm,10*sizeof(float));
        memcpy((float *)precord->vall,YSwfm,10*sizeof(float));
    }

    Avg[0] =(float)(Asum/(double)wfmCnt);
    Avg[1] =(float)(Bsum/(double)wfmCnt);
    Avg[2] =(float)(Csum/(double)wfmCnt);
    Avg[3] =(float)(Dsum/(double)wfmCnt);
    Avg[4] =(float)(Ssum/(double)wfmCnt);
    Avg[5] =(float)(Xsum/(double)wfmCnt);
    Avg[6] =(float)(Ysum/(double)wfmCnt);

    Asum = 0;
    Bsum = 0;
    Csum = 0;
    Dsum = 0;
    Ssum = 0;
    Xsum = 0;
    Ysum = 0;
    for(i=0;i<wfmCnt;i++){
        Asum = Asum + (Awfm[i]-Avg[0])*(Awfm[i]-Avg[0]);
        Bsum = Bsum + (Bwfm[i]-Avg[1])*(Bwfm[i]-Avg[1]);
        Csum = Csum + (Cwfm[i]-Avg[2])*(Cwfm[i]-Avg[2]);
        Dsum = Dsum + (Dwfm[i]-Avg[3])*(Dwfm[i]-Avg[3]);
        Ssum = Ssum + (Swfm[i]-Avg[4])*(Swfm[i]-Avg[4]);
        Xsum = Xsum + (Xwfm[i]-Avg[5])*(Xwfm[i]-Avg[5]);
        Ysum = Ysum + (Ywfm[i]-Avg[6])*(Ywfm[i]-Avg[6]);
    }
    Sig[0] = sqrt(Asum/wfmCnt);
    Sig[1] = sqrt(Bsum/wfmCnt);
    Sig[2] = sqrt(Csum/wfmCnt);
    Sig[3] = sqrt(Dsum/wfmCnt);
    Sig[4] = sqrt(Ssum/wfmCnt);
    Sig[5] = sqrt(Xsum/wfmCnt);
    Sig[6] = sqrt(Ysum/wfmCnt);
    precord->nevc = wfmCnt;
    precord->nevd = wfmCnt;
    precord->neve = wfmCnt;
    precord->nevf = wfmCnt;
    precord->nevg = wfmCnt;
    precord->nevh = wfmCnt;
    precord->nevi = wfmCnt;
    precord->nevj = wfmCnt;
    memcpy((float *)precord->vala,Awfm,wfmCnt*sizeof(float));
    memcpy((float *)precord->valb,Bwfm,wfmCnt*sizeof(float));
    memcpy((float *)precord->valc,Cwfm,wfmCnt*sizeof(float));
    memcpy((float *)precord->vald,Dwfm,wfmCnt*sizeof(float));
    memcpy((float *)precord->vale,Swfm,wfmCnt*sizeof(float));
    memcpy((float *)precord->valf,Xwfm,wfmCnt*sizeof(float));
    memcpy((float *)precord->valg,Ywfm,wfmCnt*sizeof(float));
    memcpy((float *)precord->valh,Twfm,wfmCnt*sizeof(float));
    memcpy((float *)precord->valm,Avg,10*sizeof(float));
    memcpy((float *)precord->valn,Sig,10*sizeof(float));
    memcpy((char *)precord->valp,tmstr,40*sizeof(char));
    topIndx = topIndx + 1;
    if(Count<BUFMAX) Count = Count + 1;
    if(topIndx==BUFMAX) topIndx = 0;

    return(0);
}
// Note the function must be registered at the end!
epicsRegisterFunction(SAsub);
