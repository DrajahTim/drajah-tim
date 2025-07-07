import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:queueme_frontend/providers/auth_provider.dart';
import 'package:queueme_frontend/screens/register_screen.dart'; // Will create this

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  static const String routeName = '/login';

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  String _phoneNumber = '';
  String _password = '';

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }
    _formKey.currentState!.save();

    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    try {
      final success = await authProvider.login(_phoneNumber, _password);
      if (!success && mounted) { // Check if widget is still in the tree
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(authProvider.errorMessage ?? 'Login failed. Please try again.'),
            backgroundColor: Colors.red,
          ),
        );
      }
      // Navigation to HomeScreen is handled by AuthWrapper in main.dart
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
      appBar: AppBar(title: const Text('Login to QueueMe')),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20.0),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: <Widget>[
                // Placeholder for a logo
                Icon(Icons.queue_play_next, size: 80, color: Theme.of(context).primaryColor),
                const SizedBox(height: 30),
                TextFormField(
                  decoration: const InputDecoration(labelText: 'Phone Number'),
                  keyboardType: TextInputType.phone,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your phone number';
                    }
                    // Basic validation, can be improved
                    if (value.length < 10) {
                        return 'Phone number seems too short';
                    }
                    return null;
                  },
                  onSaved: (value) => _phoneNumber = value!,
                ),
                const SizedBox(height: 20),
                TextFormField(
                  decoration: const InputDecoration(labelText: 'Password'),
                  obscureText: true,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your password';
                    }
                    if (value.length < 6) {
                      return 'Password must be at least 6 characters';
                    }
                    return null;
                  },
                  onSaved: (value) => _password = value!,
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
                        child: const Text('Login'),
                      ),
                const SizedBox(height: 20),
                TextButton(
                  onPressed: () {
                    // Navigate to RegisterScreen
                    Navigator.of(context).push(
                        MaterialPageRoute(builder: (_) => const RegisterScreen()) // Pushing directly for now
                    );
                    // Navigator.of(context).pushNamed(RegisterScreen.routeName); // If using named routes for this
                  },
                  child: const Text('Don\'t have an account? Register'),
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
