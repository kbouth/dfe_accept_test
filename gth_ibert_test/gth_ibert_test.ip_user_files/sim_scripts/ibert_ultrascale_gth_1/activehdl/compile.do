vlib work
vlib activehdl

vlib activehdl/xilinx_vip
vlib activehdl/xpm
vlib activehdl/xil_defaultlib

vmap xilinx_vip activehdl/xilinx_vip
vmap xpm activehdl/xpm
vmap xil_defaultlib activehdl/xil_defaultlib

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

vlog -work xpm  -sv2k12 "+incdir+../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/ip/ibert_ultrascale_gth_1/hdl/verilog" "+incdir+../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/ip/ibert_ultrascale_gth_1/synth" "+incdir+/home/bouthsarath/Vivado/2022.2/data/xilinx_vip/include" \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_fifo/hdl/xpm_fifo.sv" \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \

vcom -work xpm -93  \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_VCOMP.vhd" \

vcom -work xil_defaultlib -93  \
"../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/ip/ibert_ultrascale_gth_1/ibert_ultrascale_gth_1_sim_netlist.vhdl" \

vlog -work xil_defaultlib \
"glbl.v"

