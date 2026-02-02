"""
VFD Display Demo for RP2040

Demonstrates the GP1294AI VFD display driver with various
graphical effects, animations, and text rendering.

Run this file directly to start the demo loop.
"""

from vfd_framebuffer import VFDFramebuffer
import time


def demo_text(vfd):
    """Demonstrate text rendering."""
    vfd.fill(0)
    # Left column
    vfd.text("GP1294AI", 0, 0, 1)
    vfd.text("256x48px", 0, 12, 1)
    vfd.text("VFD", 0, 24, 1)
    vfd.text("Display", 0, 36, 1)
    # Right column
    vfd.text("RP2040", 180, 0, 1)
    vfd.text("Zero", 180, 12, 1)
    vfd.text("Micro", 180, 24, 1)
    vfd.text("Python", 180, 36, 1)
    # Center message
    vfd.text("FLUORITE", 88, 20, 1)
    vfd.show()
    time.sleep(2)


def demo_graphics(vfd):
    """Demonstrate graphics primitives."""
    vfd.fill(0)
    
    # Border around entire screen
    vfd.rect(0, 0, 256, 48, 1)
    
    # Left: nested rectangles
    vfd.rect(5, 5, 40, 38, 1)
    vfd.rect(10, 10, 30, 28, 1)
    vfd.fill_rect(15, 15, 20, 18, 1)
    
    # Center-left: circle outline
    vfd.draw_circle(75, 24, 18, 1)
    
    # Center: filled circle
    vfd.fill_circle(120, 24, 15, 1)
    
    # Center-right: diagonal cross
    vfd.line(145, 5, 185, 42, 1)
    vfd.line(145, 42, 185, 5, 1)
    
    # Right: horizontal and vertical lines
    for i in range(5):
        vfd.hline(200, 4 + i * 10, 50, 1)
    for i in range(6):
        vfd.vline(200 + i * 10, 4, 41, 1)  # height=41 to reach y=45
    
    vfd.show()
    time.sleep(2)


def demo_progress_bar(vfd):
    """Demonstrate animated progress bar."""
    vfd.fill(0)
    vfd.text("Loading...", 0, 0, 1)
    vfd.show()
    
    # Animate progress bar
    for i in range(101):
        vfd.fill_rect(0, 20, 256, 20, 0)  # Clear progress bar area
        vfd.fill_rect(100, 8, 48, 10, 0)  # Clear percentage text area
        vfd.draw_progress_bar(10, 25, 236, 15, i / 100.0, 1)
        vfd.text(f"{i:3d}%", 110, 8, 1)
        vfd.show()
        time.sleep_ms(30)
    
    time.sleep(1)


def demo_scroll(vfd):
    """Demonstrate scrolling text."""
    message = "    Welcome to the GP1294AI VFD Display Demo!    "
    
    vfd.fill(0)
    vfd.text("Scrolling:", 0, 0, 1)
    vfd.show()
    
    # Scroll the message
    for offset in range(len(message) * 8):
        vfd.fill_rect(0, 20, 256, 20, 0)  # Clear scroll area
        
        # Calculate visible portion
        char_offset = offset // 8
        pixel_offset = offset % 8
        
        visible_text = message[char_offset:char_offset + 32]
        vfd.text(visible_text, -pixel_offset, 24, 1)
        vfd.show()
        time.sleep_ms(50)


def demo_invert(vfd):
    """Demonstrate display inversion."""
    vfd.fill(0)
    vfd.center_text("Invert Demo", 20)
    vfd.show()
    time.sleep(1)
    
    for _ in range(6):
        vfd.invert()
        vfd.show()
        time.sleep_ms(500)


def demo_brightness(vfd):
    """Demonstrate brightness control."""
    vfd.fill(0)
    vfd.center_text("Brightness", 10)
    vfd.show()
    
    # Fade out
    for b in range(40, 0, -1):
        vfd.set_brightness(b)
        vfd.fill_rect(0, 30, 256, 8, 0)  # Clear text area
        vfd.center_text(f"Level: {b:3d}", 30)
        vfd.show()
        time.sleep_ms(50)
    
    # Fade in
    for b in range(0, 41):
        vfd.set_brightness(b)
        vfd.fill_rect(0, 30, 256, 8, 0)  # Clear text area
        vfd.center_text(f"Level: {b:3d}", 30)
        vfd.show()
        time.sleep_ms(50)
    
    time.sleep(1)


def demo_animation(vfd):
    """Demonstrate simple animation."""
    # Bouncing ball animation with trail
    x, y = 30, 24
    dx, dy = 4, 3
    radius = 6
    
    for frame in range(200):
        vfd.fill(0)
        
        # Draw border around full screen
        vfd.rect(0, 0, 256, 48, 1)
        
        # Draw corner markers
        vfd.fill_rect(2, 2, 4, 4, 1)
        vfd.fill_rect(250, 2, 4, 4, 1)
        vfd.fill_rect(2, 42, 4, 4, 1)
        vfd.fill_rect(250, 42, 4, 4, 1)
        
        # Draw ball
        vfd.fill_circle(int(x), int(y), radius, 1)
        
        # Draw frame counter on right side
        vfd.text(f"{frame:03d}", 210, 20, 1)
        
        # Update position
        x += dx
        y += dy
        
        # Bounce off walls (with border margin)
        if x <= radius + 2 or x >= 254 - radius:
            dx = -dx
        if y <= radius + 2 or y >= 46 - radius:
            dy = -dy
        
        vfd.show()
        time.sleep_ms(25)


def demo_pattern(vfd):
    """Demonstrate pattern drawing."""
    # First: Full screen border test
    vfd.fill(0)
    vfd.rect(0, 0, 256, 48, 1)  # Outer border
    vfd.rect(2, 2, 252, 44, 1)  # Inner border
    vfd.text("FULL SCREEN", 88, 10, 1)
    vfd.text("256 x 48", 96, 25, 1)
    # Draw corner dots at extremes
    vfd.pixel(0, 0, 1)
    vfd.pixel(255, 0, 1)
    vfd.pixel(0, 47, 1)
    vfd.pixel(255, 47, 1)
    vfd.show()
    time.sleep(2)
    
    # Draw checkerboard pattern across full width
    vfd.fill(0)
    for y in range(0, 48, 8):
        for x in range(0, 256, 8):
            if (x // 8 + y // 8) % 2 == 0:
                vfd.fill_rect(x, y, 8, 8, 1)
    vfd.show()
    time.sleep(2)
    
    # Draw vertical stripes across full width
    vfd.fill(0)
    for x in range(0, 256, 4):
        if (x // 4) % 2 == 0:
            vfd.vline(x, 0, 48, 1)
            vfd.vline(x + 1, 0, 48, 1)
    vfd.show()
    time.sleep(2)
    
    # Horizontal gradient bars from both edges
    vfd.fill(0)
    for y in range(0, 48, 8):
        width = 32 + y * 4  # Increasing width bars
        vfd.fill_rect(0, y, width, 6, 1)
        vfd.fill_rect(256 - width, y, width, 6, 1)
    vfd.show()
    time.sleep(2)


def run_demo():
    """Run the complete demo sequence."""
    print("Initializing VFD display...")
    
    # Create framebuffer with default pins
    vfd = VFDFramebuffer(
        spi_id=0,
        sck_pin=2,
        mosi_pin=3,
        cs_pin=1,
        rst_pin=4,
        fil_en_pin=0,
        baudrate=500000
    )
    
    # Initialize display
    vfd.init()
    print("VFD initialized!")
    
    try:
        while True:
            print("Demo: Text")
            demo_text(vfd)
            
            print("Demo: Graphics")
            demo_graphics(vfd)
            
            print("Demo: Progress Bar")
            demo_progress_bar(vfd)
            
            print("Demo: Scrolling")
            demo_scroll(vfd)
            
            print("Demo: Invert")
            demo_invert(vfd)
            
            print("Demo: Brightness")
            demo_brightness(vfd)
            
            print("Demo: Animation")
            demo_animation(vfd)
            
            print("Demo: Pattern")
            demo_pattern(vfd)
            
            print("Demo cycle complete, restarting...")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nDemo stopped by user")
    finally:
        vfd.fill(0)
        vfd.center_text("Goodbye!", 20)
        vfd.show()
        time.sleep(1)
        vfd.deinit()
        print("Display deinitialized")


# Run demo when executed directly
if __name__ == "__main__":
    run_demo()
