vlib questa_lib/work
vlib questa_lib/msim

vlib questa_lib/msim/xilinx_vip
vlib questa_lib/msim/xpm
vlib questa_lib/msim/xil_defaultlib

vmap xilinx_vip questa_lib/msim/xilinx_vip
vmap xpm questa_lib/msim/xpm
vmap xil_defaultlib questa_lib/msim/xil_defaultlib

vlog -work xilinx_vip -64 -incr -mfcu  -sv -L axi_vip_v1_1_13 -L smartconnect_v1_0 -L zynq_ultra_ps_e_vip_v1_0_13 -L xilinx_vip "+incdir+/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/include" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/axi4stream_vip_axi4streampc.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/axi_vip_axi4pc.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/xil_common_vip_pkg.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/axi4stream_vip_pkg.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/axi_vip_pkg.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/axi4stream_vip_if.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/axi_vip_if.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/clk_vip_if.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/rst_vip_if.sv" \

vlog -work xpm -64 -incr -mfcu  -sv -L axi_vip_v1_1_13 -L smartconnect_v1_0 -L zynq_ultra_ps_e_vip_v1_0_13 -L xilinx_vip "+incdir+../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/ip/ibert_ultrascale_gth_1/hdl/verilog" "+incdir+../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/ip/ibert_ultrascale_gth_1/synth" "+incdir+/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/include" \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_fifo/hdl/xpm_fifo.sv" \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \

vcom -work xpm -64 -93  \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_VCOMP.vhd" \

vcom -work xil_defaultlib -64 -93  \
"../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/ip/ibert_ultrascale_gth_1/ibert_ultrascale_gth_1_sim_netlist.vhdl" \

vlog -work xil_defaultlib \
"glbl.v"

