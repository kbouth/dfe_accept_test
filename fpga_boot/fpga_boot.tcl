set SCRIPT_DIR [file dirname [file normalize [info script]]]
puts "Running from: $SCRIPT_DIR"

# Read JTAG IP from shared config file
set CFG_FILE [file join $SCRIPT_DIR .. jtag_ip.cfg]
set fp [open $CFG_FILE r]
set JTAG_IP [string trim [read $fp]]
close $fp
puts "Connecting to JTAG: $JTAG_IP"

connect -url tcp:${JTAG_IP}:3121

targets -set -nocase -filter {name =~"APU*"}
rst -system 
after 3000
fpga -file [file join $SCRIPT_DIR zubpm_hw.bit]

targets -set -nocase -filter {name =~"APU*"}

loadhw -hw [file join $SCRIPT_DIR zubpm_hw.xsa] \
       -mem-ranges [list \
		    {0x80000000 0xbfffffff} \
		    {0x400000000 0x5ffffffff} \
		    {0x1000000000 0x7fffffffff}] \
       -regs
       
configparams force-mem-access 1
targets -set -nocase -filter {name =~"APU*"}
set mode [expr [mrd -value 0xFF5E0200] & 0xf]
targets -set -nocase -filter {name =~ "*A53*#0"}
rst -processor -clear-registers

dow [file join $SCRIPT_DIR fsbl.elf]
con
after 5000
stop
targets -set -nocase -filter {name =~ "*A53*#0"}
rst -processor -clear-registers

dow [file join $SCRIPT_DIR zubpm.elf]
configparams force-mem-access 0
targets -set -nocase -filter {name =~ "*A53*#0"}
con
