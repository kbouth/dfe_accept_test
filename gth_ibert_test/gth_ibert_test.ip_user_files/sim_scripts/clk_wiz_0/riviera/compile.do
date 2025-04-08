vlib work
vlib riviera

vlib riviera/xpm
vlib riviera/xil_defaultlib

vmap xpm riviera/xpm
vmap xil_defaultlib riviera/xil_defaultlib

vlog -work xpm  -sv2k12 "+incdir+../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/ip/clk_wiz_0" \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \

vcom -work xpm -93  \
"/home/bouthsarath/Vivado/2022.2/data/ip/xpm/xpm_VCOMP.vhd" \

vcom -work xil_defaultlib -93  \
"../../../../ibert_ultrascale_gth_1_ex.gen/sources_1/ip/clk_wiz_0/clk_wiz_0_sim_netlist.vhdl" \

vlog -work xil_defaultlib \
"glbl.v"

