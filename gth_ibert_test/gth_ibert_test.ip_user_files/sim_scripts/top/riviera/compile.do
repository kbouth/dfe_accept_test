vlib work
vlib riviera

vlib riviera/xilinx_vip
vlib riviera/xpm
vlib riviera/xil_defaultlib
vlib riviera/lib_cdc_v1_0_2
vlib riviera/proc_sys_reset_v5_0_13

vmap xilinx_vip riviera/xilinx_vip
vmap xpm riviera/xpm
vmap xil_defaultlib riviera/xil_defaultlib
vmap lib_cdc_v1_0_2 riviera/lib_cdc_v1_0_2
vmap proc_sys_reset_v5_0_13 riviera/proc_sys_reset_v5_0_13

vlog -work xilinx_vip  -sv2k12 "+incdir+/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/include" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/axi4stream_vip_axi4streampc.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/axi_vip_axi4pc.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/xil_common_vip_pkg.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/axi4stream_vip_pkg.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/axi_vip_pkg.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/axi4stream_vip_if.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/axi_vip_if.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/clk_vip_if.sv" \
"/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/hdl/rst_vip_if.sv" \

vlog -work xpm  -sv2k12 "+incdir+../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/bd/top/ipshared/ec67/hdl" "+incdir+../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/bd/top/ipshared/abef/hdl" "+incdir+../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/bd/top/ipshared/f0b6/hdl/verilog" "+incdir+../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/bd/top/ipshared/66be/hdl/verilog" "+incdir+/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/include" \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_fifo/hdl/xpm_fifo.sv" \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \

vcom -work xpm -93  \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_VCOMP.vhd" \

vcom -work xil_defaultlib -93  \
"../../../bd/top/ip/top_zynq_ultra_ps_e_0_0/top_zynq_ultra_ps_e_0_0_sim_netlist.vhdl" \
"/home/bouthsarath/ibert_ultrascale_gth_1_ex/ibert_ultrascale_gth_1_ex.gen/sources_1/bd/top/ip/top_smartconnect_0_0/top_smartconnect_0_0_sim_netlist.vhdl" \

vcom -work lib_cdc_v1_0_2 -93  \
"../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/bd/top/ipshared/ef1e/hdl/lib_cdc_v1_0_rfs.vhd" \

vcom -work proc_sys_reset_v5_0_13 -93  \
"../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/bd/top/ipshared/8842/hdl/proc_sys_reset_v5_0_vh_rfs.vhd" \

vcom -work xil_defaultlib -93  \
"../../../bd/top/ip/top_proc_sys_reset_0_0/sim/top_proc_sys_reset_0_0.vhd" \
"../../../bd/top/sim/top.vhd" \

vlog -work xil_defaultlib \
"glbl.v"

