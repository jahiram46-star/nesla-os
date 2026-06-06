import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../models/module_info.dart';

class StatusBadge extends StatelessWidget {
  final ModuleStatus status;
  final String label;

  const StatusBadge({
    super.key,
    required this.status,
    required this.label,
  });

  Color get statusColor {
    switch (status) {
      case ModuleStatus.online:
        return NeslaColors.onlineGreen;
      case ModuleStatus.offline:
        return NeslaColors.offlineRed;
      case ModuleStatus.warning:
        return NeslaColors.warningOrange;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: statusColor.withAlpha((0.15 * 255).toInt()),
        border: Border.all(color: statusColor, width: 1),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 8,
            height: 8,
            decoration: BoxDecoration(
              color: statusColor,
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(
                  color: statusColor.withAlpha((0.5 * 255).toInt()),
                  blurRadius: 4,
                ),
              ],
            ),
          ),
          const SizedBox(width: 6),
          Text(
            label,
            style: TextStyle(
              color: statusColor,
              fontSize: 12,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}
