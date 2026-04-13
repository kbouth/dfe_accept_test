open_hw_manager

# Read JTAG IP from shared config file
set CFG_FILE [file join [file dirname [file normalize [info script]]] .. jtag_ip.cfg]
set fp [open $CFG_FILE r]
set JTAG_IP [string trim [read $fp]]
close $fp
puts "Connecting to JTAG: $JTAG_IP"

connect_hw_server -url ${JTAG_IP}:3121
open_hw_target

# Get device
set dev [lindex [get_hw_devices] 0]
current_hw_device $dev
refresh_hw_device $dev

# ----------------------------
# Find prj directory
# ----------------------------

set base_dir [pwd]
set prj_root [file join $base_dir]

if {![file exists $prj_root]} {
    error "ERROR: prj directory not found at: $prj_root"
}

puts "Project root: $prj_root"

# ----------------------------
# Build paths
# ----------------------------

set bitfile [file join $prj_root ibert_test.bit]
set ltxfile [file join $prj_root ibert_test.ltx]

puts "BIT: $bitfile"
puts "LTX: $ltxfile"

# ----------------------------
# Program FPGA
# ----------------------------

set_property PROGRAM.FILE $bitfile $dev
set_property FULL_PROBES.FILE $ltxfile $dev

program_hw_devices $dev
puts "FPGA PROGRAMMED"

# ----------------------------
# Cleanup
# ----------------------------

close_hw_manager
exit

