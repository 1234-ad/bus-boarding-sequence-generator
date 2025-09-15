#!/usr/bin/env python3
"""
Command Line Interface for Bus Boarding Sequence Generator

Usage:
    python boarding_cli.py input.txt
    python boarding_cli.py input.txt --output output.txt
    python boarding_cli.py --interactive
"""

import argparse
import sys
import os
from typing import List, Tuple

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from boarding_sequence_generator import BusBoardingSequenceGenerator


def interactive_mode():
    """Run the generator in interactive mode."""
    print("=" * 50)
    print("Bus Boarding Sequence Generator - Interactive Mode")
    print("=" * 50)
    
    generator = BusBoardingSequenceGenerator()
    bookings = []
    
    print("\nEnter booking data (press Enter with empty Booking ID to finish):")
    print("Format: Booking_ID Seats (e.g., 101 A1,B1)")
    print("-" * 30)
    
    while True:
        try:
            booking_input = input("Booking ID: ").strip()
            if not booking_input:
                break
            
            booking_id = int(booking_input)
            seats_input = input("Seats (comma-separated): ").strip()
            
            if seats_input:
                bookings.append((booking_id, seats_input))
                print(f"✓ Added: Booking {booking_id} -> {seats_input}")
            else:
                print("⚠ Skipped: No seats provided")
            
            print()
            
        except ValueError:
            print("⚠ Invalid booking ID. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            return
    
    if not bookings:
        print("No bookings entered. Exiting.")
        return
    
    # Generate sequence
    generator.load_bookings_from_data(bookings)
    
    print("\n" + "=" * 30)
    print("BOARDING SEQUENCE RESULTS")
    print("=" * 30)
    generator.print_boarding_sequence()
    
    # Show detailed analysis
    print("\n" + "-" * 30)
    print("DETAILED ANALYSIS")
    print("-" * 30)
    details = generator.get_boarding_details()
    for detail in details:
        print(f"Seq {detail['sequence']}: Booking {detail['booking_id']} "
              f"(Seats: {', '.join(detail['seats'])}, "
              f"Furthest: Row {detail['furthest_seat_distance']})")
    
    # Ask if user wants to save results
    save_choice = input("\nSave results to file? (y/N): ").strip().lower()
    if save_choice in ['y', 'yes']:
        output_file = input("Output filename (default: boarding_sequence.txt): ").strip()
        if not output_file:
            output_file = "boarding_sequence.txt"
        
        try:
            generator.export_to_file(output_file)
            print(f"✓ Results saved to {output_file}")
        except Exception as e:
            print(f"✗ Error saving file: {e}")


def file_mode(input_file: str, output_file: str = None):
    """Process a file and generate boarding sequence."""
    print("=" * 50)
    print("Bus Boarding Sequence Generator - File Mode")
    print("=" * 50)
    
    if not os.path.exists(input_file):
        print(f"✗ Error: Input file '{input_file}' not found.")
        return 1
    
    try:
        generator = BusBoardingSequenceGenerator()
        generator.load_bookings_from_file(input_file)
        
        print(f"✓ Loaded booking data from: {input_file}")
        print(f"✓ Total bookings: {len(generator.bookings)}")
        
        print("\n" + "=" * 30)
        print("BOARDING SEQUENCE RESULTS")
        print("=" * 30)
        generator.print_boarding_sequence()
        
        # Show detailed analysis
        print("\n" + "-" * 30)
        print("DETAILED ANALYSIS")
        print("-" * 30)
        details = generator.get_boarding_details()
        for detail in details:
            print(f"Seq {detail['sequence']}: Booking {detail['booking_id']} "
                  f"(Seats: {', '.join(detail['seats'])}, "
                  f"Furthest: Row {detail['furthest_seat_distance']})")
        
        # Save to output file if specified
        if output_file:
            generator.export_to_file(output_file)
            print(f"\n✓ Results saved to: {output_file}")
        
        return 0
        
    except Exception as e:
        print(f"✗ Error processing file: {e}")
        return 1


def create_sample_file():
    """Create a sample input file for demonstration."""
    sample_content = """Booking_ID	Seats
101	A1,B1
120	A20,C2
105	A15,B15
130	C5,D5
115	A10,B10,C10
140	D18,C18"""
    
    filename = "sample_bookings.txt"
    with open(filename, 'w') as f:
        f.write(sample_content)
    
    print(f"✓ Sample file created: {filename}")
    print("\nSample content:")
    print("-" * 20)
    print(sample_content)
    print("-" * 20)
    print(f"\nTry: python {sys.argv[0]} {filename}")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Bus Boarding Sequence Generator - Optimize boarding time with front entry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python boarding_cli.py bookings.txt
  python boarding_cli.py bookings.txt --output sequence.txt
  python boarding_cli.py --interactive
  python boarding_cli.py --sample

Input file format:
  Booking_ID    Seats
  101           A1,B1
  120           A20,C2
        """
    )
    
    parser.add_argument('input_file', nargs='?', help='Input file with booking data')
    parser.add_argument('-o', '--output', help='Output file for results')
    parser.add_argument('-i', '--interactive', action='store_true', 
                       help='Run in interactive mode')
    parser.add_argument('-s', '--sample', action='store_true',
                       help='Create a sample input file')
    parser.add_argument('-v', '--version', action='version', version='Bus Boarding Sequence Generator 1.0')
    
    args = parser.parse_args()
    
    # Handle different modes
    if args.sample:
        create_sample_file()
        return 0
    
    if args.interactive:
        interactive_mode()
        return 0
    
    if not args.input_file:
        parser.print_help()
        print("\n✗ Error: Please provide an input file or use --interactive mode")
        return 1
    
    return file_mode(args.input_file, args.output)


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)