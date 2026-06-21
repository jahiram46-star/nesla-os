import 'package:flutter/material.dart';

class NeslaColors {
  static const deepBlue = Color(0xFF07111F);
  static const darkBlue = Color(0xFF0B1B2E);
  static const mediumBlue = Color(0xFF12365A);
  static const cyan = Color(0xFF35D9F6);
  static const white = Color(0xFFF7FBFF);
  static const darkGray = Color(0xFF8EA3B8);
  static const mediumGray = Color(0xFFB7C7D6);
  static const onlineGreen = Color(0xFF22C55E);
  static const offlineRed = Color(0xFFEF4444);
  static const warningOrange = Color(0xFFF59E0B);

  static const cyanGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [cyan, Color(0xFF60A5FA)],
  );
}

