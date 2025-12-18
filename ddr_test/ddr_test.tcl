# Absolute path to this script's directory
set SCRIPT_DIR [file dirname [file normalize [info script]]]

puts "Running from: $SCRIPT_DIR"

connect -url tcp:10.0.142.173:3121

targets -set -nocase -filter {name =~ "APU*"}
rst -system
after 3000

targets -set -nocase -filter {name =~ "APU*"}
loadhw \
  -hw [file join $SCRIPT_DIR ddr_test.xsa] \
  -mem-ranges [list \
    {0x80000000 0xbfffffff} \
    {0x400000000 0x5ffffffff} \
    {0x1000000000 0x7fffffffff}] \
  -regs

configparams force-mem-access 1

targets -set -nocase -filter {name =~ "APU*"}
source [file join $SCRIPT_DIR psu_init.tcl]
psu_init
catch {psu_protection}

targets -set -nocase -filter {name =~ "*A53*#0"}
rst -processor

dow [file join $SCRIPT_DIR ddr_test.elf]

configparams force-mem-access 0

targets -set -nocase -filter {name =~ "*A53*#0"}
con

