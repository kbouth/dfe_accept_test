onbreak {quit -force}
onerror {quit -force}

asim +access +r +m+ibert_ultrascale_gth_1  -L xilinx_vip -L xpm -L xil_defaultlib -L xilinx_vip -L unisims_ver -L unimacro_ver -L secureip -O5 xil_defaultlib.ibert_ultrascale_gth_1 xil_defaultlib.glbl

set NumericStdNoWarnings 1
set StdArithNoWarnings 1

do {wave.do}

view wave
view structure

do {ibert_ultrascale_gth_1.udo}

run

endsim

quit -force
