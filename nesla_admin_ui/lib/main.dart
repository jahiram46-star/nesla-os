import 'package:flutter/material.dart';

import 'screens/dashboard_screen.dart';
import 'theme/colors.dart';

void main() {
  runApp(const NeslaAdminUI());
}

class NeslaAdminUI extends StatelessWidget {
  const NeslaAdminUI({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Nesla Admin UI',
      theme: ThemeData(
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: NeslaColors.cyan,
          brightness: Brightness.dark,
        ),
        scaffoldBackgroundColor: NeslaColors.deepBlue,
        useMaterial3: true,
      ),
      home: const DashboardScreen(),
    );
  }
}
