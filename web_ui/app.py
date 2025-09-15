"""
Flask Web Application for Bus Boarding Sequence Generator
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from boarding_sequence_generator import BusBoardingSequenceGenerator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'txt', 'csv', 'tsv'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page with file upload and manual input options."""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_sequence():
    """Generate boarding sequence from uploaded file or manual input."""
    try:
        generator = BusBoardingSequenceGenerator()
        
        # Check if file was uploaded
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            
            if file and allowed_file(file.filename):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as temp_file:
                    content = file.read().decode('utf-8')
                    temp_file.write(content)
                    temp_file_path = temp_file.name
                
                try:
                    generator.load_bookings_from_file(temp_file_path)
                finally:
                    os.unlink(temp_file_path)  # Clean up temp file
            else:
                return jsonify({'error': 'Invalid file type. Please upload .txt, .csv, or .tsv files.'}), 400
        
        # Check for manual input
        elif 'manual_data' in request.json:
            manual_data = request.json['manual_data']
            booking_data = []
            
            for entry in manual_data:
                booking_id = int(entry['booking_id'])
                seats = entry['seats']
                booking_data.append((booking_id, seats))
            
            generator.load_bookings_from_data(booking_data)
        
        else:
            return jsonify({'error': 'No data provided. Please upload a file or enter manual data.'}), 400
        
        # Generate sequence and details
        sequence = generator.generate_boarding_sequence()
        details = generator.get_boarding_details()
        
        return jsonify({
            'success': True,
            'sequence': sequence,
            'details': details,
            'total_bookings': len(sequence)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export', methods=['POST'])
def export_sequence():
    """Export boarding sequence to downloadable file."""
    try:
        data = request.json
        sequence = data.get('sequence', [])
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("Seq\tBooking_ID\n")
            for seq_num, booking_id in sequence:
                temp_file.write(f"{seq_num}\t{booking_id}\n")
            temp_file_path = temp_file.name
        
        return send_file(
            temp_file_path,
            as_attachment=True,
            download_name='boarding_sequence.txt',
            mimetype='text/plain'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/demo')
def demo():
    """Demo page with sample data."""
    return render_template('demo.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)