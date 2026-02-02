# GP1294AI VFD Display Driver for MicroPython

A MicroPython driver for Chinese VFD (Vacuum Fluorescent Display) modules using the GP1294AI controller, designed for the RP2040 microcontroller.

## Display Specifications

| Parameter | Value |
|-----------|-------|
| Visible Resolution | 256 x 48 pixels |
| GRAM Memory | 512 columns x 8 bytes (4096 bytes) |
| Memory Mapping | 2 GRAM columns = 1 physical pixel |
| Column Layout | 8 bytes per column (64 vertical pixels, bytes 0-5 visible) |
| Controller | GP1294AI |

## Hardware Wiring

### Default Pin Configuration (RP2040 Zero)

| GPIO | Signal | Description |
|------|--------|-------------|
| GP0 | FIL_EN | Filament Enable (Active High) |
| GP1 | CS# | Chip Select (Active Low) |
| GP2 | SCK | SPI Clock |
| GP3 | MOSI | SPI Data (TX) |
| GP4 | RST# | Hardware Reset (Active Low) |
| GND | GND | Ground |
| VBUS | +5V | Power Supply |

### Connection Notes

- The VFD module requires +5V power for the filament
- All logic signals are directly connected (no level shifting required for 3.3V RP2040)
- The filament enable pin must be driven high for the display to illuminate

## SPI Protocol

| Parameter | Value |
|-----------|-------|
| SPI Mode | Mode 3 (CPOL=1, CPHA=1) |
| Bit Order | LSB-first (handled by driver via bit reversal) |
| Default Speed | 500 kHz |

The RP2040's hardware SPI does not support LSB-first transmission natively. The driver includes a pre-computed bit reversal lookup table for efficient conversion.

## Memory Layout

### GRAM Structure

The display GRAM is organized as 512 columns, each containing 8 bytes (64 vertical pixels):

```
GRAM Column 0:  [Byte 0][Byte 1][Byte 2][Byte 3][Byte 4][Byte 5][Byte 6][Byte 7]
GRAM Column 1:  [Byte 0][Byte 1][Byte 2][Byte 3][Byte 4][Byte 5][Byte 6][Byte 7]
...
GRAM Column 511: [Byte 0][Byte 1][Byte 2][Byte 3][Byte 4][Byte 5][Byte 6][Byte 7]
```

- Bytes 0-5 (48 pixels) are visible on the physical display
- Bytes 6-7 (16 pixels) are in the non-visible GRAM area
- Each byte contains 8 vertical pixels, LSB at top

### Physical to GRAM Mapping

Two GRAM columns correspond to one physical pixel column:
- Physical pixel at (x, y) maps to GRAM columns (x*2) and (x*2+1)
- Both GRAM columns must be written with the same data

### Memory Addressing

For a physical pixel at coordinates (x, y):
```
gram_column = x * 2
byte_index = y // 8
bit_index = y % 8
gram_offset = gram_column * 8 + byte_index
```

## Command Reference

| Command | Byte | Description |
|---------|------|-------------|
| RESET | 0xAA | Software reset |
| BRIGHTNESS | 0xA0 | Set brightness (followed by 2 bytes) |
| DISPLAY_MODE | 0x80 | Set display mode |
| WRITE_GRAM | 0xF0 | Write to GRAM (followed by x, y, data) |
| DISPLAY_OFFSET | 0xC0 | Set display offset (x, y) |
| VFD_MODE | 0xCC | Configure VFD parameters (7 bytes follow) |
| OSC_SETTING | 0x78 | Oscillator configuration |
| ENTER_STANDBY | 0x61 | Enter power-saving mode |
| EXIT_STANDBY | 0x6D | Exit power-saving mode |

### Initialization Sequence

1. Hardware reset (RST# low for 10ms, then high)
2. Software reset (0xAA)
3. VFD mode configuration (0xCC, 0x01, 0x1F, 0x00, 0xFF, 0x3F, 0x00, 0x20)
4. Set brightness
5. Clear GRAM
6. Set display offset (0xC0, 0x00, 0x38)
7. Set display mode (0x80, 0x00)
8. Configure oscillator (0x78, 0x08)
9. Enable filament

## Usage

### Basic Example

```python
from vfd_framebuffer import VFDFramebuffer
import time

# Initialize display with default pins
vfd = VFDFramebuffer()
vfd.init()

# Draw some graphics
vfd.fill(0)  # Clear screen
vfd.text("Hello VFD!", 10, 10, 1)
vfd.rect(0, 0, 256, 48, 1)  # Border
vfd.show()  # Update display
```

### Available Drawing Methods

The `VFDFramebuffer` class inherits from MicroPython's `framebuf.FrameBuffer` and provides:

| Method | Description |
|--------|-------------|
| `fill(c)` | Fill entire buffer (0=off, 1=on) |
| `pixel(x, y, c)` | Set single pixel |
| `hline(x, y, w, c)` | Horizontal line |
| `vline(x, y, h, c)` | Vertical line |
| `line(x1, y1, x2, y2, c)` | Line between two points |
| `rect(x, y, w, h, c)` | Rectangle outline |
| `fill_rect(x, y, w, h, c)` | Filled rectangle |
| `text(string, x, y, c)` | Text string (8x8 font) |
| `scroll(xstep, ystep)` | Scroll buffer contents |
| `blit(fbuf, x, y)` | Copy another framebuffer |

Additional methods provided by VFDFramebuffer:

| Method | Description |
|--------|-------------|
| `show()` | Transfer buffer to display |
| `clear()` | Clear and update display |
| `draw_circle(cx, cy, r, c)` | Circle outline |
| `fill_circle(cx, cy, r, c)` | Filled circle |
| `draw_progress_bar(x, y, w, h, progress, c)` | Progress bar (0.0-1.0) |
| `center_text(text, y, c)` | Horizontally centered text |
| `draw_bitmap(x, y, bitmap, w, h, c)` | Bitmap image |
| `invert()` | Invert all pixels |
| `set_brightness(level)` | Set display brightness (0-255) |
| `filament_on()` / `filament_off()` | Control filament |
| `standby(enable)` | Enter/exit standby mode |

### Custom Pin Configuration

```python
vfd = VFDFramebuffer(
    spi_id=0,
    sck_pin=2,
    mosi_pin=3,
    cs_pin=1,
    rst_pin=4,
    fil_en_pin=0,
    baudrate=500000
)
```

### Direct GRAM Access

For advanced usage, access the low-level driver:

```python
# Access underlying GP1294AI driver
driver = vfd.display

# Write raw GRAM data
driver.write_gram(data_bytes, x_start=0, y_start=0)
```

## File Structure

| File | Description |
|------|-------------|
| `gp1294ai.py` | Low-level hardware driver |
| `vfd_framebuffer.py` | High-level framebuffer interface |
| `main.py` | Demo application |

## Hardware Compatibility

Tested with:
- RP2040 Zero (Waveshare)
- Chinese VFD module with GP1294AI controller (256x48 visible pixels)

## License

MIT License
