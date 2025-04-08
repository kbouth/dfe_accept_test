--Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2022.2 (lin64) Build 3671981 Fri Oct 14 04:59:54 MDT 2022
--Date        : Mon Mar 17 11:57:22 2025
--Host        : WPS-171005 running 64-bit Ubuntu 22.04.5 LTS
--Command     : generate_target top_wrapper.bd
--Design      : top_wrapper
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity top_wrapper is
  port (
    M00_AXI_0_araddr : out STD_LOGIC_VECTOR ( 31 downto 0 );
    M00_AXI_0_arburst : out STD_LOGIC_VECTOR ( 1 downto 0 );
    M00_AXI_0_arcache : out STD_LOGIC_VECTOR ( 3 downto 0 );
    M00_AXI_0_arlen : out STD_LOGIC_VECTOR ( 7 downto 0 );
    M00_AXI_0_arlock : out STD_LOGIC_VECTOR ( 0 to 0 );
    M00_AXI_0_arprot : out STD_LOGIC_VECTOR ( 2 downto 0 );
    M00_AXI_0_arqos : out STD_LOGIC_VECTOR ( 3 downto 0 );
    M00_AXI_0_arready : in STD_LOGIC;
    M00_AXI_0_arsize : out STD_LOGIC_VECTOR ( 2 downto 0 );
    M00_AXI_0_aruser : out STD_LOGIC_VECTOR ( 15 downto 0 );
    M00_AXI_0_arvalid : out STD_LOGIC;
    M00_AXI_0_awaddr : out STD_LOGIC_VECTOR ( 31 downto 0 );
    M00_AXI_0_awburst : out STD_LOGIC_VECTOR ( 1 downto 0 );
    M00_AXI_0_awcache : out STD_LOGIC_VECTOR ( 3 downto 0 );
    M00_AXI_0_awlen : out STD_LOGIC_VECTOR ( 7 downto 0 );
    M00_AXI_0_awlock : out STD_LOGIC_VECTOR ( 0 to 0 );
    M00_AXI_0_awprot : out STD_LOGIC_VECTOR ( 2 downto 0 );
    M00_AXI_0_awqos : out STD_LOGIC_VECTOR ( 3 downto 0 );
    M00_AXI_0_awready : in STD_LOGIC;
    M00_AXI_0_awsize : out STD_LOGIC_VECTOR ( 2 downto 0 );
    M00_AXI_0_awuser : out STD_LOGIC_VECTOR ( 15 downto 0 );
    M00_AXI_0_awvalid : out STD_LOGIC;
    M00_AXI_0_bready : out STD_LOGIC;
    M00_AXI_0_bresp : in STD_LOGIC_VECTOR ( 1 downto 0 );
    M00_AXI_0_bvalid : in STD_LOGIC;
    M00_AXI_0_rdata : in STD_LOGIC_VECTOR ( 31 downto 0 );
    M00_AXI_0_rlast : in STD_LOGIC;
    M00_AXI_0_rready : out STD_LOGIC;
    M00_AXI_0_rresp : in STD_LOGIC_VECTOR ( 1 downto 0 );
    M00_AXI_0_rvalid : in STD_LOGIC;
    M00_AXI_0_wdata : out STD_LOGIC_VECTOR ( 31 downto 0 );
    M00_AXI_0_wlast : out STD_LOGIC;
    M00_AXI_0_wready : in STD_LOGIC;
    M00_AXI_0_wstrb : out STD_LOGIC_VECTOR ( 3 downto 0 );
    M00_AXI_0_wvalid : out STD_LOGIC;
    pl_clk0 : out STD_LOGIC
  );
end top_wrapper;

architecture STRUCTURE of top_wrapper is
  component top is
  port (
    pl_clk0 : out STD_LOGIC;
    M00_AXI_0_awaddr : out STD_LOGIC_VECTOR ( 31 downto 0 );
    M00_AXI_0_awlen : out STD_LOGIC_VECTOR ( 7 downto 0 );
    M00_AXI_0_awsize : out STD_LOGIC_VECTOR ( 2 downto 0 );
    M00_AXI_0_awburst : out STD_LOGIC_VECTOR ( 1 downto 0 );
    M00_AXI_0_awlock : out STD_LOGIC_VECTOR ( 0 to 0 );
    M00_AXI_0_awcache : out STD_LOGIC_VECTOR ( 3 downto 0 );
    M00_AXI_0_awprot : out STD_LOGIC_VECTOR ( 2 downto 0 );
    M00_AXI_0_awqos : out STD_LOGIC_VECTOR ( 3 downto 0 );
    M00_AXI_0_awuser : out STD_LOGIC_VECTOR ( 15 downto 0 );
    M00_AXI_0_awvalid : out STD_LOGIC;
    M00_AXI_0_awready : in STD_LOGIC;
    M00_AXI_0_wdata : out STD_LOGIC_VECTOR ( 31 downto 0 );
    M00_AXI_0_wstrb : out STD_LOGIC_VECTOR ( 3 downto 0 );
    M00_AXI_0_wlast : out STD_LOGIC;
    M00_AXI_0_wvalid : out STD_LOGIC;
    M00_AXI_0_wready : in STD_LOGIC;
    M00_AXI_0_bresp : in STD_LOGIC_VECTOR ( 1 downto 0 );
    M00_AXI_0_bvalid : in STD_LOGIC;
    M00_AXI_0_bready : out STD_LOGIC;
    M00_AXI_0_araddr : out STD_LOGIC_VECTOR ( 31 downto 0 );
    M00_AXI_0_arlen : out STD_LOGIC_VECTOR ( 7 downto 0 );
    M00_AXI_0_arsize : out STD_LOGIC_VECTOR ( 2 downto 0 );
    M00_AXI_0_arburst : out STD_LOGIC_VECTOR ( 1 downto 0 );
    M00_AXI_0_arlock : out STD_LOGIC_VECTOR ( 0 to 0 );
    M00_AXI_0_arcache : out STD_LOGIC_VECTOR ( 3 downto 0 );
    M00_AXI_0_arprot : out STD_LOGIC_VECTOR ( 2 downto 0 );
    M00_AXI_0_arqos : out STD_LOGIC_VECTOR ( 3 downto 0 );
    M00_AXI_0_aruser : out STD_LOGIC_VECTOR ( 15 downto 0 );
    M00_AXI_0_arvalid : out STD_LOGIC;
    M00_AXI_0_arready : in STD_LOGIC;
    M00_AXI_0_rdata : in STD_LOGIC_VECTOR ( 31 downto 0 );
    M00_AXI_0_rresp : in STD_LOGIC_VECTOR ( 1 downto 0 );
    M00_AXI_0_rlast : in STD_LOGIC;
    M00_AXI_0_rvalid : in STD_LOGIC;
    M00_AXI_0_rready : out STD_LOGIC
  );
  end component top;
begin
top_i: component top
     port map (
      M00_AXI_0_araddr(31 downto 0) => M00_AXI_0_araddr(31 downto 0),
      M00_AXI_0_arburst(1 downto 0) => M00_AXI_0_arburst(1 downto 0),
      M00_AXI_0_arcache(3 downto 0) => M00_AXI_0_arcache(3 downto 0),
      M00_AXI_0_arlen(7 downto 0) => M00_AXI_0_arlen(7 downto 0),
      M00_AXI_0_arlock(0) => M00_AXI_0_arlock(0),
      M00_AXI_0_arprot(2 downto 0) => M00_AXI_0_arprot(2 downto 0),
      M00_AXI_0_arqos(3 downto 0) => M00_AXI_0_arqos(3 downto 0),
      M00_AXI_0_arready => M00_AXI_0_arready,
      M00_AXI_0_arsize(2 downto 0) => M00_AXI_0_arsize(2 downto 0),
      M00_AXI_0_aruser(15 downto 0) => M00_AXI_0_aruser(15 downto 0),
      M00_AXI_0_arvalid => M00_AXI_0_arvalid,
      M00_AXI_0_awaddr(31 downto 0) => M00_AXI_0_awaddr(31 downto 0),
      M00_AXI_0_awburst(1 downto 0) => M00_AXI_0_awburst(1 downto 0),
      M00_AXI_0_awcache(3 downto 0) => M00_AXI_0_awcache(3 downto 0),
      M00_AXI_0_awlen(7 downto 0) => M00_AXI_0_awlen(7 downto 0),
      M00_AXI_0_awlock(0) => M00_AXI_0_awlock(0),
      M00_AXI_0_awprot(2 downto 0) => M00_AXI_0_awprot(2 downto 0),
      M00_AXI_0_awqos(3 downto 0) => M00_AXI_0_awqos(3 downto 0),
      M00_AXI_0_awready => M00_AXI_0_awready,
      M00_AXI_0_awsize(2 downto 0) => M00_AXI_0_awsize(2 downto 0),
      M00_AXI_0_awuser(15 downto 0) => M00_AXI_0_awuser(15 downto 0),
      M00_AXI_0_awvalid => M00_AXI_0_awvalid,
      M00_AXI_0_bready => M00_AXI_0_bready,
      M00_AXI_0_bresp(1 downto 0) => M00_AXI_0_bresp(1 downto 0),
      M00_AXI_0_bvalid => M00_AXI_0_bvalid,
      M00_AXI_0_rdata(31 downto 0) => M00_AXI_0_rdata(31 downto 0),
      M00_AXI_0_rlast => M00_AXI_0_rlast,
      M00_AXI_0_rready => M00_AXI_0_rready,
      M00_AXI_0_rresp(1 downto 0) => M00_AXI_0_rresp(1 downto 0),
      M00_AXI_0_rvalid => M00_AXI_0_rvalid,
      M00_AXI_0_wdata(31 downto 0) => M00_AXI_0_wdata(31 downto 0),
      M00_AXI_0_wlast => M00_AXI_0_wlast,
      M00_AXI_0_wready => M00_AXI_0_wready,
      M00_AXI_0_wstrb(3 downto 0) => M00_AXI_0_wstrb(3 downto 0),
      M00_AXI_0_wvalid => M00_AXI_0_wvalid,
      pl_clk0 => pl_clk0
    );
end STRUCTURE;
