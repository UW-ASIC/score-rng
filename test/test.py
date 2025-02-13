# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 0

    dut._log.info("test score module")
    
    # Check initial output state
    assert dut.uo_out.value == 0, "uo_out should be 0 after reset"
    assert dut.uio_out.value == 0, "uio_out should be 0 after reset"

     # Start game
    dut._log.info("Starting game")
    dut.ui_in.value = 0b00000001  # game_start pulse
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0  # Remove pulse
    await ClockCycles(dut.clk, 2)
# Generate game ticks to increment score
    for _ in range(10):  # Simulate 10 game ticks
        dut.ui_in.value = 0b00000100  # game_tick pulse
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 2)

    # Capture score after 10 ticks
    score_high = dut.uo_out.value
    score_low = dut.uio_out.value
    score = (int(score_high) << 8) | int(score_low)
    dut._log.info(f"Score after 10 ticks: {score}")

    # End game
    dut._log.info("Ending game")
    dut.ui_in.value = 0b00000010  # game_over pulse
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0  # Remove pulse
    await ClockCycles(dut.clk, 2)

    # Check final score (should remain unchanged after game_over)
    final_score_high = dut.uo_out.value
    final_score_low = dut.uio_out.value
    final_score = (int(final_score_high) << 8) | int(final_score_low)
    
    assert final_score == score, "Score should not change after game over"
    dut._log.info(f"Final score after game over: {final_score}")

    dut._log.info("Test completed successfully!")
