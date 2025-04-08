
connect -url tcp:10.0.142.187:3121
source /tools/Xilinx/Vitis/2022.2/scripts/vitis/util/zynqmp_utils.tcl
targets -set -nocase -filter {name =~"APU*"}
rst -system
fpga -file /home/bouthsarath/acmi-backend_test/prj/zubpm_sw/zubpm/_ide/bitstream/zubpm_hw_0.0.0-17-g2216b585-WPS-171005.bit
targets -set -nocase -filter {name =~"APU*"}
loadhw -hw /home/bouthsarath/acmi-backend_test/prj/zubpm_sw/zubpm_platform/export/zubpm_platform/hw/zubpm_hw_0.0.0-17-g2216b585-WPS-171005.xsa
targets -set -nocase -filter {name =~ "*A53*#0"}
rst -processor -clear-registers
dow /home/bouthsarath/acmi-backend_test/prj/zubpm_sw/zubpm_platform/export/zubpm_platform/sw/zubpm_platform/boot/fsbl.elf
con
after 10000
stop
after 10000
targets -set -nocase -filter {name =~ "*A53*#0"}
rst -processor -clear-registers
dow /home/bouthsarath/acmi-backend_test/prj/zubpm_sw/zubpm/Debug/zubpm.elf
con
