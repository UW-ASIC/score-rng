/*
 * Copyright (c) 2025 UW ASIC
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module score (
    input  wire              game_start,     // pulse for starting the counter
    input  wire              game_over,      // pulse for ending the counter
    input  wire              game_tick,      // 60 Hz. end of frame pulse
    input  wire              clk,            // clock
    input  wire              rst_n,          // reset_n - low to reset
    output reg [15:0]        score
);

  // Internal registers to help with keeping track of the score in decimal
  reg [3:0] score_int [3:0];
  reg game_active = 1'b0;

  // determine if game_active
  always @(posedge game_start or posedge game_over or negedge rst_n) begin
    if (!rst_n) begin
      game_active <= 1'b0;
    end else begin
      if (game_start)
        game_active <= 1'b1;
      else if (game_over)
        game_active <= 1'b0;
    end
  end

  // at the posedge of the gametick, increment the score by 1.
  always @(posedge game_tick or negedge rst_n) begin
    if (!rst_n) begin
      score_int[0] <= 0;
      score_int[1] <= 0;
      score_int[2] <= 0;
      score_int[3] <= 0;
    end else if (game_active) begin
      if (score_int[0] == 9) begin
        if (score_int[1] == 9) begin
          if (score_int[2] == 9) begin
            if (score_int[3] == 9) begin
              // Reset the game if the score gets to 9999
              score_int[0] <= 0;
              score_int[1] <= 0;
              score_int[2] <= 0;
              score_int[3] <= 0;
            end else begin
              score_int[3] = score_int[3] + 1;
            end
          end else begin
            score_int[2] = score_int[2] + 1;
          end
        end else begin
          score_int[1] = score_int[1] + 1;
        end
      end else begin
        score_int[0] = score_int[0] + 1;
      end
    end
  
  end

// List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};
  
  assign score = {score_int[3], score_int[2], score_int[1], score_int[0]};

endmodule
