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

    # Start game with longer pulse
    dut._log.info("Starting game")
    dut.ui_in.value = 0b00000001  # game_start pulse
    await ClockCycles(dut.clk, 5)
    dut.ui_in.value = 0  # Remove pulse
    await ClockCycles(dut.clk, 10)

    # Generate 60 game ticks (1 every 16667 clock cycles to match 60Hz)
    for i in range(60):
        dut.ui_in.value = 0b00000100  # game_tick pulse
        await ClockCycles(dut.clk, 5)  # Longer pulse
        dut.ui_in.value = 0
        dut._log.info(f"game_active: {dut.uo_out.value & 0x80}")
        await ClockCycles(dut.clk, 16662)  # Wait for next 60Hz tick

    # Capture score after 60 ticks
    score_high = dut.uo_out.value
    score_low = dut.uio_out.value
    score = (int(score_high) << 8) | int(score_low)
    dut._log.info(f"Score after 60 ticks: {score} - bottom: {score_low} - top: {score_high}")

    # End game with longer pulse
    dut._log.info("Ending game")
    dut.ui_in.value = 0b00000010  # game_over pulse
    await ClockCycles(dut.clk, 5)
    dut.ui_in.value = 0  # Remove pulse
    await ClockCycles(dut.clk, 10)

    assert 58 < score and score < 62

    # Check final score (should remain unchanged after game_over)
    final_score_high = dut.uo_out.value
    final_score_low = dut.uio_out.value
    final_score = (int(final_score_high) << 8) | int(final_score_low)
    
    assert final_score == score, "Score should not change after game over"
    dut._log.info(f"Final score after game over: {final_score}")

    dut._log.info("Test completed successfully!")
