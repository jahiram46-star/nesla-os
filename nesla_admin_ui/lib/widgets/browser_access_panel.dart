import 'package:flutter/material.dart';

import '../services/browser_access_api.dart';
import '../theme/colors.dart';

class BrowserAccessPanel extends StatefulWidget {
  const BrowserAccessPanel({super.key});

  @override
  State<BrowserAccessPanel> createState() => _BrowserAccessPanelState();
}

class _BrowserAccessPanelState extends State<BrowserAccessPanel> {
  final api = BrowserAccessApi();
  BrowserAccessManifest? manifest;
  String? output;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    try {
      manifest = await api.fetchManifest();
    } catch (err) {
      output = err.toString();
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> openTarget(BrowserConsoleTarget target) async {
    final result = await api.requestOpen(target.key);
    setState(() {
      output = result['allowed'] == true
          ? 'Ready for Chrome API bridge: ${target.url}'
          : 'Blocked: ${result['reason']}';
    });
  }

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return const SizedBox(height: 180, child: Center(child: CircularProgressIndicator()));
    }
    final data = manifest;
    if (data == null) {
      return Text(output ?? 'Browser capability unavailable');
    }
    return SizedBox(
      width: 620,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('NESLA Browser Access', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w700)),
          const SizedBox(height: 6),
          const Text(
            'Chrome-style console access for the LLM. Real Chrome API bridge will be added at the backend hook.',
            style: TextStyle(color: NeslaColors.darkGray),
          ),
          const SizedBox(height: 16),
          ...data.targets.map(
            (target) => ListTile(
              contentPadding: EdgeInsets.zero,
              leading: const Icon(Icons.public, color: NeslaColors.cyan),
              title: Text(target.label),
              subtitle: Text(target.url),
              trailing: IconButton(
                icon: const Icon(Icons.open_in_browser),
                onPressed: () => openTarget(target),
              ),
            ),
          ),
          const Divider(),
          Text('Rules: ${data.rules.length} | Tools: ${data.toolCapabilities.join(', ')}'),
          if (output != null) ...[
            const SizedBox(height: 12),
            Text(output!, style: const TextStyle(color: NeslaColors.warningOrange)),
          ],
        ],
      ),
    );
  }
}
