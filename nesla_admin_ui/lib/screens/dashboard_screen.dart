import 'package:flutter/material.dart';
import 'dart:ui' as ui;
import '../theme/colors.dart';
import '../models/module_info.dart';
import '../widgets/sidebar.dart';
import '../widgets/dashboard_card.dart';
import '../widgets/browser_access_panel.dart';
import '../services/admin_api.dart';
import '../services/api_config.dart';
import '../services/responsive_service.dart';
import 'load_balancer_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final adminApi = AdminApi();
  final openrouterApiKeyController = TextEditingController();
  final openrouterBaseUrlController = TextEditingController();
  final openrouterModelIdsController = TextEditingController();
  final openrouterFallbackModelIdsController = TextEditingController();
  final openrouterAppNameController = TextEditingController();
  final openrouterRefererController = TextEditingController();
  final openrouterTimeoutController = TextEditingController();
  late List<ModuleInfo> modules;
  late List<SidebarItem> sidebarItems;
  String selectedRoute = 'dashboard';
  bool sidebarCollapsed = false;
  bool envLoading = true;
  String? envStatus;

  @override
  void initState() {
    super.initState();
    modules = ModuleInfo.mockModules();
    _initializeSidebarItems();
    _loadEnv();
  }

  @override
  void dispose() {
    openrouterApiKeyController.dispose();
    openrouterBaseUrlController.dispose();
    openrouterModelIdsController.dispose();
    openrouterFallbackModelIdsController.dispose();
    openrouterAppNameController.dispose();
    openrouterRefererController.dispose();
    openrouterTimeoutController.dispose();
    super.dispose();
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
        label: 'Load Balancer',
        icon: Icons.hub,
        route: 'load_balancer',
      ),
      SidebarItem(
        label: 'LLM Env',
        icon: Icons.settings,
        route: 'env',
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

  Future<void> _loadEnv() async {
    setState(() {
      envLoading = true;
      envStatus = null;
    });
    try {
      final env = await adminApi.fetchEnvConfig();
      openrouterApiKeyController.text = env.openrouterApiKey;
      openrouterBaseUrlController.text = env.openrouterBaseUrl;
      openrouterModelIdsController.text = env.openrouterModelIds;
      openrouterFallbackModelIdsController.text = env.openrouterFallbackModelIds;
      openrouterAppNameController.text = env.openrouterAppName;
      openrouterRefererController.text = env.openrouterReferer;
      openrouterTimeoutController.text = env.openrouterTimeoutSeconds;
    } catch (_) {
      envStatus = 'Env load failed';
    } finally {
      setState(() => envLoading = false);
    }
  }

  Future<void> _saveEnv() async {
    setState(() => envStatus = null);
    try {
      await adminApi.saveEnvConfig(
        AdminEnvConfig(
          openrouterApiKey: openrouterApiKeyController.text.trim(),
          openrouterBaseUrl: openrouterBaseUrlController.text.trim(),
          openrouterModelIds: openrouterModelIdsController.text.trim(),
          openrouterFallbackModelIds: openrouterFallbackModelIdsController.text.trim(),
          openrouterAppName: openrouterAppNameController.text.trim(),
          openrouterReferer: openrouterRefererController.text.trim(),
          openrouterTimeoutSeconds: openrouterTimeoutController.text.trim(),
        ),
      );
      setState(() => envStatus = 'Saved to .env');
    } catch (_) {
      setState(() => envStatus = 'Save failed');
    }
  }

  @override
  Widget build(BuildContext context) {
    final isMobile = ResponsiveService.isMobile(context);
    final isTablet = ResponsiveService.isTablet(context);
    return Scaffold(
      backgroundColor: NeslaColors.deepBlue,
      drawer: isMobile ? _buildMobileDrawer(context) : null,
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
                        child: selectedRoute == 'load_balancer'
                            ? const LoadBalancerScreen()
                            : selectedRoute == 'env'
                                ? _buildEnvPanel(context)
                                : _buildDashboardContent(context),
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
          if (isMobile)
            Builder(
              builder: (context) => IconButton(
                onPressed: () => Scaffold.of(context).openDrawer(),
                icon: const Icon(Icons.menu, color: NeslaColors.cyan),
              ),
            ),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'NESLA OS',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: Theme.of(context).textTheme.displayMedium?.copyWith(
                        fontSize: isMobile ? 24 : null,
                      ),
                ),
                const SizedBox(height: 4),
                const Text(
                  'AI Operating System Dashboard',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(
                    fontSize: 14,
                    color: NeslaColors.darkGray,
                  ),
                ),
              ],
            ),
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
              Tooltip(
                message: 'Open NESLA Browser Access',
                child: IconButton(
                  onPressed: _showBrowserAccess,
                  icon: const Icon(Icons.travel_explore, color: NeslaColors.cyan),
                ),
              ),
              const SizedBox(width: 8),
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
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildCommandBoard(context),
        const SizedBox(height: 18),
        _buildQuickStatsRow(context),
        const SizedBox(height: 18),
        _buildEventRail(context),
      ],
    );
  }

  Widget _buildCommandBoard(BuildContext context) {
    final isMobile = ResponsiveService.isMobile(context);
    final isTablet = ResponsiveService.isTablet(context);
    final width = MediaQuery.of(context).size.width;
    final twoColumn = width > 1000;

    final topModules = [
      _ModuleTileSpec('BRAIN V 02', 'FLOW: FOUNDATION', 'FLOW: ALONE', Icons.psychology, const Color(0xFFFFA9A9), 'brain'),
      _ModuleTileSpec('HEART V 02', 'FLOW: FOUNDATION', 'FLOW: BRAIN+MOUTH', Icons.favorite, const Color(0xFFFF5A5A), 'heart'),
      _ModuleTileSpec('MOUTH V 02', 'FLOW: FOUNDATION', 'FLOW: BRAIN+HEART', Icons.record_voice_over, const Color(0xFFFF6FB3), 'mouth'),
      _ModuleTileSpec('EYES V 02', 'FLOW: FOUNDATION', 'FLOW: BRAIN', Icons.remove_red_eye, const Color(0xFFF5F5F5), 'eyes'),
    ];
    final middleModules = [
      _ModuleTileSpec('SSS V 02', 'FLOW: FOUNDATION', 'FLOW: ALONE', Icons.security, const Color(0xFFF8F8F8), 'sss'),
      _ModuleTileSpec('IVR', 'FLOW: FOUNDATION', 'FLOW: SSS', Icons.call, const Color(0xFFF8F8F8), 'ivr'),
      _ModuleTileSpec('LOGIN', 'FLOW: FOUNDATION', 'FLOW: SSS', Icons.login, const Color(0xFFF8F8F8), 'login'),
      _ModuleTileSpec('monitoring', 'FLOW: FOUNDATION', 'FLOW: SSS', Icons.monitor_heart, const Color(0xFFF8F8F8), 'monitoring'),
    ];

    return Container(
      width: double.infinity,
      padding: EdgeInsets.all(isMobile ? 14 : 18),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: NeslaColors.cyan.withAlpha((0.22 * 255).toInt())),
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            NeslaColors.darkBlue.withAlpha(210),
            const Color(0xFF050B12).withAlpha(238),
          ],
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withAlpha(100),
            blurRadius: 26,
            offset: const Offset(0, 18),
          ),
        ],
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _glassBadge('NESLA.COM', 'DESKTOP (4K)', '3840x2160'),
              Text(
                'DASHBOARD',
                style: Theme.of(context).textTheme.displayMedium?.copyWith(
                      color: NeslaColors.cyan,
                      fontSize: isMobile ? 30 : 42,
                      letterSpacing: 1.6,
                    ),
              ),
              _glassBadge('ECOSYSTEM', 'LIVE', 'SYNC'),
            ],
          ),
          const SizedBox(height: 16),
          Stack(
            children: [
              Positioned.fill(
                child: Opacity(
                  opacity: 0.14,
                  child: ImageFiltered(
                    imageFilter: ui.ImageFilter.blur(sigmaX: 1.0, sigmaY: 1.0),
                    child: Container(
                      decoration: BoxDecoration(
                        gradient: RadialGradient(
                          colors: [
                            NeslaColors.cyan.withAlpha((0.15 * 255).toInt()),
                            Colors.transparent,
                          ],
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              Column(
                children: [
                  GridView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: topModules.length,
                    gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: isMobile ? 1 : (twoColumn ? 4 : 2),
                      crossAxisSpacing: 14,
                      mainAxisSpacing: 14,
                      childAspectRatio: isTablet ? 1.65 : 2.2,
                    ),
                    itemBuilder: (context, index) => _moduleTile(topModules[index]),
                  ),
                  const SizedBox(height: 14),
                  GridView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: middleModules.length,
                    gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: isMobile ? 1 : (twoColumn ? 4 : 2),
                      crossAxisSpacing: 14,
                      mainAxisSpacing: 14,
                      childAspectRatio: isTablet ? 1.65 : 2.2,
                    ),
                    itemBuilder: (context, index) => _moduleTile(middleModules[index]),
                  ),
                ],
              ),
              if (!isMobile)
                Positioned(
                  right: 0,
                  top: 30,
                  bottom: 30,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: const [
                      _VerticalLaneLabel('ECOSYSTEM'),
                      _VerticalLaneLabel('SECURITY'),
                    ],
                  ),
                ),
            ],
          ),
          const SizedBox(height: 18),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: const [
              _CenterFlowTag('MRM'),
            ],
          ),
          const SizedBox(height: 18),
          Wrap(
            spacing: 12,
            runSpacing: 12,
            alignment: WrapAlignment.center,
            children: const [
              _KeyChip('DATE'),
              _KeyChip('SSPG'),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildQuickStatsRow(BuildContext context) {
    return Row(
      children: [
        Expanded(child: _statCard('Brain', 'Foundation', 'ALONE', Icons.psychology, const Color(0xFFFFA9A9))),
        const SizedBox(width: 12),
        Expanded(child: _statCard('SSS', 'Foundation', 'SECURITY', Icons.security, const Color(0xFFF8F8F8))),
        const SizedBox(width: 12),
        Expanded(child: _statCard('Load Balancer', 'Routes', 'LIVE', Icons.hub, NeslaColors.cyan)),
      ],
    );
  }

  Widget _buildEventRail(BuildContext context) {
    return _panel(
      'Recent System Events',
      _buildEventsList(context),
    );
  }

  Widget _buildEnvPanel(BuildContext context) {
    if (envLoading) {
      return const Center(child: CircularProgressIndicator(color: NeslaColors.cyan));
    }
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('LLM Env Manager', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 8),
        const Text(
          'OpenRouter model list ekhane update korle backend next request e latest list auto-read korbe.',
          style: TextStyle(color: NeslaColors.darkGray),
        ),
        const SizedBox(height: 10),
        _panel(
          'Mobile Backend URL',
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                ApiConfig.defaultBaseUrl,
                style: const TextStyle(color: NeslaColors.white, fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 6),
              const Text(
                'Android emulator: 10.0.2.2 | iOS simulator: 127.0.0.1 | physical device: --dart-define=NESLA_API_BASE_URL=http://YOUR_IP:8000',
                style: TextStyle(color: NeslaColors.darkGray),
              ),
            ],
          ),
        ),
        if (envStatus != null) ...[
          const SizedBox(height: 8),
          Text(envStatus!, style: const TextStyle(color: NeslaColors.cyan)),
        ],
        const SizedBox(height: 16),
        Wrap(
          spacing: 16,
          runSpacing: 16,
          children: [
            SizedBox(
              width: 560,
              child: _panel(
                'OpenRouter Settings',
                Column(
                  children: [
                    _field(openrouterApiKeyController, 'OPENROUTER_API_KEY'),
                    _field(openrouterBaseUrlController, 'OPENROUTER_BASE_URL'),
                    _field(openrouterModelIdsController, 'OPENROUTER_MODEL_IDS'),
                    _field(openrouterFallbackModelIdsController, 'OPENROUTER_FALLBACK_MODEL_IDS'),
                    _field(openrouterAppNameController, 'OPENROUTER_APP_NAME'),
                    _field(openrouterRefererController, 'OPENROUTER_REFERER'),
                    _field(openrouterTimeoutController, 'OPENROUTER_TIMEOUT_SECONDS', number: true),
                    const SizedBox(height: 12),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        onPressed: _saveEnv,
                        icon: const Icon(Icons.save),
                        label: const Text('Save to .env'),
                      ),
                    ),
                    const SizedBox(height: 8),
                    SizedBox(
                      width: double.infinity,
                      child: OutlinedButton.icon(
                        onPressed: _loadEnv,
                        icon: const Icon(Icons.refresh),
                        label: const Text('Reload from .env'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(
              width: 560,
              child: _panel(
                'Model Examples',
                const Text(
                  'Suggested OpenRouter list:\n'
                  'openai/gpt-4o-mini\n'
                  'anthropic/claude-3.5-sonnet\n'
                  'meta-llama/llama-3.1-70b-instruct\n'
                  'mistralai/mistral-large',
                  style: TextStyle(color: NeslaColors.darkGray),
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildMobileDrawer(BuildContext context) {
    return Drawer(
      backgroundColor: NeslaColors.darkBlue,
      child: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(12),
          children: [
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 12),
              child: Text(
                'NESLA OS',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: NeslaColors.white),
              ),
            ),
            const Divider(color: NeslaColors.mediumBlue),
            ...sidebarItems.map(
              (item) => ListTile(
                leading: Icon(item.icon, color: item.isActive ? NeslaColors.cyan : NeslaColors.darkGray),
                title: Text(item.label, style: TextStyle(color: item.isActive ? NeslaColors.cyan : NeslaColors.mediumGray)),
                selected: item.isActive,
                onTap: () {
                  setState(() {
                    selectedRoute = item.route;
                    for (final sidebarItem in sidebarItems) {
                      sidebarItem.isActive = sidebarItem.route == item.route;
                    }
                  });
                  Navigator.pop(context);
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showBrowserAccess() {
    showDialog<void>(
      context: context,
      builder: (context) => Dialog(
        backgroundColor: NeslaColors.darkBlue,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        child: const Padding(
          padding: EdgeInsets.all(20),
          child: BrowserAccessPanel(),
        ),
      ),
    );
  }

  Widget _buildGeminiStyleHero() {
    final isMobile = ResponsiveService.isMobile(context);
    return Container(
      width: double.infinity,
      padding: EdgeInsets.all(isMobile ? 18 : 24),
      decoration: BoxDecoration(
        color: NeslaColors.darkBlue.withAlpha(190),
        border: Border.all(color: NeslaColors.cyan.withAlpha(45)),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          ShaderMask(
            shaderCallback: (bounds) => NeslaColors.cyanGradient.createShader(bounds),
            child: const Text(
              'Hello, Admin',
              style: TextStyle(fontSize: 34, fontWeight: FontWeight.w800, color: Colors.white),
            ),
          ),
          const SizedBox(height: 8),
          const Text(
            'Ask NESLA to inspect servers, open approved consoles, or prepare a deployment path.',
            style: TextStyle(color: NeslaColors.darkGray, fontSize: 15),
          ),
          const SizedBox(height: 18),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
            decoration: BoxDecoration(
              color: NeslaColors.deepBlue,
              border: Border.all(color: NeslaColors.cyan.withAlpha(35)),
              borderRadius: BorderRadius.circular(28),
            ),
            child: Row(
              children: [
                const Icon(Icons.auto_awesome, color: NeslaColors.cyan),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    isMobile ? 'Tap a module or ask NESLA...' : 'Tell NESLA what to do next...',
                    style: const TextStyle(color: NeslaColors.mediumGray),
                  ),
                ),
                const Icon(Icons.mic_none, color: NeslaColors.darkGray),
              ],
            ),
          ),
        ],
      ),
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

  Widget _glassBadge(String title, String subtitle, String footer) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.black.withAlpha(70),
        border: Border.all(color: NeslaColors.cyan.withAlpha((0.22 * 255).toInt())),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(color: NeslaColors.white, fontWeight: FontWeight.w700, fontSize: 12)),
          Text(subtitle, style: const TextStyle(color: NeslaColors.darkGray, fontSize: 11)),
          Text(footer, style: const TextStyle(color: NeslaColors.mediumGray, fontSize: 10)),
        ],
      ),
    );
  }

  Widget _moduleTile(_ModuleTileSpec spec) {
    return Container(
      height: 150,
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.black.withAlpha(90),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: const Color(0xFF1F4B8A), width: 1.6),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withAlpha(70),
            blurRadius: 18,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: Stack(
        children: [
          Align(
            alignment: Alignment.centerRight,
            child: Opacity(
              opacity: 0.16,
              child: Icon(spec.icon, size: 110, color: spec.accent),
            ),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Row(
                children: [
                  Icon(spec.icon, color: spec.accent, size: 30),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      spec.title,
                      style: const TextStyle(
                        color: NeslaColors.white,
                        fontSize: 20,
                        fontWeight: FontWeight.w800,
                        letterSpacing: 0.8,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(spec.line1, style: const TextStyle(color: NeslaColors.mediumGray, fontSize: 12)),
              const SizedBox(height: 3),
              Text(spec.line2, style: const TextStyle(color: NeslaColors.mediumGray, fontSize: 12)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _statCard(String title, String subtitle, String footnote, IconData icon, Color accent) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: NeslaColors.darkBlue.withAlpha(190),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: accent.withAlpha((0.22 * 255).toInt())),
      ),
      child: Row(
        children: [
          Icon(icon, color: accent, size: 26),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(color: NeslaColors.white, fontWeight: FontWeight.w700)),
                Text(subtitle, style: const TextStyle(color: NeslaColors.darkGray, fontSize: 11)),
                Text(footnote, style: TextStyle(color: accent, fontSize: 11, fontWeight: FontWeight.w700)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _keyChip(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.black.withAlpha(80),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.white.withAlpha(90), width: 1.2),
      ),
      child: Text(
        text,
        style: const TextStyle(
          color: NeslaColors.white,
          fontWeight: FontWeight.w800,
          fontSize: 16,
          letterSpacing: 2,
        ),
      ),
    );
  }

  Widget _centerFlowTag(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.black.withAlpha(100),
        border: Border.all(color: NeslaColors.cyan.withAlpha(120)),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Text(
        text,
        style: const TextStyle(color: NeslaColors.cyan, fontSize: 26, fontWeight: FontWeight.w700),
      ),
    );
  }

  Widget _verticalLaneLabel(String label) {
    return RotatedBox(
      quarterTurns: 1,
      child: Text(
        label,
        style: const TextStyle(color: NeslaColors.mediumGray, letterSpacing: 2, fontWeight: FontWeight.w700),
      ),
    );
  }

  Widget _panel(String title, Widget child) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: NeslaColors.darkBlue.withAlpha((0.72 * 255).toInt()),
        border: Border.all(color: NeslaColors.cyan.withAlpha((0.18 * 255).toInt())),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(color: NeslaColors.white, fontWeight: FontWeight.w700)),
          const SizedBox(height: 12),
          child,
        ],
      ),
    );
  }

  Widget _field(TextEditingController controller, String label, {bool number = false}) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: TextField(
        controller: controller,
        keyboardType: number ? TextInputType.number : TextInputType.text,
        decoration: InputDecoration(
          labelText: label,
          labelStyle: const TextStyle(color: NeslaColors.darkGray),
          enabledBorder: OutlineInputBorder(
            borderSide: BorderSide(color: NeslaColors.cyan.withAlpha((0.18 * 255).toInt())),
          ),
          focusedBorder: const OutlineInputBorder(borderSide: BorderSide(color: NeslaColors.cyan)),
        ),
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

class _ModuleTileSpec {
  final String title;
  final String line1;
  final String line2;
  final IconData icon;
  final Color accent;
  final String route;

  const _ModuleTileSpec(
    this.title,
    this.line1,
    this.line2,
    this.icon,
    this.accent,
    this.route,
  );
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
