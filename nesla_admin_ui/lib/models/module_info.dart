import 'package:flutter/material.dart';

enum ModuleStatus { online, warning, offline }

class ModuleInfo {
  final String name;
  final String displayName;
  final IconData icon;
  final ModuleStatus status;
  final Color accentColor;
  final double cpuUsage;
  final double memoryUsage;
  final String lastUpdate;

  const ModuleInfo({
    required this.name,
    required this.displayName,
    required this.icon,
    required this.status,
    required this.accentColor,
    required this.cpuUsage,
    required this.memoryUsage,
    required this.lastUpdate,
  });

  String get statusText {
    switch (status) {
      case ModuleStatus.online:
        return 'Online';
      case ModuleStatus.warning:
        return 'Warning';
      case ModuleStatus.offline:
        return 'Offline';
    }
  }

  static List<ModuleInfo> mockModules() {
    return const [
      ModuleInfo(
        name: 'brain',
        displayName: 'Brain',
        icon: Icons.psychology,
        status: ModuleStatus.online,
        accentColor: Color(0xFF60A5FA),
        cpuUsage: 42,
        memoryUsage: 58,
        lastUpdate: 'now',
      ),
      ModuleInfo(
        name: 'memory',
        displayName: 'Memory',
        icon: Icons.storage,
        status: ModuleStatus.online,
        accentColor: Color(0xFF22C55E),
        cpuUsage: 24,
        memoryUsage: 66,
        lastUpdate: '1 min ago',
      ),
      ModuleInfo(
        name: 'sss',
        displayName: 'SSS Monitor',
        icon: Icons.security,
        status: ModuleStatus.warning,
        accentColor: Color(0xFFF59E0B),
        cpuUsage: 35,
        memoryUsage: 48,
        lastUpdate: '2 min ago',
      ),
      ModuleInfo(
        name: 'load_balancer',
        displayName: 'Load Balancer',
        icon: Icons.hub,
        status: ModuleStatus.online,
        accentColor: Color(0xFF35D9F6),
        cpuUsage: 18,
        memoryUsage: 30,
        lastUpdate: 'now',
      ),
      ModuleInfo(
        name: 'heart',
        displayName: 'Heart',
        icon: Icons.favorite,
        status: ModuleStatus.online,
        accentColor: Color(0xFFFB7185),
        cpuUsage: 28,
        memoryUsage: 37,
        lastUpdate: 'now',
      ),
      ModuleInfo(
        name: 'mouth',
        displayName: 'Mouth',
        icon: Icons.record_voice_over,
        status: ModuleStatus.online,
        accentColor: Color(0xFFA78BFA),
        cpuUsage: 22,
        memoryUsage: 41,
        lastUpdate: 'now',
      ),
    ];
  }
}

