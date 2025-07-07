import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:queueme_frontend/providers/auth_provider.dart';
import 'package:queueme_frontend/screens/home_screen.dart';
import 'package:queueme_frontend/screens/login_screen.dart';
import 'package:queueme_frontend/screens/splash_screen.dart'; // Will create this

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => AuthProvider(), // Initialize AuthProvider
      child: MaterialApp(
        title: 'QueueMe',
        theme: ThemeData(
          primarySwatch: Colors.teal, // Changed theme color for a fresh look
          visualDensity: VisualDensity.adaptivePlatformDensity,
          buttonTheme: ButtonThemeData(
            buttonColor: Colors.teal,
            textTheme: ButtonTextTheme.primary,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8.0),
            ),
          ),
          inputDecorationTheme: InputDecorationTheme(
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8.0),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8.0),
              borderSide: const BorderSide(color: Colors.teal, width: 2.0),
            ),
          ),
        ),
        // The initial screen logic will be handled by AuthWrapper or SplashScreen
        // For now, let's set up a basic home and routes
        home: const AuthWrapper(), // This will decide to show Login or Home
        // Define routes for easier navigation if needed, though direct navigation is also used.
        // For simple apps, direct navigation (MaterialPageRoute) is fine.
        // For larger apps, consider a routing package like go_router.
        routes: {
          SplashScreen.routeName: (ctx) => const SplashScreen(),
          LoginScreen.routeName: (ctx) => const LoginScreen(),
          HomeScreen.routeName: (ctx) => const HomeScreen(),
          // RegisterScreen.routeName is not added here as it's typically pushed
          // as a sub-route from LoginScreen, but can be added if direct access is needed.
        },
      ),
    );
  }
}

// This widget will listen to AuthProvider and show appropriate screen
class AuthWrapper extends StatelessWidget {
  const AuthWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    // Using Consumer to react to changes in AuthProvider
    return Consumer<AuthProvider>(
      builder: (context, auth, child) {
        if (auth.isLoading && auth.token == null) { // Initial loading state (e.g. trying auto-login)
          return const SplashScreen(); // Show splash screen during initial auth check
        } else if (auth.isAuthenticated) {
          return const HomeScreen();
        } else {
          return const LoginScreen();
        }
      },
    );
  }
}

// MyHomePage is removed as AuthWrapper and specific screens will handle UI
// We will create LoginScreen, HomeScreen, SplashScreen in subsequent steps.
