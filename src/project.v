/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_dino_score (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
    wire [15:0] score_out;
    wire debug;

  ScoreModule score_mod (
    .game_start(ui_in[0]),     // pulse for starting the counter
    .game_over(ui_in[1]),      // pulse for ending the counter
    .game_tick(ui_in[2]),      // 60 Hz. end of frame pulse
    .clk(clk),            // clock
    .rst_n(rst_n),          // reset_n - low to reset
    .score(score_out),
      .debug_temp(debug)
  );

  // Assign top 8 bits to uo_out and bottom 8 bits to uio_out
assign uo_out  = debug << 8 & score_out[14:8]; // Top 8 bits
  assign uio_out = score_out[7:0];  // Bottom 8 bits

  // Set uio_oe to output mode for all 8 bits
  assign uio_oe = 8'b11111111; // Enable output mode for all uio_out pins

  // List all unused inputs to prevent warnings
    wire _unused = &{ena, clk, rst_n, 1'b0, uio_in, ui_in[7:3], score_out[15]};

endmodule
