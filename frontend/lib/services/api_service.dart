import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart' show kDebugMode; // For checking debug mode

class ApiService {
  // For Android emulator, '10.0.2.2' points to the host machine's localhost.
  // For iOS simulator, 'localhost' or '127.0.0.1' usually works.
  // For physical devices, use the actual IP address of your machine on the local network.
  // This should ideally be configurable (e.g., via environment variables or a config file).
  static const String _androidBaseUrl = "http://10.0.2.2:8000/api/v1";
  static const String _iosBaseUrl = "http://localhost:8000/api/v1";

  // A simple way to determine base URL, can be improved with TargetPlatform
  final String _baseUrl = defaultTargetPlatform == TargetPlatform.android ? _androidBaseUrl : _iosBaseUrl;


  Future<Map<String, dynamic>> _handleResponse(http.Response response) async {
    final Map<String, dynamic> responseBody = json.decode(response.body);
    if (kDebugMode) {
      print('API Response Status: ${response.statusCode}');
      print('API Response Body: $responseBody');
    }
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return responseBody;
    } else {
      // Try to get a specific error message from backend if available
      final errorMessage = responseBody['detail'] ?? 'An unknown error occurred';
      throw Exception('API Error (${response.statusCode}): $errorMessage');
    }
  }

  Future<Map<String, dynamic>> registerUser({
    required String phoneNumber,
    required String password,
    String? fullName,
    String? email,
    // String role = "customer", // Default role, or let backend handle it
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/auth/register'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String?>{
        'phone_number': phoneNumber,
        'password': password,
        'full_name': fullName,
        'email': email,
        // 'role': role, // Backend should default this or handle it based on registration type
      }),
    );
    return _handleResponse(response); // Returns the created user data
  }

  Future<Map<String, dynamic>> loginUser(String phoneNumber, String password) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/auth/token'),
      headers: <String, String>{
        'Content-Type': 'application/x-www-form-urlencoded', // As per OAuth2PasswordRequestForm
      },
      // OAuth2PasswordRequestForm expects form data
      body: {
        'username': phoneNumber, // FastAPI's OAuth2PasswordRequestForm uses 'username'
        'password': password,
        // 'scope': '', // Optional: if you use scopes
        // 'client_id': '', // Optional: if using client credentials
        // 'client_secret': '', // Optional
      },
    );
    return _handleResponse(response); // Returns token data e.g. {"access_token": "...", "token_type": "bearer"}
  }

  Future<Map<String, dynamic>> getCurrentUser(String token) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/auth/users/me'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer $token',
      },
    );
    return _handleResponse(response); // Returns current user data
  }

  // Placeholder for a potential logout API call
  // Future<void> logoutUser(String token) async {
  //   try {
  //     final response = await http.post(
  //       Uri.parse('$_baseUrl/auth/logout'), // Assuming a logout endpoint exists
  //       headers: <String, String>{
  //         'Content-Type': 'application/json; charset=UTF-8',
  //         'Authorization': 'Bearer $token',
  //       },
  //     );
  //     _handleResponse(response);
  //   } catch (e) {
  //     // Logout failure is often not critical for client, just log it
  //     if (kDebugMode) {
  //       print("Error during API logout: $e");
  //     }
  //   }
  // }
}
