/*
 * Copyright (c) 2025 UW ASIC
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module score (
    input  wire       game_start,
    input  wire       game_over,
    input  wire       clk,      // clock
    input  wire       rst_n,     // reset_n - low to reset
    output reg [15:0]        score
);

  // Internal registers to help with keeping track of the score in decimal
  reg [3:0] score_int [3:0];
  reg [15:0] counter;

  always @(negedge rst_n) begin
    if (!rst_n) begin
        counter <= 0;
        score_int[0] <= 0;
        score_int[1] <= 0;
        score_int[2] <= 0;
        score_int[3] <= 0;
    end
  

  
  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
