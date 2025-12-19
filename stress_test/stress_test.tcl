set SCRIPT_DIR [file dirname [file normalize [info script]]]
puts "Running from: $SCRIPT_DIR"

connect -path [list tcp::1534 tcp:10.0.142.173:3121]


targets -set -nocase -filter {name =~"APU*"}
rst -system 
after 3000
fpga -file [file join $SCRIPT_DIR zubpm_stress.bit]

targets -set -nocase -filter {name =~"APU*"}

loadhw -hw [file join $SCRIPT_DIR stress_test.xsa] \
       -mem-ranges [list \
		    {0x80000000 0xbfffffff} \
		    {0x400000000 0x5ffffffff} \
		    {0x1000000000 0x7fffffffff}] \
       -regs
       
configparams force-mem-access 1
targets -set -nocase -filter {name =~"APU*"}
set mode [expr [mrd -value 0xFF5E0200] & 0xf]
targets -set -nocase -filter {name =~ "*A53*#0"}
rst -processor
dow [file join $SCRIPT_DIR stress_fsbl.elf]
set bp_25_5_fsbl_bp [bpadd -addr &XFsbl_Exit]
con -block -timeout 60
bpremove $bp_25_5_fsbl_bp
targets -set -nocase -filter {name =~ "*A53*#0"}
rst -processor
dow [file join $SCRIPT_DIR zubpm_stress.elf]
configparams force-mem-access 0
targets -set -nocase -filter {name =~ "*A53*#0"}
con
