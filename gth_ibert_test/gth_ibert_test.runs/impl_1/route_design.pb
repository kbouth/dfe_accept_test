
Q
Command: %s
53*	vivadotcl2 
route_design2default:defaultZ4-113h px� 
�
@Attempting to get a license for feature '%s' and/or device '%s'
308*common2"
Implementation2default:default2
xczu6eg2default:defaultZ17-347h px� 
�
0Got license for feature '%s' and/or device '%s'
310*common2"
Implementation2default:default2
xczu6eg2default:defaultZ17-349h px� 
�
�The version limit for your license is '%s' and has expired for new software. A version limit expiration means that, although you may be able to continue to use the current version of tools or IP with this license, you will not be eligible for new releases.
719*common2
2025.022default:defaultZ17-1540h px� 
p
,Running DRC as a precondition to command %s
22*	vivadotcl2 
route_design2default:defaultZ4-22h px� 
P
Running DRC with %s threads
24*drc2
82default:defaultZ23-27h px� 
V
DRC finished with %s
79*	vivadotcl2
0 Errors2default:defaultZ4-198h px� 
e
BPlease refer to the DRC report (report_drc) for more information.
80*	vivadotclZ4-199h px� 
V

Starting %s Task
103*constraints2
Routing2default:defaultZ18-103h px� 
}
BMultithreading enabled for route_design using a maximum of %s CPUs17*	routeflow2
82default:defaultZ35-254h px� 
p

Phase %s%s
101*constraints2
1 2default:default2#
Build RT Design2default:defaultZ18-101h px� 
�
r%sTime (s): cpu = %s ; elapsed = %s . Memory (MB): peak = %s ; gain = %s ; free physical = %s ; free virtual = %s
480*common22
Nodegraph reading from file.  2default:default2
00:00:00.292default:default2
00:00:00.342default:default2
5448.8552default:default2
0.0002default:default2
102512default:default2
860932default:defaultZ17-722h px� 
[
%s*common2B
.Phase 1 Build RT Design | Checksum: 1a5fac3a3
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:12 ; elapsed = 00:00:05 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10295 ; free virtual = 861362default:defaulth px� 
v

Phase %s%s
101*constraints2
2 2default:default2)
Router Initialization2default:defaultZ18-101h px� 
{

Phase %s%s
101*constraints2
2.1 2default:default2,
Fix Topology Constraints2default:defaultZ18-101h px� 
f
%s*common2M
9Phase 2.1 Fix Topology Constraints | Checksum: 1a5fac3a3
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:12 ; elapsed = 00:00:05 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10232 ; free virtual = 860742default:defaulth px� 
t

Phase %s%s
101*constraints2
2.2 2default:default2%
Pre Route Cleanup2default:defaultZ18-101h px� 
_
%s*common2F
2Phase 2.2 Pre Route Cleanup | Checksum: 1a5fac3a3
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:12 ; elapsed = 00:00:05 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10232 ; free virtual = 860732default:defaulth px� 
{

Phase %s%s
101*constraints2
2.3 2default:default2,
Global Clock Net Routing2default:defaultZ18-101h px� 
f
%s*common2M
9Phase 2.3 Global Clock Net Routing | Checksum: 227da9266
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:14 ; elapsed = 00:00:06 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10071 ; free virtual = 859132default:defaulth px� 
p

Phase %s%s
101*constraints2
2.4 2default:default2!
Update Timing2default:defaultZ18-101h px� 
[
%s*common2B
.Phase 2.4 Update Timing | Checksum: 246a791b6
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:19 ; elapsed = 00:00:08 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10086 ; free virtual = 859282default:defaulth px� 
�
Intermediate Timing Summary %s164*route2J
6| WNS=2.024  | TNS=0.000  | WHS=-0.147 | THS=-17.479|
2default:defaultZ35-416h px� 
}

Phase %s%s
101*constraints2
2.5 2default:default2.
Update Timing for Bus Skew2default:defaultZ18-101h px� 
r

Phase %s%s
101*constraints2
2.5.1 2default:default2!
Update Timing2default:defaultZ18-101h px� 
]
%s*common2D
0Phase 2.5.1 Update Timing | Checksum: 28e895637
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:33 ; elapsed = 00:00:12 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10256 ; free virtual = 860912default:defaulth px� 
�
Intermediate Timing Summary %s164*route2J
6| WNS=2.024  | TNS=0.000  | WHS=N/A    | THS=N/A    |
2default:defaultZ35-416h px� 
h
%s*common2O
;Phase 2.5 Update Timing for Bus Skew | Checksum: 2bd11e6eb
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:33 ; elapsed = 00:00:12 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10257 ; free virtual = 860922default:defaulth px� 
a
%s*common2H
4Phase 2 Router Initialization | Checksum: 2071cd6fc
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:34 ; elapsed = 00:00:12 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10272 ; free virtual = 861072default:defaulth px� 
p

Phase %s%s
101*constraints2
3 2default:default2#
Initial Routing2default:defaultZ18-101h px� 
q

Phase %s%s
101*constraints2
3.1 2default:default2"
Global Routing2default:defaultZ18-101h px� 
\
%s*common2C
/Phase 3.1 Global Routing | Checksum: 2071cd6fc
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:34 ; elapsed = 00:00:12 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10272 ; free virtual = 861072default:defaulth px� 
[
%s*common2B
.Phase 3 Initial Routing | Checksum: 1f8046d97
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:41 ; elapsed = 00:00:14 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10330 ; free virtual = 861652default:defaulth px� 
s

Phase %s%s
101*constraints2
4 2default:default2&
Rip-up And Reroute2default:defaultZ18-101h px� 
u

Phase %s%s
101*constraints2
4.1 2default:default2&
Global Iteration 02default:defaultZ18-101h px� 
�
Intermediate Timing Summary %s164*route2J
6| WNS=1.511  | TNS=0.000  | WHS=-0.023 | THS=-0.023 |
2default:defaultZ35-416h px� 
`
%s*common2G
3Phase 4.1 Global Iteration 0 | Checksum: 1f818f080
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:32 ; elapsed = 00:00:38 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10235 ; free virtual = 860692default:defaulth px� 
�

Phase %s%s
101*constraints2
4.2 2default:default21
Additional Iteration for Hold2default:defaultZ18-101h px� 
k
%s*common2R
>Phase 4.2 Additional Iteration for Hold | Checksum: 276209d89
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:32 ; elapsed = 00:00:38 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10229 ; free virtual = 860692default:defaulth px� 
^
%s*common2E
1Phase 4 Rip-up And Reroute | Checksum: 276209d89
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:32 ; elapsed = 00:00:38 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10230 ; free virtual = 860702default:defaulth px� 
|

Phase %s%s
101*constraints2
5 2default:default2/
Delay and Skew Optimization2default:defaultZ18-101h px� 
p

Phase %s%s
101*constraints2
5.1 2default:default2!
Delay CleanUp2default:defaultZ18-101h px� 
r

Phase %s%s
101*constraints2
5.1.1 2default:default2!
Update Timing2default:defaultZ18-101h px� 
]
%s*common2D
0Phase 5.1.1 Update Timing | Checksum: 24e599c44
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:37 ; elapsed = 00:00:40 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10221 ; free virtual = 860602default:defaulth px� 
�
Intermediate Timing Summary %s164*route2J
6| WNS=1.511  | TNS=0.000  | WHS=0.010  | THS=0.000  |
2default:defaultZ35-416h px� 
r

Phase %s%s
101*constraints2
5.1.2 2default:default2!
Update Timing2default:defaultZ18-101h px� 
]
%s*common2D
0Phase 5.1.2 Update Timing | Checksum: 233ee8da4
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:41 ; elapsed = 00:00:41 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10217 ; free virtual = 860522default:defaulth px� 
�
Intermediate Timing Summary %s164*route2J
6| WNS=1.511  | TNS=0.000  | WHS=0.010  | THS=0.000  |
2default:defaultZ35-416h px� 
[
%s*common2B
.Phase 5.1 Delay CleanUp | Checksum: 2aa087f53
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:41 ; elapsed = 00:00:41 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10217 ; free virtual = 860522default:defaulth px� 
z

Phase %s%s
101*constraints2
5.2 2default:default2+
Clock Skew Optimization2default:defaultZ18-101h px� 
e
%s*common2L
8Phase 5.2 Clock Skew Optimization | Checksum: 2aa087f53
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:41 ; elapsed = 00:00:41 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10217 ; free virtual = 860522default:defaulth px� 
g
%s*common2N
:Phase 5 Delay and Skew Optimization | Checksum: 2aa087f53
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:41 ; elapsed = 00:00:41 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10217 ; free virtual = 860522default:defaulth px� 
n

Phase %s%s
101*constraints2
6 2default:default2!
Post Hold Fix2default:defaultZ18-101h px� 
p

Phase %s%s
101*constraints2
6.1 2default:default2!
Hold Fix Iter2default:defaultZ18-101h px� 
r

Phase %s%s
101*constraints2
6.1.1 2default:default2!
Update Timing2default:defaultZ18-101h px� 
]
%s*common2D
0Phase 6.1.1 Update Timing | Checksum: 31ffd37f4
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:45 ; elapsed = 00:00:43 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10062 ; free virtual = 859032default:defaulth px� 
�
Intermediate Timing Summary %s164*route2J
6| WNS=1.511  | TNS=0.000  | WHS=0.010  | THS=0.000  |
2default:defaultZ35-416h px� 
[
%s*common2B
.Phase 6.1 Hold Fix Iter | Checksum: 280655bae
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:45 ; elapsed = 00:00:43 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10067 ; free virtual = 859092default:defaulth px� 
Y
%s*common2@
,Phase 6 Post Hold Fix | Checksum: 280655bae
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:45 ; elapsed = 00:00:43 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10056 ; free virtual = 859042default:defaulth px� 
o

Phase %s%s
101*constraints2
7 2default:default2"
Route finalize2default:defaultZ18-101h px� 
Z
%s*common2A
-Phase 7 Route finalize | Checksum: 27214c6a3
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:46 ; elapsed = 00:00:43 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10029 ; free virtual = 858762default:defaulth px� 
v

Phase %s%s
101*constraints2
8 2default:default2)
Verifying routed nets2default:defaultZ18-101h px� 
a
%s*common2H
4Phase 8 Verifying routed nets | Checksum: 27214c6a3
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:46 ; elapsed = 00:00:43 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10033 ; free virtual = 858812default:defaulth px� 
r

Phase %s%s
101*constraints2
9 2default:default2%
Depositing Routes2default:defaultZ18-101h px� 
�
,Router swapped GT pin %s to physical pin %s
200*route2�
Iu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common/GTNORTHREFCLK00Iu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common/GTNORTHREFCLK002default:default2Z
!GTHE4_COMMON_X0Y2/COM0_REFCLKOUT3!GTHE4_COMMON_X0Y2/COM0_REFCLKOUT32default:default8Z35-467h px� 
�
,Router swapped GT pin %s to physical pin %s
200*route2�
Iu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common/GTNORTHREFCLK01Iu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common/GTNORTHREFCLK012default:default2Z
!GTHE4_COMMON_X0Y2/COM2_REFCLKOUT3!GTHE4_COMMON_X0Y2/COM2_REFCLKOUT32default:default8Z35-467h px� 
]
%s*common2D
0Phase 9 Depositing Routes | Checksum: 27214c6a3
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:48 ; elapsed = 00:00:45 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10017 ; free virtual = 858632default:defaulth px� 
o

Phase %s%s
101*constraints2
10 2default:default2!
Resolve XTalk2default:defaultZ18-101h px� 
Z
%s*common2A
-Phase 10 Resolve XTalk | Checksum: 27214c6a3
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:48 ; elapsed = 00:00:45 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10023 ; free virtual = 858692default:defaulth px� 
t

Phase %s%s
101*constraints2
11 2default:default2&
Post Router Timing2default:defaultZ18-101h px� 
�
Estimated Timing Summary %s
57*route2J
6| WNS=1.511  | TNS=0.000  | WHS=0.010  | THS=0.000  |
2default:defaultZ35-57h px� 
�
�The final timing numbers are based on the router estimated timing analysis. For a complete and accurate timing signoff, please run report_timing_summary.
127*routeZ35-327h px� 
_
%s*common2F
2Phase 11 Post Router Timing | Checksum: 27214c6a3
2default:defaulth px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:50 ; elapsed = 00:00:45 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10021 ; free virtual = 858672default:defaulth px� 
@
Router Completed Successfully
2*	routeflowZ35-16h px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:50 ; elapsed = 00:00:45 . Memory (MB): peak = 5448.855 ; gain = 0.000 ; free physical = 10123 ; free virtual = 859692default:defaulth px� 
Z
Releasing license: %s
83*common2"
Implementation2default:defaultZ17-83h px� 
�
G%s Infos, %s Warnings, %s Critical Warnings and %s Errors encountered.
28*	vivadotcl2
1602default:default2
2022default:default2
02default:default2
02default:defaultZ4-41h px� 
^
%s completed successfully
29*	vivadotcl2 
route_design2default:defaultZ4-42h px� 
�
r%sTime (s): cpu = %s ; elapsed = %s . Memory (MB): peak = %s ; gain = %s ; free physical = %s ; free virtual = %s
480*common2"
route_design: 2default:default2
00:01:532default:default2
00:00:462default:default2
5448.8552default:default2
0.0002default:default2
101232default:default2
859692default:defaultZ17-722h px� 
H
&Writing timing data to binary archive.266*timingZ38-480h px� 
=
Writing XDEF routing.
211*designutilsZ20-211h px� 
J
#Writing XDEF routing logical nets.
209*designutilsZ20-209h px� 
J
#Writing XDEF routing special nets.
210*designutilsZ20-210h px� 
�
r%sTime (s): cpu = %s ; elapsed = %s . Memory (MB): peak = %s ; gain = %s ; free physical = %s ; free virtual = %s
480*common2)
Write XDEF Complete: 2default:default2
00:00:052default:default2
00:00:022default:default2
5448.8552default:default2
0.0002default:default2
100612default:default2
859852default:defaultZ17-722h px� 
�
 The %s '%s' has been generated.
621*common2

checkpoint2default:default2�
{/home/bouthsarath/ibert_ultrascale_gth_1_ex/ibert_ultrascale_gth_1_ex.runs/impl_1/example_ibert_ultrascale_gth_1_routed.dcp2default:defaultZ17-1381h px� 
�
%s4*runtcl2�
�Executing : report_drc -file example_ibert_ultrascale_gth_1_drc_routed.rpt -pb example_ibert_ultrascale_gth_1_drc_routed.pb -rpx example_ibert_ultrascale_gth_1_drc_routed.rpx
2default:defaulth px� 
�
Command: %s
53*	vivadotcl2�
�report_drc -file example_ibert_ultrascale_gth_1_drc_routed.rpt -pb example_ibert_ultrascale_gth_1_drc_routed.pb -rpx example_ibert_ultrascale_gth_1_drc_routed.rpx2default:defaultZ4-113h px� 
>
IP Catalog is up to date.1232*coregenZ19-1839h px� 
P
Running DRC with %s threads
24*drc2
82default:defaultZ23-27h px� 
�
#The results of DRC are in file %s.
586*	vivadotcl2�
/home/bouthsarath/ibert_ultrascale_gth_1_ex/ibert_ultrascale_gth_1_ex.runs/impl_1/example_ibert_ultrascale_gth_1_drc_routed.rpt/home/bouthsarath/ibert_ultrascale_gth_1_ex/ibert_ultrascale_gth_1_ex.runs/impl_1/example_ibert_ultrascale_gth_1_drc_routed.rpt2default:default8Z2-168h px� 
\
%s completed successfully
29*	vivadotcl2

report_drc2default:defaultZ4-42h px� 
�
%s4*runtcl2�
�Executing : report_methodology -file example_ibert_ultrascale_gth_1_methodology_drc_routed.rpt -pb example_ibert_ultrascale_gth_1_methodology_drc_routed.pb -rpx example_ibert_ultrascale_gth_1_methodology_drc_routed.rpx
2default:defaulth px� 
�
Command: %s
53*	vivadotcl2�
�report_methodology -file example_ibert_ultrascale_gth_1_methodology_drc_routed.rpt -pb example_ibert_ultrascale_gth_1_methodology_drc_routed.pb -rpx example_ibert_ultrascale_gth_1_methodology_drc_routed.rpx2default:defaultZ4-113h px� 
E
%Done setting XDC timing constraints.
35*timingZ38-35h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr0_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr0_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr0_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr0_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr1_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr1_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr1_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr1_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr2_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr2_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr2_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr2_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr3_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr3_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr3_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr3_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr0_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr0_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr0_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr0_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr1_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr1_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr1_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr1_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr2_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr2_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr2_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr2_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr3_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr3_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr3_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr3_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr0_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr0_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr0_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr0_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr1_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr1_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr1_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr1_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr2_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr2_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr2_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr2_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr3_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr3_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr3_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr3_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr0_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr0_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr0_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr0_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr1_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr1_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr1_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr1_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr2_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr2_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr2_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr2_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr3_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr3_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr3_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr3_12default:default8Z38-252h px� 
�
�The instance %s has %s pins that are not tied constant, so the worst case value will be used for automatic derivation of generated clocks274*timing2�
9u_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_gthe4_common	9u_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_gthe4_common2default:default2
	SDM0WIDTH2default:default8Z38-491h px� 
�
�The instance %s has %s pins that are not tied constant, so the worst case value will be used for automatic derivation of generated clocks274*timing2�
9u_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_gthe4_common	9u_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_gthe4_common2default:default2
SDM0DATA2default:default8Z38-491h px� 
�
�The instance %s has %s pins that are not tied constant, so the worst case value will be used for automatic derivation of generated clocks274*timing2�
9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common	9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common2default:default2
	SDM0WIDTH2default:default8Z38-491h px� 
�
�The instance %s has %s pins that are not tied constant, so the worst case value will be used for automatic derivation of generated clocks274*timing2�
9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common	9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common2default:default2
SDM0DATA2default:default8Z38-491h px� 
�
�The instance %s has %s pins that are not tied constant, so the worst case value will be used for automatic derivation of generated clocks274*timing2�
9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common	9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common2default:default2
	SDM1WIDTH2default:default8Z38-491h px� 
�
�The instance %s has %s pins that are not tied constant, so the worst case value will be used for automatic derivation of generated clocks274*timing2�
9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common	9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common2default:default2
SDM1DATA2default:default8Z38-491h px� 
Y
$Running Methodology with %s threads
74*drc2
82default:defaultZ23-133h px� 
�
2The results of Report Methodology are in file %s.
609*	vivadotcl2�
�/home/bouthsarath/ibert_ultrascale_gth_1_ex/ibert_ultrascale_gth_1_ex.runs/impl_1/example_ibert_ultrascale_gth_1_methodology_drc_routed.rpt�/home/bouthsarath/ibert_ultrascale_gth_1_ex/ibert_ultrascale_gth_1_ex.runs/impl_1/example_ibert_ultrascale_gth_1_methodology_drc_routed.rpt2default:default8Z2-1520h px� 
d
%s completed successfully
29*	vivadotcl2&
report_methodology2default:defaultZ4-42h px� 
�
%s4*runtcl2�
�Executing : report_power -file example_ibert_ultrascale_gth_1_power_routed.rpt -pb example_ibert_ultrascale_gth_1_power_summary_routed.pb -rpx example_ibert_ultrascale_gth_1_power_routed.rpx
2default:defaulth px� 
�
Command: %s
53*	vivadotcl2�
�report_power -file example_ibert_ultrascale_gth_1_power_routed.rpt -pb example_ibert_ultrascale_gth_1_power_summary_routed.pb -rpx example_ibert_ultrascale_gth_1_power_routed.rpx2default:defaultZ4-113h px� 
E
%Done setting XDC timing constraints.
35*timingZ38-35h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr0_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr0_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr0_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr0_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr1_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr1_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr1_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr1_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr2_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr2_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr2_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr2_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr3_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr3_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr3_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/rx_ind.u_rxusr3_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr0_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr0_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr0_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr0_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr1_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr1_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr1_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr1_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr2_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr2_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr2_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr2_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr3_0	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr3_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr3_1	Gu_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_clocking/tx_ind.u_txusr3_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr0_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr0_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr0_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr0_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr1_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr1_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr1_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr1_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr2_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr2_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr2_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr2_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr3_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr3_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr3_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/rx_ind.u_rxusr3_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr0_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr0_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr0_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr0_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr1_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr1_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr1_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr1_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr2_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr2_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr2_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr2_12default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr3_0	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr3_02default:default8Z38-252h px� 
�
�The BUFG_GT instance '%s' has DIV pins that are not tied constant, so the automatically derived generated clock will use a worst case divide of 1.177*timing2�
Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr3_1	Gu_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_clocking/tx_ind.u_txusr3_12default:default8Z38-252h px� 
�
�The instance %s has %s pins that are not tied constant, so the worst case value will be used for automatic derivation of generated clocks274*timing2�
9u_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_gthe4_common	9u_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_gthe4_common2default:default2
	SDM0WIDTH2default:default8Z38-491h px� 
�
�The instance %s has %s pins that are not tied constant, so the worst case value will be used for automatic derivation of generated clocks274*timing2�
9u_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_gthe4_common	9u_ibert_gth_core/inst/QUAD[0].u_q/u_common/u_gthe4_common2default:default2
SDM0DATA2default:default8Z38-491h px� 
�
�The instance %s has %s pins that are not tied constant, so the worst case value will be used for automatic derivation of generated clocks274*timing2�
9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common	9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common2default:default2
	SDM0WIDTH2default:default8Z38-491h px� 
�
�The instance %s has %s pins that are not tied constant, so the worst case value will be used for automatic derivation of generated clocks274*timing2�
9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common	9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common2default:default2
SDM0DATA2default:default8Z38-491h px� 
�
�The instance %s has %s pins that are not tied constant, so the worst case value will be used for automatic derivation of generated clocks274*timing2�
9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common	9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common2default:default2
	SDM1WIDTH2default:default8Z38-491h px� 
�
�The instance %s has %s pins that are not tied constant, so the worst case value will be used for automatic derivation of generated clocks274*timing2�
9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common	9u_ibert_gth_core/inst/QUAD[1].u_q/u_common/u_gthe4_common2default:default2
SDM1DATA2default:default8Z38-491h px� 
K
,Running Vector-less Activity Propagation...
51*powerZ33-51h px� 
P
3
Finished Running Vector-less Activity Propagation
1*powerZ33-1h px� 
�
G%s Infos, %s Warnings, %s Critical Warnings and %s Errors encountered.
28*	vivadotcl2
1722default:default2
2782default:default2
02default:default2
02default:defaultZ4-41h px� 
^
%s completed successfully
29*	vivadotcl2 
report_power2default:defaultZ4-42h px� 
�
r%sTime (s): cpu = %s ; elapsed = %s . Memory (MB): peak = %s ; gain = %s ; free physical = %s ; free virtual = %s
480*common2"
report_power: 2default:default2
00:00:162default:default2
00:00:072default:default2
5464.8632default:default2
16.0082default:default2
99552default:default2
858542default:defaultZ17-722h px� 
�
%s4*runtcl2�
�Executing : report_route_status -file example_ibert_ultrascale_gth_1_route_status.rpt -pb example_ibert_ultrascale_gth_1_route_status.pb
2default:defaulth px� 
�
%s4*runtcl2�
�Executing : report_timing_summary -max_paths 10 -report_unconstrained -file example_ibert_ultrascale_gth_1_timing_summary_routed.rpt -pb example_ibert_ultrascale_gth_1_timing_summary_routed.pb -rpx example_ibert_ultrascale_gth_1_timing_summary_routed.rpx -warn_on_violation 
2default:defaulth px� 
�
UpdateTimingParams:%s.
91*timing2O
; Speed grade: -1, Temperature grade: E, Delay Type: min_max2default:defaultZ38-91h px� 
|
CMultithreading enabled for timing update using a maximum of %s CPUs155*timing2
82default:defaultZ38-191h px� 
�
}There are set_bus_skew constraint(s) in this design. Please run report_bus_skew to ensure that bus skew requirements are met.223*timingZ38-436h px� 
�
%s4*runtcl2{
gExecuting : report_incremental_reuse -file example_ibert_ultrascale_gth_1_incremental_reuse_routed.rpt
2default:defaulth px� 
g
BIncremental flow is disabled. No incremental reuse Info to report.423*	vivadotclZ4-1062h px� 
�
%s4*runtcl2{
gExecuting : report_clock_utilization -file example_ibert_ultrascale_gth_1_clock_utilization_routed.rpt
2default:defaulth px� 
�
%s4*runtcl2�
�Executing : report_bus_skew -warn_on_violation -file example_ibert_ultrascale_gth_1_bus_skew_routed.rpt -pb example_ibert_ultrascale_gth_1_bus_skew_routed.pb -rpx example_ibert_ultrascale_gth_1_bus_skew_routed.rpx
2default:defaulth px� 
�
UpdateTimingParams:%s.
91*timing2O
; Speed grade: -1, Temperature grade: E, Delay Type: min_max2default:defaultZ38-91h px� 
|
CMultithreading enabled for timing update using a maximum of %s CPUs155*timing2
82default:defaultZ38-191h px� 


End Record