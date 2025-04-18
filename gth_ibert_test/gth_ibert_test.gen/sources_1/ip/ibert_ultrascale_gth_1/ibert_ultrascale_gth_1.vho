-- (c) Copyright 1995-2025 Xilinx, Inc. All rights reserved.
-- 
-- This file contains confidential and proprietary information
-- of Xilinx, Inc. and is protected under U.S. and
-- international copyright and other intellectual property
-- laws.
-- 
-- DISCLAIMER
-- This disclaimer is not a license and does not grant any
-- rights to the materials distributed herewith. Except as
-- otherwise provided in a valid license issued to you by
-- Xilinx, and to the maximum extent permitted by applicable
-- law: (1) THESE MATERIALS ARE MADE AVAILABLE "AS IS" AND
-- WITH ALL FAULTS, AND XILINX HEREBY DISCLAIMS ALL WARRANTIES
-- AND CONDITIONS, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING
-- BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, NON-
-- INFRINGEMENT, OR FITNESS FOR ANY PARTICULAR PURPOSE; and
-- (2) Xilinx shall not be liable (whether in contract or tort,
-- including negligence, or under any other theory of
-- liability) for any loss or damage of any kind or nature
-- related to, arising under or in connection with these
-- materials, including for any direct, or any indirect,
-- special, incidental, or consequential loss or damage
-- (including loss of data, profits, goodwill, or any type of
-- loss or damage suffered as a result of any action brought
-- by a third party) even if such damage or loss was
-- reasonably foreseeable or Xilinx had been advised of the
-- possibility of the same.
-- 
-- CRITICAL APPLICATIONS
-- Xilinx products are not designed or intended to be fail-
-- safe, or for use in any application requiring fail-safe
-- performance, such as life-support or safety devices or
-- systems, Class III medical devices, nuclear facilities,
-- applications related to the deployment of airbags, or any
-- other applications that could lead to death, personal
-- injury, or severe property or environmental damage
-- (individually and collectively, "Critical
-- Applications"). Customer assumes the sole risk and
-- liability of any use of Xilinx products in Critical
-- Applications, subject only to applicable laws and
-- regulations governing limitations on product liability.
-- 
-- THIS COPYRIGHT NOTICE AND DISCLAIMER MUST BE RETAINED AS
-- PART OF THIS FILE AT ALL TIMES.
-- 
-- DO NOT MODIFY THIS FILE.
-- IP VLNV: xilinx.com:ip:ibert_ultrascale_gth:1.4
-- IP Revision: 10

-- The following code must appear in the VHDL architecture header.

------------- Begin Cut here for COMPONENT Declaration ------ COMP_TAG
COMPONENT ibert_ultrascale_gth_1
  PORT (
    txn_o : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
    txp_o : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
    rxoutclk_o : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
    rxn_i : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
    rxp_i : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
    gtrefclk0_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtrefclk1_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtnorthrefclk0_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtnorthrefclk1_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtsouthrefclk0_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtsouthrefclk1_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtrefclk00_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtrefclk10_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtrefclk01_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtrefclk11_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtnorthrefclk00_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtnorthrefclk10_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtnorthrefclk01_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtnorthrefclk11_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtsouthrefclk00_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtsouthrefclk10_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtsouthrefclk01_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    gtsouthrefclk11_i : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
    clk : IN STD_LOGIC 
  );
END COMPONENT;
-- COMP_TAG_END ------ End COMPONENT Declaration ------------

-- The following code must appear in the VHDL architecture
-- body. Substitute your own instance name and net names.

------------- Begin Cut here for INSTANTIATION Template ----- INST_TAG
your_instance_name : ibert_ultrascale_gth_1
  PORT MAP (
    txn_o => txn_o,
    txp_o => txp_o,
    rxoutclk_o => rxoutclk_o,
    rxn_i => rxn_i,
    rxp_i => rxp_i,
    gtrefclk0_i => gtrefclk0_i,
    gtrefclk1_i => gtrefclk1_i,
    gtnorthrefclk0_i => gtnorthrefclk0_i,
    gtnorthrefclk1_i => gtnorthrefclk1_i,
    gtsouthrefclk0_i => gtsouthrefclk0_i,
    gtsouthrefclk1_i => gtsouthrefclk1_i,
    gtrefclk00_i => gtrefclk00_i,
    gtrefclk10_i => gtrefclk10_i,
    gtrefclk01_i => gtrefclk01_i,
    gtrefclk11_i => gtrefclk11_i,
    gtnorthrefclk00_i => gtnorthrefclk00_i,
    gtnorthrefclk10_i => gtnorthrefclk10_i,
    gtnorthrefclk01_i => gtnorthrefclk01_i,
    gtnorthrefclk11_i => gtnorthrefclk11_i,
    gtsouthrefclk00_i => gtsouthrefclk00_i,
    gtsouthrefclk10_i => gtsouthrefclk10_i,
    gtsouthrefclk01_i => gtsouthrefclk01_i,
    gtsouthrefclk11_i => gtsouthrefclk11_i,
    clk => clk
  );
-- INST_TAG_END ------ End INSTANTIATION Template ---------

-- You must compile the wrapper file ibert_ultrascale_gth_1.vhd when simulating
-- the core, ibert_ultrascale_gth_1. When compiling the wrapper file, be sure to
-- reference the VHDL simulation library.



