// frontend/lib/models/user_model.dart
import 'package:flutter/foundation.dart';

// Matches the UserRole enum in the backend (models/user.py and schemas/user.py)
enum UserRole {
  customer,
  businessAdmin,
  staff,
  superAdmin,
  unknown // Fallback for unexpected roles
}

UserRole userRoleFromString(String roleString) {
  switch (roleString.toLowerCase()) {
    case 'customer':
      return UserRole.customer;
    case 'business_admin': // Ensure this matches your backend string
      return UserRole.businessAdmin;
    case 'staff':
      return UserRole.staff;
    case 'super_admin': // Ensure this matches your backend string
      return UserRole.superAdmin;
    default:
      if (kDebugMode) {
        print("Unknown user role string: $roleString");
      }
      return UserRole.unknown;
  }
}

String userRoleToString(UserRole role) {
  switch (role) {
    case UserRole.customer:
      return 'customer';
    case UserRole.businessAdmin:
      return 'business_admin';
    case UserRole.staff:
      return 'staff';
    case UserRole.superAdmin:
      return 'super_admin';
    case UserRole.unknown:
      return 'unknown';
  }
}


class UserModel {
  final String id; // Assuming UUID from backend is string here
  final String phoneNumber;
  final String? fullName;
  final String? email;
  final UserRole role;
  final DateTime createdAt;
  final DateTime updatedAt;

  UserModel({
    required this.id,
    required this.phoneNumber,
    this.fullName,
    this.email,
    required this.role,
    required this.createdAt,
    required this.updatedAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      phoneNumber: json['phone_number'] as String,
      fullName: json['full_name'] as String?,
      email: json['email'] as String?,
      role: userRoleFromString(json['role'] as String),
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'phone_number': phoneNumber,
      'full_name': fullName,
      'email': email,
      'role': userRoleToString(role),
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}
