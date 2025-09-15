"""
Unit tests for Bus Boarding Sequence Generator
"""

import unittest
import tempfile
import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from boarding_sequence_generator import BusBoardingSequenceGenerator, Booking


class TestBoardingSequenceGenerator(unittest.TestCase):
    """Test cases for the boarding sequence generator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = BusBoardingSequenceGenerator()
    
    def test_parse_seat_distance(self):
        """Test seat distance parsing."""
        test_cases = [
            ("A1", 1),
            ("B20", 20),
            ("C15", 15),
            ("D5", 5),
            ("A100", 100),
            ("Z1", 1),
        ]
        
        for seat, expected_distance in test_cases:
            with self.subTest(seat=seat):
                distance = self.generator.parse_seat_distance(seat)
                self.assertEqual(distance, expected_distance)
    
    def test_parse_seat_distance_invalid(self):
        """Test seat distance parsing with invalid inputs."""
        invalid_seats = ["", "ABC", "X", "123"]
        
        for seat in invalid_seats:
            with self.subTest(seat=seat):
                distance = self.generator.parse_seat_distance(seat)
                self.assertEqual(distance, 0)
    
    def test_load_bookings_from_data(self):
        """Test loading bookings from data."""
        booking_data = [
            (101, "A1,B1"),
            (120, "A20,C2"),
            (105, "A15,B15")
        ]
        
        self.generator.load_bookings_from_data(booking_data)
        
        self.assertEqual(len(self.generator.bookings), 3)
        
        # Check first booking
        booking1 = self.generator.bookings[0]
        self.assertEqual(booking1.booking_id, 101)
        self.assertEqual(booking1.seats, ["A1", "B1"])
        self.assertEqual(booking1.min_distance, 1)  # max of [1, 1]
        
        # Check second booking
        booking2 = self.generator.bookings[1]
        self.assertEqual(booking2.booking_id, 120)
        self.assertEqual(booking2.seats, ["A20", "C2"])
        self.assertEqual(booking2.min_distance, 20)  # max of [20, 2]
    
    def test_load_bookings_from_file(self):
        """Test loading bookings from file."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("Booking_ID\tSeats\n")
            temp_file.write("101\tA1,B1\n")
            temp_file.write("120\tA20,C2\n")
            temp_file.write("105\tA15,B15\n")
            temp_file_path = temp_file.name
        
        try:
            self.generator.load_bookings_from_file(temp_file_path)
            
            self.assertEqual(len(self.generator.bookings), 3)
            
            # Verify data loaded correctly
            booking_ids = [b.booking_id for b in self.generator.bookings]
            self.assertIn(101, booking_ids)
            self.assertIn(120, booking_ids)
            self.assertIn(105, booking_ids)
            
        finally:
            os.unlink(temp_file_path)
    
    def test_load_bookings_from_file_no_header(self):
        """Test loading bookings from file without header."""
        # Create temporary file without header
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("101\tA1,B1\n")
            temp_file.write("120\tA20,C2\n")
            temp_file_path = temp_file.name
        
        try:
            self.generator.load_bookings_from_file(temp_file_path)
            self.assertEqual(len(self.generator.bookings), 2)
            
        finally:
            os.unlink(temp_file_path)
    
    def test_load_bookings_file_not_found(self):
        """Test loading from non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.generator.load_bookings_from_file("non_existent_file.txt")
    
    def test_generate_boarding_sequence_basic(self):
        """Test basic boarding sequence generation."""
        booking_data = [
            (101, "A1,B1"),      # Distance: 1
            (120, "A20,C2"),     # Distance: 20
            (105, "A15,B15")     # Distance: 15
        ]
        
        self.generator.load_bookings_from_data(booking_data)
        sequence = self.generator.generate_boarding_sequence()
        
        # Should be ordered by distance (descending), then by booking_id (ascending)
        expected_order = [120, 105, 101]  # 20, 15, 1
        actual_order = [booking_id for _, booking_id in sequence]
        
        self.assertEqual(actual_order, expected_order)
        
        # Check sequence numbers
        expected_sequence = [(1, 120), (2, 105), (3, 101)]
        self.assertEqual(sequence, expected_sequence)
    
    def test_generate_boarding_sequence_tie_breaking(self):
        """Test tie breaking with same distances."""
        booking_data = [
            (105, "A10,B10"),    # Distance: 10
            (101, "A10,C10"),    # Distance: 10 (same as above)
            (120, "A20,C2"),     # Distance: 20
        ]
        
        self.generator.load_bookings_from_data(booking_data)
        sequence = self.generator.generate_boarding_sequence()
        
        # Should be: 120 (distance 20), then 101 (distance 10, lower ID), then 105 (distance 10, higher ID)
        expected_order = [120, 101, 105]
        actual_order = [booking_id for _, booking_id in sequence]
        
        self.assertEqual(actual_order, expected_order)
    
    def test_generate_boarding_sequence_multiple_seats(self):
        """Test with bookings having multiple seats."""
        booking_data = [
            (101, "A1,B1,C1"),       # Distance: 1 (max of [1,1,1])
            (120, "A5,B10,C20"),     # Distance: 20 (max of [5,10,20])
            (105, "A15,B2,C8")       # Distance: 15 (max of [15,2,8])
        ]
        
        self.generator.load_bookings_from_data(booking_data)
        sequence = self.generator.generate_boarding_sequence()
        
        # Should be ordered by furthest seat: 120 (20), 105 (15), 101 (1)
        expected_order = [120, 105, 101]
        actual_order = [booking_id for _, booking_id in sequence]
        
        self.assertEqual(actual_order, expected_order)
    
    def test_generate_boarding_sequence_empty(self):
        """Test with no bookings."""
        sequence = self.generator.generate_boarding_sequence()
        self.assertEqual(sequence, [])
    
    def test_get_boarding_details(self):
        """Test getting detailed boarding information."""
        booking_data = [
            (101, "A1,B1"),
            (120, "A20,C2")
        ]
        
        self.generator.load_bookings_from_data(booking_data)
        details = self.generator.get_boarding_details()
        
        self.assertEqual(len(details), 2)
        
        # First in sequence should be booking 120
        first_detail = details[0]
        self.assertEqual(first_detail['sequence'], 1)
        self.assertEqual(first_detail['booking_id'], 120)
        self.assertEqual(first_detail['seats'], ['A20', 'C2'])
        self.assertEqual(first_detail['furthest_seat_distance'], 20)
        
        # Second in sequence should be booking 101
        second_detail = details[1]
        self.assertEqual(second_detail['sequence'], 2)
        self.assertEqual(second_detail['booking_id'], 101)
        self.assertEqual(second_detail['seats'], ['A1', 'B1'])
        self.assertEqual(second_detail['furthest_seat_distance'], 1)
    
    def test_export_to_file(self):
        """Test exporting results to file."""
        booking_data = [
            (101, "A1,B1"),
            (120, "A20,C2")
        ]
        
        self.generator.load_bookings_from_data(booking_data)
        
        # Create temporary output file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file_path = temp_file.name
        
        try:
            self.generator.export_to_file(temp_file_path)
            
            # Read and verify content
            with open(temp_file_path, 'r') as f:
                content = f.read()
            
            expected_lines = [
                "Seq\tBooking_ID",
                "1\t120",
                "2\t101"
            ]
            
            actual_lines = content.strip().split('\n')
            self.assertEqual(actual_lines, expected_lines)
            
        finally:
            os.unlink(temp_file_path)
    
    def test_booking_dataclass(self):
        """Test Booking dataclass."""
        booking = Booking(booking_id=101, seats=["A1", "B1"], min_distance=1)
        
        self.assertEqual(booking.booking_id, 101)
        self.assertEqual(booking.seats, ["A1", "B1"])
        self.assertEqual(booking.min_distance, 1)
    
    def test_complex_scenario(self):
        """Test a complex real-world scenario."""
        booking_data = [
            (201, "A1,B1,C1"),       # Distance: 1
            (202, "A20,B20"),        # Distance: 20
            (203, "A10,C10,D10"),    # Distance: 10
            (204, "B5,C5"),          # Distance: 5
            (205, "A18,D18"),        # Distance: 18
            (206, "C15,D15"),        # Distance: 15
            (207, "A20,B19"),        # Distance: 20 (tie with 202)
        ]
        
        self.generator.load_bookings_from_data(booking_data)
        sequence = self.generator.generate_boarding_sequence()
        
        # Expected order: 202 (20), 207 (20), 205 (18), 206 (15), 203 (10), 204 (5), 201 (1)
        # For ties (202 and 207 both have distance 20), lower booking ID goes first
        expected_order = [202, 207, 205, 206, 203, 204, 201]
        actual_order = [booking_id for _, booking_id in sequence]
        
        self.assertEqual(actual_order, expected_order)


class TestIntegration(unittest.TestCase):
    """Integration tests."""
    
    def test_end_to_end_file_processing(self):
        """Test complete file processing workflow."""
        # Create test file
        test_data = """Booking_ID	Seats
101	A1,B1
120	A20,C2
105	A15,B15
130	C5,D5"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as input_file:
            input_file.write(test_data)
            input_file_path = input_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as output_file:
            output_file_path = output_file.name
        
        try:
            # Process file
            generator = BusBoardingSequenceGenerator()
            generator.load_bookings_from_file(input_file_path)
            generator.export_to_file(output_file_path)
            
            # Verify output
            with open(output_file_path, 'r') as f:
                content = f.read()
            
            lines = content.strip().split('\n')
            self.assertEqual(lines[0], "Seq\tBooking_ID")
            
            # Should have 4 bookings + header
            self.assertEqual(len(lines), 5)
            
            # First booking should be 120 (A20 = distance 20)
            self.assertEqual(lines[1], "1\t120")
            
        finally:
            os.unlink(input_file_path)
            os.unlink(output_file_path)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)