import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:queueme_frontend/providers/auth_provider.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});
  static const String routeName = '/home';

  @override
  Widget build(BuildContext context) {
    final authProvider = Provider.of<AuthProvider>(context);
    final user = authProvider.user;

    return Scaffold(
      appBar: AppBar(
        title: const Text('QueueMe Home'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Logout',
            onPressed: () async {
              // Add a confirmation dialog before logging out
              final confirmLogout = await showDialog<bool>(
                context: context,
                builder: (BuildContext ctx) {
                  return AlertDialog(
                    title: const Text('Confirm Logout'),
                    content: const Text('Are you sure you want to log out?'),
                    actions: <Widget>[
                      TextButton(
                        child: const Text('Cancel'),
                        onPressed: () {
                          Navigator.of(ctx).pop(false);
                        },
                      ),
                      TextButton(
                        child: const Text('Logout'),
                        onPressed: () {
                          Navigator.of(ctx).pop(true);
                        },
                      ),
                    ],
                  );
                },
              );

              if (confirmLogout == true) {
                await authProvider.logout();
                // AuthWrapper in main.dart will handle navigation to LoginScreen
              }
            },
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            if (user != null) ...[
              Text(
                'Welcome, ${user.fullName ?? user.phoneNumber}!',
                style: Theme.of(context).textTheme.headlineSmall,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              Text('User ID: ${user.id}'),
              Text('Role: ${user.role.toString().split('.').last}'), // Display role nicely
              const SizedBox(height: 20),
            ] else ...[
              const Text(
                'Welcome to QueueMe!',
                style: TextStyle(fontSize: 24),
              ),
              const SizedBox(height: 8),
              const Text("Loading user data or not logged in."),
              const SizedBox(height: 20),
            ],
            ElevatedButton(
              onPressed: () {
                // TODO: Navigate to a screen to view available queues
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('View Queues - To be implemented')),
                );
              },
              child: const Text('View Available Queues'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: () {
                // TODO: Navigate to a screen showing user's current queue entries
                 ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('My Queues - To be implemented')),
                );
              },
              child: const Text('My Queues'),
            ),
          ],
        ),
      ),
      // Example of a Floating Action Button
      // floatingActionButton: FloatingActionButton(
      //   onPressed: () {
      //     // Action for FAB
      //   },
      //   tooltip: 'Join Queue by Code',
      //   child: const Icon(Icons.qr_code_scanner),
      // ),
    );
  }
}
