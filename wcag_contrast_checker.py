#!/usr/bin/env python3
"""
VisionUX - WCAG Contrast Checker
Analyzes mobile screenshots for text-background contrast compliance.

Input: PNG screenshot
Output: Detected text-background color pairs with WCAG AA/AAA compliance status
"""

import sys
from pathlib import Path
from typing import List, Tuple, Dict
import numpy as np
from PIL import Image
import easyocr
import colorsys


class WCAGContrastChecker:
    """WCAG 2.1 contrast ratio calculator and compliance checker."""
    
    # WCAG 2.1 minimum contrast ratios
    WCAG_AA_NORMAL = 4.5
    WCAG_AA_LARGE = 3.0
    WCAG_AAA_NORMAL = 7.0
    WCAG_AAA_LARGE = 4.5
    
    @staticmethod
    def rgb_to_relative_luminance(rgb: Tuple[int, int, int]) -> float:
        """
        Calculate relative luminance according to WCAG 2.1 formula.
        
        Args:
            rgb: RGB color tuple (0-255 range)
            
        Returns:
            Relative luminance (0.0-1.0)
        """
        def normalize_channel(channel: int) -> float:
            """Normalize and linearize a single color channel."""
            c = channel / 255.0
            if c <= 0.03928:
                return c / 12.92
            else:
                return ((c + 0.055) / 1.055) ** 2.4
        
        r, g, b = rgb
        R = normalize_channel(r)
        G = normalize_channel(g)
        B = normalize_channel(b)
        
        return 0.2126 * R + 0.7152 * G + 0.0722 * B
    
    @staticmethod
    def calculate_contrast_ratio(color1: Tuple[int, int, int], 
                                 color2: Tuple[int, int, int]) -> float:
        """
        Calculate contrast ratio between two colors.
        
        Args:
            color1: First RGB color tuple
            color2: Second RGB color tuple
            
        Returns:
            Contrast ratio (1.0-21.0)
        """
        l1 = WCAGContrastChecker.rgb_to_relative_luminance(color1)
        l2 = WCAGContrastChecker.rgb_to_relative_luminance(color2)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    @staticmethod
    def check_compliance(contrast_ratio: float, is_large_text: bool = False) -> Dict[str, bool]:
        """
        Check WCAG AA and AAA compliance.
        
        Args:
            contrast_ratio: Calculated contrast ratio
            is_large_text: Whether text is large (18pt+ or 14pt+ bold)
            
        Returns:
            Dict with AA and AAA pass/fail status
        """
        if is_large_text:
            aa_pass = contrast_ratio >= WCAGContrastChecker.WCAG_AA_LARGE
            aaa_pass = contrast_ratio >= WCAGContrastChecker.WCAG_AAA_LARGE
        else:
            aa_pass = contrast_ratio >= WCAGContrastChecker.WCAG_AA_NORMAL
            aaa_pass = contrast_ratio >= WCAGContrastChecker.WCAG_AAA_NORMAL
        
        return {
            'AA': aa_pass,
            'AAA': aaa_pass
        }


class ScreenshotAnalyzer:
    """Analyzes screenshots for text elements and their background colors."""
    
    def __init__(self, image_path: str):
        """
        Initialize analyzer with screenshot path.
        
        Args:
            image_path: Path to PNG screenshot
        """
        self.image_path = Path(image_path)
        if not self.image_path.exists():
            raise FileNotFoundError(f"Screenshot not found: {image_path}")
        
        self.image = Image.open(self.image_path).convert('RGB')
        self.image_array = np.array(self.image)
        self.reader = easyocr.Reader(['en'], gpu=False)
    
    def detect_text_regions(self) -> List[Dict]:
        """
        Detect text regions using OCR.
        
        Returns:
            List of detected text regions with bounding boxes
        """
        results = self.reader.readtext(np.array(self.image))
        
        text_regions = []
        for detection in results:
            bbox, text, confidence = detection
            
            # Convert bbox to integer coordinates
            x_coords = [point[0] for point in bbox]
            y_coords = [point[1] for point in bbox]
            
            x_min = int(min(x_coords))
            x_max = int(max(x_coords))
            y_min = int(min(y_coords))
            y_max = int(max(y_coords))
            
            text_regions.append({
                'text': text,
                'bbox': (x_min, y_min, x_max, y_max),
                'confidence': confidence
            })
        
        return text_regions
    
    def extract_text_and_background_colors(self, bbox: Tuple[int, int, int, int]) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
        """
        Extract both text and background colors from a bounding box.
        Expands bbox to capture background, then uses luminance clustering.
        
        Args:
            bbox: Bounding box (x_min, y_min, x_max, y_max)
            
        Returns:
            Tuple of (text_color, background_color) as RGB tuples
        """
        x_min, y_min, x_max, y_max = bbox
        
        # Ensure coordinates are within image bounds
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(self.image_array.shape[1], x_max)
        y_max = min(self.image_array.shape[0], y_max)
        
        # Extract text region (tight bbox)
        text_region = self.image_array[y_min:y_max, x_min:x_max]
        
        if text_region.size == 0:
            return ((0, 0, 0), (255, 255, 255))
        
        # Also sample expanded region for background (add padding)
        padding = 10
        bg_x_min = max(0, x_min - padding)
        bg_y_min = max(0, y_min - padding)
        bg_x_max = min(self.image_array.shape[1], x_max + padding)
        bg_y_max = min(self.image_array.shape[0], y_max + padding)
        
        # Get background samples from border area
        bg_samples = []
        
        # Top border
        if bg_y_min < y_min:
            bg_samples.append(self.image_array[bg_y_min:y_min, bg_x_min:bg_x_max])
        # Bottom border
        if y_max < bg_y_max:
            bg_samples.append(self.image_array[y_max:bg_y_max, bg_x_min:bg_x_max])
        # Left border
        if bg_x_min < x_min:
            bg_samples.append(self.image_array[y_min:y_max, bg_x_min:x_min])
        # Right border
        if x_max < bg_x_max:
            bg_samples.append(self.image_array[y_min:y_max, x_max:bg_x_max])
        
        # Flatten text pixels
        text_pixels = text_region.reshape(-1, 3)
        
        # Calculate luminance for text pixels
        text_luminances = np.array([
            WCAGContrastChecker.rgb_to_relative_luminance(tuple(pixel))
            for pixel in text_pixels
        ])
        
        # Get the darkest and lightest pixels from text region (excluding anti-aliasing)
        # Use 10th and 90th percentile to avoid edge artifacts
        dark_threshold = np.percentile(text_luminances, 10)
        light_threshold = np.percentile(text_luminances, 90)
        
        dark_pixels = text_pixels[text_luminances <= dark_threshold]
        light_pixels = text_pixels[text_luminances >= light_threshold]
        
        # Get median color from each group
        if len(dark_pixels) > 0:
            dark_color = tuple(np.median(dark_pixels, axis=0).astype(int))
        else:
            dark_color = tuple(text_pixels[np.argmin(text_luminances)])
        
        if len(light_pixels) > 0:
            light_color = tuple(np.median(light_pixels, axis=0).astype(int))
        else:
            light_color = tuple(text_pixels[np.argmax(text_luminances)])
        
        # If we have background samples, use them
        if bg_samples:
            bg_pixels = np.vstack([s.reshape(-1, 3) for s in bg_samples if s.size > 0])
            if len(bg_pixels) > 0:
                # Background is usually the most common color in border
                unique_bg, counts_bg = np.unique(bg_pixels, axis=0, return_counts=True)
                bg_color = tuple(unique_bg[np.argmax(counts_bg)])
                
                # Determine which text color (dark or light) has better contrast with background
                bg_lum = WCAGContrastChecker.rgb_to_relative_luminance(bg_color)
                dark_lum = WCAGContrastChecker.rgb_to_relative_luminance(dark_color)
                light_lum = WCAGContrastChecker.rgb_to_relative_luminance(light_color)
                
                dark_contrast = WCAGContrastChecker.calculate_contrast_ratio(dark_color, bg_color)
                light_contrast = WCAGContrastChecker.calculate_contrast_ratio(light_color, bg_color)
                
                # Choose the text color with better contrast
                if dark_contrast > light_contrast:
                    return (dark_color, bg_color)
                else:
                    return (light_color, bg_color)
        
        # Fallback: no background samples, use dark/light from text region
        # Assume more frequent is background
        dark_count = len(dark_pixels)
        light_count = len(light_pixels)
        
        if light_count > dark_count * 1.5:
            return (dark_color, light_color)
        elif dark_count > light_count * 1.5:
            return (light_color, dark_color)
        else:
            # Similar amounts - assume text is darker
            return (dark_color, light_color)
    
    
    def analyze(self) -> List[Dict]:
        """
        Perform full analysis of screenshot.
        
        Returns:
            List of analysis results for each text element
        """
        print(f"Analyzing screenshot: {self.image_path.name}")
        print(f"Image size: {self.image.size}")
        print("Detecting text regions...")
        
        text_regions = self.detect_text_regions()
        print(f"Found {len(text_regions)} text regions")
        
        results = []
        
        for i, region in enumerate(text_regions, 1):
            print(f"\nAnalyzing region {i}/{len(text_regions)}: '{region['text'][:30]}...'")
            
            bbox = region['bbox']
            text_color, bg_color = self.extract_text_and_background_colors(bbox)
            
            contrast_ratio = WCAGContrastChecker.calculate_contrast_ratio(
                text_color, bg_color
            )
            
            # Assume normal text for now (can be enhanced later)
            compliance = WCAGContrastChecker.check_compliance(contrast_ratio, is_large_text=False)
            
            result = {
                'text': region['text'],
                'bbox': bbox,
                'text_color': text_color,
                'background_color': bg_color,
                'contrast_ratio': round(contrast_ratio, 2),
                'wcag_aa': 'PASS' if compliance['AA'] else 'FAIL',
                'wcag_aaa': 'PASS' if compliance['AAA'] else 'FAIL',
                'confidence': round(region['confidence'], 2)
            }
            
            results.append(result)
        
        return results


def format_color(rgb: Tuple[int, int, int]) -> str:
    """Format RGB tuple as readable string."""
    r, g, b = rgb
    return f"RGB({r:3d}, {g:3d}, {b:3d}) | #{r:02x}{g:02x}{b:02x}"


def print_results(results: List[Dict]):
    """Print analysis results in a readable format."""
    print("\n" + "="*80)
    print("WCAG CONTRAST ANALYSIS RESULTS")
    print("="*80)
    
    if not results:
        print("\nNo text detected in the screenshot.")
        return
    
    aa_fails = sum(1 for r in results if r['wcag_aa'] == 'FAIL')
    aaa_fails = sum(1 for r in results if r['wcag_aaa'] == 'FAIL')
    
    print(f"\nTotal text elements: {len(results)}")
    print(f"WCAG AA failures: {aa_fails}")
    print(f"WCAG AAA failures: {aaa_fails}")
    
    print("\n" + "-"*80)
    print("DETAILED RESULTS")
    print("-"*80)
    
    for i, result in enumerate(results, 1):
        print(f"\n[{i}] Text: \"{result['text'][:50]}\"")
        print(f"    Position: {result['bbox']}")
        print(f"    Text color:       {format_color(result['text_color'])}")
        print(f"    Background color: {format_color(result['background_color'])}")
        print(f"    Contrast ratio: {result['contrast_ratio']}:1")
        print(f"    WCAG AA:  {result['wcag_aa']} (minimum 4.5:1 for normal text)")
        print(f"    WCAG AAA: {result['wcag_aaa']} (minimum 7.0:1 for normal text)")
        print(f"    OCR confidence: {result['confidence']}")


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python wcag_contrast_checker.py <screenshot.png>")
        print("\nExample:")
        print("  python wcag_contrast_checker.py screenshots/mobile_app.png")
        sys.exit(1)
    
    screenshot_path = sys.argv[1]
    
    try:
        analyzer = ScreenshotAnalyzer(screenshot_path)
        results = analyzer.analyze()
        print_results(results)
        
        # Summary
        aa_pass = sum(1 for r in results if r['wcag_aa'] == 'PASS')
        aaa_pass = sum(1 for r in results if r['wcag_aaa'] == 'PASS')
        
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"WCAG AA:  {aa_pass}/{len(results)} passed")
        print(f"WCAG AAA: {aaa_pass}/{len(results)} passed")
        
        if aa_pass < len(results):
            print("\n⚠️  Some elements do not meet WCAG AA standards.")
        else:
            print("\n✓ All elements meet WCAG AA standards.")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
