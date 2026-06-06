import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../services/responsive_service.dart';

class SidebarItem {
  final String label;
  final IconData icon;
  final String route;
  bool isActive;

  SidebarItem({
    required this.label,
    required this.icon,
    required this.route,
    this.isActive = false,
  });
}

class Sidebar extends StatelessWidget {
  final List<SidebarItem> items;
  final ValueChanged<String> onItemSelected;
  final bool isCollapsed;

  const Sidebar({
    super.key,
    required this.items,
    required this.onItemSelected,
    this.isCollapsed = false,
  });

  @override
  Widget build(BuildContext context) {
    if (ResponsiveService.isMobile(context)) {
      return const SizedBox.shrink();
    }

    return Container(
      width: isCollapsed ? 80 : 280,
      decoration: BoxDecoration(
        color: NeslaColors.darkBlue,
        border: Border(
          right: BorderSide(
            color: NeslaColors.cyan.withAlpha((0.2 * 255).toInt()),
            width: 1,
          ),
        ),
      ),
      child: Column(
        children: [
          // Logo Section
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              border: Border(
                bottom: BorderSide(
                  color: NeslaColors.cyan.withAlpha((0.2 * 255).toInt()),
                  width: 1,
                ),
              ),
            ),
            child: Column(
              children: [
                Container(
                  width: isCollapsed ? 50 : 80,
                  height: isCollapsed ? 50 : 80,
                  decoration: BoxDecoration(
                    gradient: NeslaColors.cyanGradient,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Center(
                    child: Text(
                      'N',
                      style: TextStyle(
                        fontSize: isCollapsed ? 24 : 32,
                        fontWeight: FontWeight.bold,
                        color: NeslaColors.deepBlue,
                      ),
                    ),
                  ),
                ),
                if (!isCollapsed)
                  const Padding(
                    padding: EdgeInsets.only(top: 16),
                    child: Text(
                      'NESLA OS',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                        color: NeslaColors.white,
                      ),
                    ),
                  ),
              ],
            ),
          ),

          // Menu Items
          Expanded(
            child: ListView(
              padding: const EdgeInsets.symmetric(vertical: 16),
              children: items
                  .map((item) => _buildMenuItem(item, isCollapsed))
                  .toList(),
            ),
          ),

          // Footer
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              border: Border(
                top: BorderSide(
                  color: NeslaColors.cyan.withAlpha((0.2 * 255).toInt()),
                  width: 1,
                ),
              ),
            ),
            child: Column(
              children: [
                if (!isCollapsed)
                  ElevatedButton(
                    onPressed: () {},
                    style: ElevatedButton.styleFrom(
                      minimumSize: const Size(double.infinity, 40),
                      backgroundColor: NeslaColors.cyan,
                      foregroundColor: NeslaColors.deepBlue,
                    ),
                    child: const Text('Settings'),
                  )
                else
                  IconButton(
                    onPressed: () {},
                    icon: const Icon(Icons.settings, color: NeslaColors.cyan),
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMenuItem(SidebarItem item, bool isCollapsed) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => onItemSelected(item.route),
          borderRadius: BorderRadius.circular(8),
          child: Container(
            padding: EdgeInsets.symmetric(
              horizontal: isCollapsed ? 16 : 16,
              vertical: 12,
            ),
            decoration: BoxDecoration(
              color: item.isActive
                  ? NeslaColors.cyan.withAlpha((0.15 * 255).toInt())
                  : Colors.transparent,
              border: item.isActive
                  ? Border.all(color: NeslaColors.cyan, width: 1)
                  : null,
              borderRadius: BorderRadius.circular(8),
            ),
            child: isCollapsed
                ? Icon(
                    item.icon,
                    color:
                        item.isActive ? NeslaColors.cyan : NeslaColors.darkGray,
                    size: 20,
                  )
                : Row(
                    children: [
                      Icon(
                        item.icon,
                        color: item.isActive
                            ? NeslaColors.cyan
                            : NeslaColors.darkGray,
                        size: 20,
                      ),
                      const SizedBox(width: 12),
                      Text(
                        item.label,
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w500,
                          color: item.isActive
                              ? NeslaColors.cyan
                              : NeslaColors.mediumGray,
                        ),
                      ),
                      const Spacer(),
                      if (item.isActive)
                        Container(
                          width: 4,
                          height: 4,
                          decoration: const BoxDecoration(
                            color: NeslaColors.cyan,
                            shape: BoxShape.circle,
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
