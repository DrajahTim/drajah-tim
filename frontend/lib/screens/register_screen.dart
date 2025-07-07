import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:queueme_frontend/providers/auth_provider.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});
  static const String routeName = '/register';

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  String _phoneNumber = '';
  String _password = '';
  String _confirmPassword = '';
  String? _fullName = '';
  String? _email = '';

  Future<void> _submit() async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    if (!_formKey.currentState!.validate()) {
      return;
    }
    _formKey.currentState!.save();

    if (_password != _confirmPassword) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Passwords do not match!'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    try {
      final success = await authProvider.register(
        phoneNumber: _phoneNumber,
        password: _password,
        fullName: _fullName,
        email: _email,
      );

      if (success && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Registration successful! Please login.'),
            backgroundColor: Colors.green,
          ),
        );
        Navigator.of(context).pop(); // Go back to login screen
      } else if (!success && mounted) {
         ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(authProvider.errorMessage ?? 'Registration failed. Please try again.'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } catch (error) {
       if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
           SnackBar(
            content: Text('An unexpected error occurred: ${error.toString()}'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final authProvider = Provider.of<AuthProvider>(context); // For isLoading

    return Scaffold(
      appBar: AppBar(title: const Text('Register for QueueMe')),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20.0),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: <Widget>[
                TextFormField(
                  decoration: const InputDecoration(labelText: 'Phone Number*'),
                  keyboardType: TextInputType.phone,
                  validator: (value) {
                    if (value == null || value.isEmpty) return 'Phone number is required';
                    if (value.length < 10) return 'Phone number too short';
                    return null;
                  },
                  onSaved: (value) => _phoneNumber = value!,
                ),
                const SizedBox(height: 15),
                TextFormField(
                  decoration: const InputDecoration(labelText: 'Full Name (Optional)'),
                  onSaved: (value) => _fullName = value,
                ),
                const SizedBox(height: 15),
                TextFormField(
                  decoration: const InputDecoration(labelText: 'Email (Optional)'),
                  keyboardType: TextInputType.emailAddress,
                  validator: (value) {
                    if (value != null && value.isNotEmpty && !value.contains('@')) {
                      return 'Please enter a valid email';
                    }
                    return null;
                  },
                  onSaved: (value) => _email = value,
                ),
                const SizedBox(height: 15),
                TextFormField(
                  decoration: const InputDecoration(labelText: 'Password*'),
                  obscureText: true,
                  validator: (value) {
                    if (value == null || value.isEmpty) return 'Password is required';
                    if (value.length < 6) return 'Password must be at least 6 characters';
                    _password = value; // Store it for confirm password validation
                    return null;
                  },
                  onSaved: (value) => _password = value!,
                ),
                const SizedBox(height: 15),
                TextFormField(
                  decoration: const InputDecoration(labelText: 'Confirm Password*'),
                  obscureText: true,
                  validator: (value) {
                    if (value == null || value.isEmpty) return 'Please confirm your password';
                    if (value != _password) return 'Passwords do not match';
                    return null;
                  },
                  onSaved: (value) => _confirmPassword = value!,
                ),
                const SizedBox(height: 30),
                authProvider.isLoading
                    ? const Center(child: CircularProgressIndicator())
                    : ElevatedButton(
                        onPressed: _submit,
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 15),
                          textStyle: const TextStyle(fontSize: 18),
                        ),
                        child: const Text('Register'),
                      ),
                const SizedBox(height: 15),
                TextButton(
                  onPressed: () {
                    Navigator.of(context).pop(); // Go back to Login Screen
                  },
                  child: const Text('Already have an account? Login'),
                ),
                 if (authProvider.errorMessage != null && !authProvider.isLoading)
                  Padding(
                    padding: const EdgeInsets.only(top: 15.0),
                    child: Text(
                      authProvider.errorMessage!,
                      style: const TextStyle(color: Colors.red, fontSize: 14),
                      textAlign: TextAlign.center,
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
