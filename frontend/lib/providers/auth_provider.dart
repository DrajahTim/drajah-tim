import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart'; // Will be created in the next step
import '../models/user_model.dart';

class AuthProvider with ChangeNotifier {
  late ApiService _apiService; // Instantiated in constructor or via DI

  String? _token;
  UserModel? _user;
  bool _isLoading = false;
  String? _errorMessage;

  String? get token => _token;
  UserModel? get user => _user;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  bool get isAuthenticated => _token != null && _user != null;

  // Constructor - ApiService can be injected for testability
  AuthProvider({ApiService? apiService}) {
    _apiService = apiService ?? ApiService();
    _tryAutoLogin(); // Attempt to log in from stored token on initialization
  }

  Future<void> _tryAutoLogin() async {
    _isLoading = true;
    notifyListeners();
    try {
      final prefs = await SharedPreferences.getInstance();
      final storedToken = prefs.getString('authToken');
      if (storedToken == null || storedToken.isEmpty) {
        _isLoading = false;
        notifyListeners();
        return;
      }

      // Validate token by fetching user data
      final userData = await _apiService.getCurrentUser(storedToken);
      _user = UserModel.fromJson(userData);
      _token = storedToken;
      _errorMessage = null;
    } catch (e) {
      // If token is invalid or fetching user fails, clear token
      await logout(); // Ensure clean state
      _errorMessage = "Session expired. Please log in again.";
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> login(String phoneNumber, String password) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final tokenData = await _apiService.loginUser(phoneNumber, password);
      _token = tokenData['access_token']; // Assuming token is in 'access_token' field

      if (_token == null) {
        throw Exception("Login failed: Token not received.");
      }

      // Store token
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('authToken', _token!);

      // Fetch user details
      final userData = await _apiService.getCurrentUser(_token!);
      _user = UserModel.fromJson(userData);

      _isLoading = false;
      _errorMessage = null;
      notifyListeners();
      return true;
    } catch (e) {
      _isLoading = false;
      _errorMessage = "Login failed: ${e.toString()}";
      _token = null;
      _user = null;
      notifyListeners();
      return false;
    }
  }

  Future<bool> register({
    required String phoneNumber,
    required String password,
    String? fullName,
    String? email,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      // The registerUser method in ApiService should return the created user data
      final userData = await _apiService.registerUser(
        phoneNumber: phoneNumber,
        password: password,
        fullName: fullName,
        email: email,
      );
      // Optionally, log the user in directly after registration
      // For now, we'll just indicate success and they can log in separately.
      // Or, if your backend returns a token on register:
      // _token = userData['token']; // if token is returned
      // _user = UserModel.fromJson(userData['user']); // if user data is nested
      // final prefs = await SharedPreferences.getInstance();
      // await prefs.setString('authToken', _token!);

      _isLoading = false;
      _errorMessage = null;
      notifyListeners();
      // Consider auto-login here by calling login() or by backend returning a token
      return true;
    } catch (e) {
      _isLoading = false;
      _errorMessage = "Registration failed: ${e.toString()}";
      notifyListeners();
      return false;
    }
  }

  Future<void> logout() async {
    _isLoading = true;
    notifyListeners();

    _token = null;
    _user = null;
    _errorMessage = null;

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('authToken');
    // Optionally call a backend logout endpoint if you have one
    // await _apiService.logoutUser(_token); // If such an endpoint exists

    _isLoading = false;
    notifyListeners();
  }

  void clearErrorMessage() {
    _errorMessage = null;
    notifyListeners();
  }
}

// UserModel is now in a separate file: models/user_model.dart
