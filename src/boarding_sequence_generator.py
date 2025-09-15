"""
Bus Boarding Sequence Generator

This module generates optimal boarding sequences for bus passengers
to minimize boarding time with a single front entry point.
"""

import re
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class Booking:
    """Represents a booking with ID and seat assignments."""
    booking_id: int
    seats: List[str]
    min_distance: int = 0


class BusBoardingSequenceGenerator:
    """
    Generates optimal boarding sequences for bus passengers.
    
    The algorithm prioritizes passengers with seats furthest from the front entry
    to minimize blocking and reduce overall boarding time.
    """
    
    def __init__(self):
        """Initialize the boarding sequence generator."""
        self.bookings: List[Booking] = []
    
    def parse_seat_distance(self, seat: str) -> int:
        """
        Calculate distance from front entry based on seat label.
        
        Args:
            seat: Seat label (e.g., 'A1', 'B20', 'C15')
            
        Returns:
            Distance from front entry (higher number = further from front)
        """
        # Extract row number from seat (e.g., 'A20' -> 20, 'C2' -> 2)
        match = re.search(r'(\d+)', seat)
        if match:
            return int(match.group(1))
        return 0
    
    def load_bookings_from_file(self, file_path: str) -> None:
        """
        Load booking data from file.
        
        Args:
            file_path: Path to the booking data file
        """
        self.bookings = []
        
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                
                # Skip header if present
                start_idx = 1 if lines and 'Booking_ID' in lines[0] else 0
                
                for line in lines[start_idx:]:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        booking_id = int(parts[0])
                        seats = [seat.strip() for seat in parts[1].split(',')]
                        
                        # Calculate minimum distance (furthest seat from front)
                        distances = [self.parse_seat_distance(seat) for seat in seats]
                        min_distance = max(distances) if distances else 0
                        
                        booking = Booking(booking_id, seats, min_distance)
                        self.bookings.append(booking)
                        
        except FileNotFoundError:
            raise FileNotFoundError(f"Booking file not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading booking file: {str(e)}")
    
    def load_bookings_from_data(self, booking_data: List[Tuple[int, str]]) -> None:
        """
        Load booking data from list of tuples.
        
        Args:
            booking_data: List of (booking_id, seats_string) tuples
        """
        self.bookings = []
        
        for booking_id, seats_string in booking_data:
            seats = [seat.strip() for seat in seats_string.split(',')]
            
            # Calculate minimum distance (furthest seat from front)
            distances = [self.parse_seat_distance(seat) for seat in seats]
            min_distance = max(distances) if distances else 0
            
            booking = Booking(booking_id, seats, min_distance)
            self.bookings.append(booking)
    
    def generate_boarding_sequence(self) -> List[Tuple[int, int]]:
        """
        Generate optimal boarding sequence.
        
        Returns:
            List of (sequence_number, booking_id) tuples
        """
        if not self.bookings:
            return []
        
        # Sort by distance (descending) then by booking_id (ascending) for ties
        sorted_bookings = sorted(
            self.bookings,
            key=lambda x: (-x.min_distance, x.booking_id)
        )
        
        # Generate sequence
        sequence = []
        for i, booking in enumerate(sorted_bookings, 1):
            sequence.append((i, booking.booking_id))
        
        return sequence
    
    def get_boarding_details(self) -> List[Dict]:
        """
        Get detailed boarding information for analysis.
        
        Returns:
            List of dictionaries with booking details
        """
        sequence = self.generate_boarding_sequence()
        details = []
        
        booking_dict = {b.booking_id: b for b in self.bookings}
        
        for seq_num, booking_id in sequence:
            booking = booking_dict[booking_id]
            details.append({
                'sequence': seq_num,
                'booking_id': booking_id,
                'seats': booking.seats,
                'furthest_seat_distance': booking.min_distance
            })
        
        return details
    
    def print_boarding_sequence(self) -> None:
        """Print the boarding sequence in UI-friendly format."""
        sequence = self.generate_boarding_sequence()
        
        print("Seq   Booking_ID")
        print("-" * 15)
        for seq_num, booking_id in sequence:
            print(f"{seq_num:<5} {booking_id}")
    
    def export_to_file(self, output_path: str) -> None:
        """
        Export boarding sequence to file.
        
        Args:
            output_path: Path for output file
        """
        sequence = self.generate_boarding_sequence()
        
        with open(output_path, 'w') as file:
            file.write("Seq\tBooking_ID\n")
            for seq_num, booking_id in sequence:
                file.write(f"{seq_num}\t{booking_id}\n")


def main():
    """Example usage of the boarding sequence generator."""
    generator = BusBoardingSequenceGenerator()
    
    # Example data
    sample_data = [
        (101, "A1,B1"),
        (120, "A20,C2")
    ]
    
    generator.load_bookings_from_data(sample_data)
    
    print("Bus Boarding Sequence Generator")
    print("=" * 40)
    generator.print_boarding_sequence()
    
    print("\nDetailed Analysis:")
    print("-" * 40)
    details = generator.get_boarding_details()
    for detail in details:
        print(f"Seq {detail['sequence']}: Booking {detail['booking_id']} "
              f"(Seats: {', '.join(detail['seats'])}, "
              f"Furthest: Row {detail['furthest_seat_distance']})")


if __name__ == "__main__":
    main()