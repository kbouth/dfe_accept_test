connect -url tcp:10.0.142.173:3121
targets -set -nocase -filter {name =~"APU*"}
rst -system
after 3000
targets -set -nocase -filter {name =~"APU*"}
loadhw -hw /home/bouthsarath/dfe_accept_test/ddr_test/ddr_test.xsa -mem-ranges [list {0x80000000 0xbfffffff} {0x400000000 0x5ffffffff} {0x1000000000 0x7fffffffff}] -regs
configparams force-mem-access 1
targets -set -nocase -filter {name =~"APU*"}
source /home/bouthsarath/dfe_accept_test/ddr_test/psu_init.tcl
psu_init
catch {psu_protection}
targets -set -nocase -filter {name =~ "*A53*#0"}
rst -processor
dow /home/bouthsarath/dfe_accept_test/ddr_test/ddr_test.elf
configparams force-mem-access 0
targets -set -nocase -filter {name =~ "*A53*#0"}
con
