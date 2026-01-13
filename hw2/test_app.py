import pytest
import json
from api.index import app, text_to_number, number_to_text, base64_to_number, number_to_base64
import base64


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestUtilityFunctions:
    """Test the utility functions directly"""
    
    def test_text_to_number_basic(self):
        """Test basic text to number conversions"""
        assert text_to_number("zero") == 0
        assert text_to_number("one") == 1
        assert text_to_number("five") == 5
        assert text_to_number("ten") == 10
    
    def test_text_to_number_case_insensitive(self):
        """Test that text conversion is case insensitive"""
        assert text_to_number("ONE") == 1
        assert text_to_number("Five") == 5
        assert text_to_number("TEN") == 10
    
    def test_text_to_number_with_punctuation(self):
        """Test text conversion with punctuation"""
        assert text_to_number("one!") == 1
        assert text_to_number("five.") == 5
    
    def test_text_to_number_invalid(self):
        """Test invalid text inputs"""
        with pytest.raises(ValueError):
            text_to_number("invalid")
        with pytest.raises(ValueError):
            text_to_number("eleven")  # Not in our basic dictionary
    
    def test_number_to_text(self):
        """Test number to text conversion"""
        assert number_to_text(0) == "zero"
        assert number_to_text(1) == "one"
        assert number_to_text(42) == "forty-two"
        assert number_to_text(123) == "one hundred and twenty-three"
    
    def test_base64_to_number_little_endian(self):
        """Test base64 to number conversion using little-endian byte order"""
        # Test with known values using little-endian
        # Number 42 in little-endian bytes: [42, 0, 0, 0] -> base64: "KgAAAA=="
        number = 42
        byte_count = (number.bit_length() + 7) // 8
        if byte_count == 0:
            byte_count = 1
        number_bytes = number.to_bytes(byte_count, byteorder='little')
        b64_str = base64.b64encode(number_bytes).decode('utf-8')
        
        assert base64_to_number(b64_str) == 42
    
    def test_number_to_base64_little_endian(self):
        """Test number to base64 conversion using little-endian byte order"""
        # Test various numbers
        for number in [0, 1, 42, 255, 256, 65535]:
            b64_result = number_to_base64(number)
            # Verify we can convert back
            assert base64_to_number(b64_result) == number
    
    def test_base64_invalid_input(self):
        """Test invalid base64 inputs"""
        with pytest.raises(ValueError):
            base64_to_number("invalid_base64!")
        with pytest.raises(ValueError):
            base64_to_number("not base64")


class TestConversionEndpoint:
    """Test the /convert endpoint with all combinations"""
    
    def test_decimal_to_all_formats(self, client):
        """Test converting decimal to all other formats"""
        test_cases = [
            ("42", "decimal", "text", "forty-two"),
            ("42", "decimal", "binary", "101010"),
            ("42", "decimal", "octal", "52"),
            ("42", "decimal", "hexadecimal", "2a"),
            ("42", "decimal", "decimal", "42"),
        ]
        
        for input_val, input_type, output_type, expected in test_cases:
            response = client.post('/convert', 
                json={
                    'input': input_val,
                    'inputType': input_type,
                    'outputType': output_type
                })
            data = response.get_json()
            assert data['error'] is None
            assert data['result'] == expected
    
    def test_binary_to_all_formats(self, client):
        """Test converting binary to all other formats"""
        test_cases = [
            ("101010", "binary", "decimal", "42"),
            ("101010", "binary", "text", "forty-two"),
            ("101010", "binary", "octal", "52"),
            ("101010", "binary", "hexadecimal", "2a"),
            ("101010", "binary", "binary", "101010"),
        ]
        
        for input_val, input_type, output_type, expected in test_cases:
            response = client.post('/convert', 
                json={
                    'input': input_val,
                    'inputType': input_type,
                    'outputType': output_type
                })
            data = response.get_json()
            assert data['error'] is None
            assert data['result'] == expected
    
    def test_octal_to_all_formats(self, client):
        """Test converting octal to all other formats"""
        test_cases = [
            ("52", "octal", "decimal", "42"),
            ("52", "octal", "text", "forty-two"),
            ("52", "octal", "binary", "101010"),
            ("52", "octal", "hexadecimal", "2a"),
            ("52", "octal", "octal", "52"),
        ]
        
        for input_val, input_type, output_type, expected in test_cases:
            response = client.post('/convert', 
                json={
                    'input': input_val,
                    'inputType': input_type,
                    'outputType': output_type
                })
            data = response.get_json()
            assert data['error'] is None
            assert data['result'] == expected
    
    def test_hexadecimal_to_all_formats(self, client):
        """Test converting hexadecimal to all other formats"""
        test_cases = [
            ("2a", "hexadecimal", "decimal", "42"),
            ("2a", "hexadecimal", "text", "forty-two"),
            ("2a", "hexadecimal", "binary", "101010"),
            ("2a", "hexadecimal", "octal", "52"),
            ("2a", "hexadecimal", "hexadecimal", "2a"),
        ]
        
        for input_val, input_type, output_type, expected in test_cases:
            response = client.post('/convert', 
                json={
                    'input': input_val,
                    'inputType': input_type,
                    'outputType': output_type
                })
            data = response.get_json()
            assert data['error'] is None
            assert data['result'] == expected
    
    def test_text_to_all_formats(self, client):
        """Test converting text to all other formats"""
        test_cases = [
            ("five", "text", "decimal", "5"),
            ("five", "text", "binary", "101"),
            ("five", "text", "octal", "5"),
            ("five", "text", "hexadecimal", "5"),
            ("five", "text", "text", "five"),
        ]
        
        for input_val, input_type, output_type, expected in test_cases:
            response = client.post('/convert', 
                json={
                    'input': input_val,
                    'inputType': input_type,
                    'outputType': output_type
                })
            data = response.get_json()
            assert data['error'] is None
            assert data['result'] == expected
    
    def test_base64_conversions(self, client):
        """Test base64 conversions"""
        # First convert a known number to base64, then test conversions
        number = 42
        byte_count = (number.bit_length() + 7) // 8
        if byte_count == 0:
            byte_count = 1
        number_bytes = number.to_bytes(byte_count, byteorder='little')
        b64_input = base64.b64encode(number_bytes).decode('utf-8')
        
        test_cases = [
            (b64_input, "base64", "decimal", "42"),
            (b64_input, "base64", "text", "forty-two"),
            (b64_input, "base64", "binary", "101010"),
            (b64_input, "base64", "octal", "52"),
            (b64_input, "base64", "hexadecimal", "2a"),
        ]
        
        for input_val, input_type, output_type, expected in test_cases:
            response = client.post('/convert', 
                json={
                    'input': input_val,
                    'inputType': input_type,
                    'outputType': output_type
                })
            data = response.get_json()
            assert data['error'] is None
            assert data['result'] == expected
    
    def test_decimal_to_base64(self, client):
        """Test converting decimal to base64"""
        response = client.post('/convert', 
            json={
                'input': "42",
                'inputType': "decimal",
                'outputType': "base64"
            })
        data = response.get_json()
        assert data['error'] is None
        # Verify the result can be converted back
        result_b64 = data['result']
        assert base64_to_number(result_b64) == 42
    
    def test_edge_cases(self, client):
        """Test edge cases like zero and large numbers"""
        test_cases = [
            ("0", "decimal", "text", "zero"),
            ("0", "decimal", "binary", "0"),
            ("zero", "text", "decimal", "0"),
            ("1000", "decimal", "text", "one thousand"),
        ]
        
        for input_val, input_type, output_type, expected in test_cases:
            response = client.post('/convert', 
                json={
                    'input': input_val,
                    'inputType': input_type,
                    'outputType': output_type
                })
            data = response.get_json()
            assert data['error'] is None
            assert data['result'] == expected


class TestErrorHandling:
    """Test error handling for various invalid inputs"""
    
    def test_invalid_binary_input(self, client):
        """Test invalid binary input"""
        response = client.post('/convert', 
            json={
                'input': "102",  # Invalid binary (contains 2)
                'inputType': "binary",
                'outputType': "decimal"
            })
        data = response.get_json()
        assert data['error'] is not None
        assert data['result'] is None
    
    def test_invalid_octal_input(self, client):
        """Test invalid octal input"""
        response = client.post('/convert', 
            json={
                'input': "89",  # Invalid octal (contains 8 and 9)
                'inputType': "octal",
                'outputType': "decimal"
            })
        data = response.get_json()
        assert data['error'] is not None
        assert data['result'] is None
    
    def test_invalid_hexadecimal_input(self, client):
        """Test invalid hexadecimal input"""
        response = client.post('/convert', 
            json={
                'input': "xyz",  # Invalid hex
                'inputType': "hexadecimal",
                'outputType': "decimal"
            })
        data = response.get_json()
        assert data['error'] is not None
        assert data['result'] is None
    
    def test_invalid_decimal_input(self, client):
        """Test invalid decimal input"""
        response = client.post('/convert', 
            json={
                'input': "not_a_number",
                'inputType': "decimal",
                'outputType': "binary"
            })
        data = response.get_json()
        assert data['error'] is not None
        assert data['result'] is None
    
    def test_invalid_text_input(self, client):
        """Test invalid text input"""
        response = client.post('/convert', 
            json={
                'input': "invalid_text_number",
                'inputType': "text",
                'outputType': "decimal"
            })
        data = response.get_json()
        assert data['error'] is not None
        assert data['result'] is None
    
    def test_invalid_base64_input(self, client):
        """Test invalid base64 input"""
        response = client.post('/convert', 
            json={
                'input': "invalid_base64!",
                'inputType': "base64",
                'outputType': "decimal"
            })
        data = response.get_json()
        assert data['error'] is not None
        assert data['result'] is None
    
    def test_invalid_input_type(self, client):
        """Test invalid input type"""
        response = client.post('/convert', 
            json={
                'input': "42",
                'inputType': "invalid_type",
                'outputType': "decimal"
            })
        data = response.get_json()
        assert data['error'] is not None
        assert data['result'] is None
    
    def test_invalid_output_type(self, client):
        """Test invalid output type"""
        response = client.post('/convert', 
            json={
                'input': "42",
                'inputType': "decimal",
                'outputType': "invalid_type"
            })
        data = response.get_json()
        assert data['error'] is not None
        assert data['result'] is None
    
    def test_missing_input_data(self, client):
        """Test missing input data"""
        response = client.post('/convert', json={})
        data = response.get_json()
        assert data['error'] is not None
        assert data['result'] is None


class TestWebInterface:
    """Test the web interface"""
    
    def test_index_page(self, client):
        """Test that the index page loads correctly"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Numeric Converter' in response.data
        assert b'Input Value:' in response.data
        assert b'Input Type:' in response.data
        assert b'Output Type:' in response.data


if __name__ == '__main__':
    pytest.main(['-v'])