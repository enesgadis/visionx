#!/usr/bin/env python3
"""
Test script for WCAG Contrast Checker with a sample screenshot.
Creates a synthetic mobile UI screenshot for testing.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def create_test_screenshot():
    """Create a synthetic mobile UI screenshot with various contrast issues."""
    
    # Create a 375x812 image (iPhone X size)
    width, height = 375, 812
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_normal = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header (dark blue background, white text - should PASS)
    draw.rectangle([(0, 0), (width, 80)], fill='#1E3A8A')
    draw.text((20, 30), "My Mobile App", fill='#FFFFFF', font=font_large)
    
    # Good contrast example (black on white - should PASS AA and AAA)
    draw.rectangle([(20, 100), (width-20, 180)], fill='#FFFFFF', outline='#E5E7EB')
    draw.text((30, 120), "Good Contrast: Black on White", fill='#000000', font=font_normal)
    draw.text((30, 145), "Contrast ratio: 21:1", fill='#374151', font=font_small)
    
    # Bad contrast example (light gray on white - should FAIL)
    draw.rectangle([(20, 200), (width-20, 280)], fill='#FFFFFF', outline='#E5E7EB')
    draw.text((30, 220), "Bad Contrast: Light Gray", fill='#D1D5DB', font=font_normal)
    draw.text((30, 245), "Contrast ratio: ~1.5:1", fill='#D1D5DB', font=font_small)
    
    # Moderate contrast (should PASS AA but FAIL AAA)
    draw.rectangle([(20, 300), (width-20, 380)], fill='#F3F4F6')
    draw.text((30, 320), "Moderate Contrast", fill='#6B7280', font=font_normal)
    draw.text((30, 345), "Contrast ratio: ~4.6:1", fill='#6B7280', font=font_small)
    
    # Button with good contrast
    draw.rectangle([(20, 400), (width-20, 460)], fill='#10B981')
    draw.text((30, 420), "Submit Button", fill='#FFFFFF', font=font_normal)
    
    # Button with poor contrast (yellow on white - should FAIL)
    draw.rectangle([(20, 480), (width-20, 540)], fill='#FEF3C7')
    draw.text((30, 500), "Warning Button", fill='#FDE047', font=font_normal)
    
    # Dark theme example (good)
    draw.rectangle([(20, 560), (width-20, 640)], fill='#1F2937')
    draw.text((30, 580), "Dark Theme Text", fill='#F9FAFB', font=font_normal)
    draw.text((30, 605), "High contrast on dark", fill='#E5E7EB', font=font_small)
    
    # Footer
    draw.rectangle([(0, height-60), (width, height)], fill='#F9FAFB')
    draw.text((20, height-40), "Footer: Copyright 2026", fill='#9CA3AF', font=font_small)
    
    # Save
    output_dir = Path('test_screenshots')
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / 'sample_mobile_ui.png'
    img.save(output_path)
    
    print(f"Test screenshot created: {output_path}")
    print(f"Size: {width}x{height}px")
    print("\nExpected results:")
    print("- Header (white on dark blue): PASS AA & AAA")
    print("- Black on white: PASS AA & AAA")
    print("- Light gray on white: FAIL AA & AAA")
    print("- Gray on light gray: PASS AA, FAIL AAA")
    print("- White on green button: PASS AA & AAA")
    print("- Yellow on cream: FAIL AA & AAA")
    print("- White on dark gray: PASS AA & AAA")
    print("- Gray on light footer: May vary (~3.5:1)")
    
    return output_path


if __name__ == "__main__":
    screenshot_path = create_test_screenshot()
    print(f"\nNow run: python wcag_contrast_checker.py {screenshot_path}")
