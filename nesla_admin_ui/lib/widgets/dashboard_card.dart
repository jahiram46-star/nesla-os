import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../models/module_info.dart';
import 'status_badge.dart';

class DashboardCard extends StatelessWidget {
  final ModuleInfo module;
  final VoidCallback? onTap;

  const DashboardCard({
    super.key,
    required this.module,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: module.accentColor.withAlpha((0.4 * 255).toInt()),
            width: 1,
          ),
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              NeslaColors.darkBlue.withAlpha((0.8 * 255).toInt()),
              NeslaColors.mediumBlue.withAlpha((0.5 * 255).toInt()),
            ],
          ),
          boxShadow: [
            BoxShadow(
              color: module.accentColor.withAlpha((0.1 * 255).toInt()),
              blurRadius: 16,
              spreadRadius: 0,
            ),
          ],
        ),
        child: Stack(
          children: [
            // Background blur effect decoration
            Positioned(
              top: -50,
              right: -50,
              child: Container(
                width: 150,
                height: 150,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: RadialGradient(
                    colors: [
                      module.accentColor.withAlpha((0.1 * 255).toInt()),
                      Colors.transparent,
                    ],
                  ),
                ),
              ),
            ),

            // Content
            Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  // Header
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: module.accentColor.withAlpha((0.15 * 255).toInt()),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Icon(
                          module.icon,
                          color: module.accentColor,
                          size: 24,
                        ),
                      ),
                      StatusBadge(
                        status: module.status,
                        label: module.statusText,
                      ),
                    ],
                  ),

                  // Title
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        module.displayName,
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                          color: NeslaColors.white,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Updated ${module.lastUpdate}',
                        style: const TextStyle(
                          fontSize: 12,
                          color: NeslaColors.darkGray,
                        ),
                      ),
                    ],
                  ),

                  // Stats
                  Column(
                    children: [
                      StatRow(
                        label: 'CPU',
                        value: '${module.cpuUsage.toStringAsFixed(1)}%',
                        percentage: module.cpuUsage / 100,
                        color: module.accentColor,
                      ),
                      const SizedBox(height: 12),
                      StatRow(
                        label: 'Memory',
                        value: '${module.memoryUsage.toStringAsFixed(1)}%',
                        percentage: module.memoryUsage / 100,
                        color: module.accentColor,
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class StatRow extends StatelessWidget {
  final String label;
  final String value;
  final double percentage;
  final Color color;

  const StatRow({
    super.key,
    required this.label,
    required this.value,
    required this.percentage,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              label,
              style: const TextStyle(
                fontSize: 12,
                color: NeslaColors.darkGray,
                fontWeight: FontWeight.w500,
              ),
            ),
            Text(
              value,
              style: const TextStyle(
                fontSize: 12,
                color: NeslaColors.white,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
        const SizedBox(height: 4),
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: LinearProgressIndicator(
            value: percentage,
            backgroundColor: NeslaColors.mediumBlue.withAlpha((0.5 * 255).toInt()),
            valueColor: AlwaysStoppedAnimation<Color>(color),
            minHeight: 4,
          ),
        ),
      ],
    );
  }
}
