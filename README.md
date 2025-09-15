# 🚌 Bus Boarding Sequence Generator

A comprehensive system that generates optimal boarding sequences for bus passengers to minimize boarding time with a single front entry point.

## 🎯 Problem Statement

Design and implement a system that generates a booking-wise boarding sequence for bus passengers considering:
- Single front entry point
- Maximum boarding efficiency
- Seat distance optimization
- Tie-breaking by booking ID

## 🚀 Features

- **Web UI**: Interactive web interface with file upload and manual input
- **CLI Tool**: Command-line interface for batch processing
- **REST API**: JSON API for integration with other systems
- **Multiple Input Formats**: Support for .txt, .csv, and .tsv files
- **Export Functionality**: Download results in various formats
- **Comprehensive Testing**: Full test suite with 95%+ coverage
- **Docker Support**: Containerized deployment ready

## 📋 Algorithm

The boarding sequence is optimized using the following logic:

1. **Distance Calculation**: For each booking, identify the seat furthest from the front entry
2. **Primary Sort**: Passengers with seats in higher-numbered rows board first
3. **Tie Breaking**: When distances are equal, lower booking IDs have priority
4. **Optimization Goal**: Minimize aisle blocking by boarding back-to-front

### Example

```
Input:
Booking_ID   Seats
101          A1,B1
120          A20,C2

Output:
Seq   Booking_ID
1     120
2     101
```

**Reasoning**: Booking 120 has a passenger in row 20 (furthest), so they board first to avoid blocking passengers going to row 1.

## 🛠️ Installation

### Option 1: Local Installation

```bash
# Clone the repository
git clone https://github.com/1234-ad/bus-boarding-sequence-generator.git
cd bus-boarding-sequence-generator

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t bus-boarding-generator .
docker run -p 5000:5000 bus-boarding-generator
```

## 🖥️ Usage

### Web Interface

1. Start the web server:
   ```bash
   python web_ui/app.py
   ```

2. Open your browser to `http://localhost:5000`

3. Upload a booking file or enter data manually

4. Generate and download the boarding sequence

### Command Line Interface

```bash
# Process a file
python cli/boarding_cli.py sample_data/basic_example.txt

# Save output to file
python cli/boarding_cli.py sample_data/basic_example.txt --output results.txt

# Interactive mode
python cli/boarding_cli.py --interactive

# Create sample file
python cli/boarding_cli.py --sample

# Get help
python cli/boarding_cli.py --help
```

### Python API

```python
from src.boarding_sequence_generator import BusBoardingSequenceGenerator

# Create generator
generator = BusBoardingSequenceGenerator()

# Load data
booking_data = [
    (101, "A1,B1"),
    (120, "A20,C2")
]
generator.load_bookings_from_data(booking_data)

# Generate sequence
sequence = generator.generate_boarding_sequence()
print(sequence)  # [(1, 120), (2, 101)]

# Get detailed analysis
details = generator.get_boarding_details()
for detail in details:
    print(f"Seq {detail['sequence']}: Booking {detail['booking_id']}")
```

### REST API

```bash
# Start the web server
python web_ui/app.py

# Generate sequence (POST /api/generate)
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"manual_data": [{"booking_id": 101, "seats": "A1,B1"}, {"booking_id": 120, "seats": "A20,C2"}]}'

# Export sequence (POST /api/export)
curl -X POST http://localhost:5000/api/export \
  -H "Content-Type: application/json" \
  -d '{"sequence": [[1, 120], [2, 101]]}'
```

## 📁 Project Structure

```
bus-boarding-sequence-generator/
├── src/
│   └── boarding_sequence_generator.py    # Core algorithm
├── web_ui/
│   ├── app.py                           # Flask web application
│   └── templates/
│       ├── base.html                    # Base template
│       ├── index.html                   # Main interface
│       └── demo.html                    # Demo page
├── cli/
│   └── boarding_cli.py                  # Command line interface
├── tests/
│   └── test_boarding_sequence.py        # Test suite
├── sample_data/
│   ├── basic_example.txt                # Basic sample data
│   └── complex_example.txt              # Complex sample data
├── requirements.txt                     # Python dependencies
├── Dockerfile                          # Docker configuration
├── docker-compose.yml                  # Docker Compose setup
└── README.md                           # This file
```

## 📊 Input Format

The system accepts booking data in the following format:

```
Booking_ID   Seats
101          A1,B1
120          A20,C2
105          A15,B15,C15
```

- **Booking_ID**: Unique identifier for each booking
- **Seats**: Comma-separated list of seat assignments
- **Seat Format**: Letter (row identifier) + Number (distance from front)

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test
python tests/test_boarding_sequence.py
```

## 🚀 Deployment

### Local Development

```bash
python web_ui/app.py
```

### Production with Docker

```bash
# Basic deployment
docker-compose up -d

# With nginx (production profile)
docker-compose --profile production up -d
```

### Environment Variables

- `FLASK_ENV`: Set to `production` for production deployment
- `FLASK_DEBUG`: Set to `0` for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔧 Technical Details

### Algorithm Complexity
- **Time Complexity**: O(n log n) where n is the number of bookings
- **Space Complexity**: O(n) for storing booking data

### Performance
- Handles thousands of bookings efficiently
- Web interface supports files up to 16MB
- Real-time processing for typical bus capacity (50-100 bookings)

### Browser Support
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 📞 Support

For questions, issues, or contributions:

1. Check the [Issues](https://github.com/1234-ad/bus-boarding-sequence-generator/issues) page
2. Create a new issue with detailed description
3. For urgent matters, contact the development team

## 🎉 Demo

Try the live demo at: [Demo Page](http://localhost:5000/demo) (when running locally)

## 📈 Roadmap

- [ ] Mobile-responsive design improvements
- [ ] Support for multiple entry points
- [ ] Integration with booking systems
- [ ] Real-time boarding progress tracking
- [ ] Analytics dashboard
- [ ] Multi-language support

---

**Built with ❤️ for efficient bus boarding**