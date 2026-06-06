import 'package:flutter/material.dart';
import 'dart:ui' as ui;
import '../theme/colors.dart';
import '../models/module_info.dart';
import '../widgets/sidebar.dart';
import '../widgets/dashboard_card.dart';
import '../services/responsive_service.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  late List<ModuleInfo> modules;
  late List<SidebarItem> sidebarItems;
  String selectedRoute = 'dashboard';
  bool sidebarCollapsed = false;

  @override
  void initState() {
    super.initState();
    modules = ModuleInfo.mockModules();
    _initializeSidebarItems();
  }

  void _initializeSidebarItems() {
    sidebarItems = [
      SidebarItem(
        label: 'Dashboard',
        icon: Icons.dashboard,
        route: 'dashboard',
        isActive: true,
      ),
      SidebarItem(
        label: 'Brain',
        icon: Icons.psychology,
        route: 'brain',
      ),
      SidebarItem(
        label: 'Memory',
        icon: Icons.storage,
        route: 'memory',
      ),
      SidebarItem(
        label: 'Knowledge',
        icon: Icons.library_books,
        route: 'knowledge',
      ),
      SidebarItem(
        label: 'Documents',
        icon: Icons.description,
        route: 'documents',
      ),
      SidebarItem(
        label: 'SSS Monitor',
        icon: Icons.security,
        route: 'sss',
      ),
      SidebarItem(
        label: 'Heart',
        icon: Icons.favorite,
        route: 'heart',
      ),
      SidebarItem(
        label: 'Mouth',
        icon: Icons.message,
        route: 'mouth',
      ),
      SidebarItem(
        label: 'Eyes',
        icon: Icons.remove_red_eye,
        route: 'eyes',
      ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    final isMobile = ResponsiveService.isMobile(context);
    final isTablet = ResponsiveService.isTablet(context);
    final isWeb = ResponsiveService.isWeb(context);

    return Scaffold(
      backgroundColor: NeslaColors.deepBlue,
      body: Stack(
        children: [
          // Futuristic Background
          _buildFutureristicBackground(),

          // Main Layout
          Row(
            children: [
              // Sidebar
              if (!isMobile)
                Sidebar(
                  items: sidebarItems,
                  isCollapsed: isTablet,
                  onItemSelected: (route) {
                    setState(() {
                      selectedRoute = route;
                      // Update sidebar items active state
                      for (var item in sidebarItems) {
                        item.isActive = item.route == route;
                      }
                    });
                  },
                ),

              // Main Content
              Expanded(
                child: Column(
                  children: [
                    // Top Header
                    _buildTopHeader(isMobile, isTablet),

                    // Dashboard Content
                    Expanded(
                      child: SingleChildScrollView(
                        padding: EdgeInsets.all(
                          ResponsiveService.getResponsivePadding(context),
                        ),
                        child: _buildDashboardContent(context),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),

      // Mobile Bottom Navigation
      bottomNavigationBar: isMobile ? _buildMobileBottomNav(context) : null,
    );
  }

  Widget _buildFutureristicBackground() {
    return Container(
      color: NeslaColors.deepBlue,
      child: Stack(
        children: [
          // Neural Network Pattern
          Opacity(
            opacity: 0.08,
            child: CustomPaint(
              painter: NeuralNetworkPainter(),
              size: Size.infinite,
            ),
          ),

          // Gradient Overlay
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [
                  NeslaColors.cyan.withAlpha((0.05 * 255).toInt()),
                  NeslaColors.mediumBlue.withAlpha((0.08 * 255).toInt()),
                ],
                stops: const [0.0, 1.0],
              ),
            ),
          ),

          // Blur Effect
          BackdropFilter(
            filter: ui.ImageFilter.blur(sigmaX: 0.5, sigmaY: 0.5),
            child: Container(
              color: Colors.transparent,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTopHeader(bool isMobile, bool isTablet) {
    return Container(
      padding: EdgeInsets.all(
        ResponsiveService.getResponsivePadding(context),
      ),
      decoration: BoxDecoration(
        border: Border(
          bottom: BorderSide(
            color: NeslaColors.cyan.withAlpha((0.2 * 255).toInt()),
            width: 1,
          ),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          // Title
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'NESLA OS',
                style: Theme.of(context).textTheme.displayMedium,
              ),
              const SizedBox(height: 4),
              const Text(
                'AI Operating System Dashboard',
                style: TextStyle(
                  fontSize: 14,
                  color: NeslaColors.darkGray,
                ),
              ),
            ],
          ),

          // Right Section
          Row(
            children: [
              if (!isMobile)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: NeslaColors.onlineGreen.withAlpha((0.1 * 255).toInt()),
                    border: Border.all(
                      color: NeslaColors.onlineGreen,
                      width: 1,
                    ),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Row(
                    children: [
                      Icon(
                        Icons.circle,
                        size: 8,
                        color: NeslaColors.onlineGreen,
                      ),
                      SizedBox(width: 8),
                      Text(
                        'All Systems Online',
                        style: TextStyle(
                          color: NeslaColors.onlineGreen,
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                ),
              const SizedBox(width: 16),
              IconButton(
                onPressed: () {},
                icon: const Icon(Icons.notifications, color: NeslaColors.cyan),
              ),
              const SizedBox(width: 8),
              Container(
                width: isMobile ? 32 : 40,
                height: isMobile ? 32 : 40,
                decoration: BoxDecoration(
                  gradient: NeslaColors.cyanGradient,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Center(
                  child: Text(
                    'A',
                    style: TextStyle(
                      fontSize: isMobile ? 14 : 18,
                      fontWeight: FontWeight.bold,
                      color: NeslaColors.deepBlue,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildDashboardContent(BuildContext context) {
    final gridColumns = ResponsiveService.getGridColumns(context);
    final padding = ResponsiveService.getResponsivePadding(context);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // System Status Section
        Text(
          'Module Status',
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const SizedBox(height: 16),

        // Grid of Module Cards
        GridView.builder(
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: gridColumns,
            crossAxisSpacing: padding,
            mainAxisSpacing: padding,
            childAspectRatio: gridColumns == 1 ? 2.5 : 1.2,
          ),
          itemCount: modules.length,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemBuilder: (context, index) {
            return DashboardCard(
              module: modules[index],
              onTap: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Opening ${modules[index].displayName}...'),
                    duration: const Duration(milliseconds: 1500),
                    backgroundColor: modules[index].accentColor,
                  ),
                );
              },
            );
          },
        ),

        const SizedBox(height: 32),

        // System Events Section
        Text(
          'Recent System Events',
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const SizedBox(height: 16),

        // Events List
        _buildEventsList(context),
      ],
    );
  }

  Widget _buildEventsList(BuildContext context) {
    final events = [
      _EventItem(
        title: 'Brain Module Optimization',
        description: 'Processing efficiency increased by 15%',
        time: '2 min ago',
        icon: Icons.psychology,
        color: const Color(0xFF3B82F6),
      ),
      _EventItem(
        title: 'Memory Checkpoint Created',
        description: 'Full system memory snapshot saved',
        time: '5 min ago',
        icon: Icons.storage,
        color: const Color(0xFF10B981),
      ),
      _EventItem(
        title: 'Knowledge Base Indexed',
        description: '1,247 documents indexed successfully',
        time: '12 min ago',
        icon: Icons.library_books,
        color: const Color(0xFFF59E0B),
      ),
      _EventItem(
        title: 'Heart Analysis Complete',
        description: 'Emotion patterns detected in recent interactions',
        time: '18 min ago',
        icon: Icons.favorite,
        color: const Color(0xFFDC2626),
      ),
    ];

    return ListView.builder(
      itemCount: events.length,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemBuilder: (context, index) => _buildEventItem(events[index], index),
    );
  }

  Widget _buildEventItem(_EventItem event, int index) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: NeslaColors.darkBlue.withAlpha((0.6 * 255).toInt()),
        border: Border.all(
          color: event.color.withAlpha((0.2 * 255).toInt()),
          width: 1,
        ),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              color: event.color.withAlpha((0.15 * 255).toInt()),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(event.icon, color: event.color, size: 24),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  event.title,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: NeslaColors.white,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  event.description,
                  style: const TextStyle(
                    fontSize: 12,
                    color: NeslaColors.darkGray,
                  ),
                ),
              ],
            ),
          ),
          Text(
            event.time,
            style: const TextStyle(
              fontSize: 12,
              color: NeslaColors.darkGray,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMobileBottomNav(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        border: Border(
          top: BorderSide(
            color: NeslaColors.cyan.withAlpha((0.2 * 255).toInt()),
            width: 1,
          ),
        ),
        color: NeslaColors.darkBlue,
      ),
      child: BottomNavigationBar(
        backgroundColor: NeslaColors.darkBlue,
        selectedItemColor: NeslaColors.cyan,
        unselectedItemColor: NeslaColors.darkGray,
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.dashboard),
            label: 'Dashboard',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.psychology),
            label: 'Brain',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.storage),
            label: 'Memory',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.security),
            label: 'SSS',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.more_horiz),
            label: 'More',
          ),
        ],
      ),
    );
  }
}

// Event Model
class _EventItem {
  final String title;
  final String description;
  final String time;
  final IconData icon;
  final Color color;

  _EventItem({
    required this.title,
    required this.description,
    required this.time,
    required this.icon,
    required this.color,
  });
}

// Neural Network Background Painter
class NeuralNetworkPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = NeslaColors.cyan.withAlpha((0.5 * 255).toInt())
      ..strokeWidth = 1.0;

    final pointPaint = Paint()
      ..color = NeslaColors.cyan.withAlpha((0.8 * 255).toInt())
      ..style = PaintingStyle.fill;

    // Create neural network pattern
    const rows = 8;
    const cols = 12;
    final cellWidth = size.width / cols;
    final cellHeight = size.height / rows;

    for (int i = 0; i < rows; i++) {
      for (int j = 0; j < cols; j++) {
        final x = j * cellWidth + cellWidth / 2;
        final y = i * cellHeight + cellHeight / 2;

        // Draw nodes
        canvas.drawCircle(Offset(x, y), 2, pointPaint);

        // Draw connections
        if (j < cols - 1) {
          canvas.drawLine(
            Offset(x, y),
            Offset((j + 1) * cellWidth + cellWidth / 2, y),
            paint,
          );
        }
        if (i < rows - 1) {
          canvas.drawLine(
            Offset(x, y),
            Offset(x, (i + 1) * cellHeight + cellHeight / 2),
            paint,
          );
        }
      }
    }
  }

  @override
  bool shouldRepaint(NeuralNetworkPainter oldDelegate) => false;
}
