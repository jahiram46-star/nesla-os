import 'package:flutter/material.dart';

import '../services/load_balancer_api.dart';
import '../theme/colors.dart';

class BrowserAutomationPanel extends StatefulWidget {
  const BrowserAutomationPanel({super.key, required this.api});

  final LoadBalancerApi api;

  @override
  State<BrowserAutomationPanel> createState() => _BrowserAutomationPanelState();
}

class _BrowserAutomationPanelState extends State<BrowserAutomationPanel> {
  BrowserAccessManifest? manifest;
  final urlController = TextEditingController(text: 'https://example.com');
  final selectorController = TextEditingController(text: 'body');
  final textController = TextEditingController(text: 'Hello');
  String? output;
  bool busy = false;

  @override
  void initState() {
    super.initState();
    refresh();
  }

  Future<void> refresh() async {
    setState(() => busy = true);
    try {
      manifest = await widget.api.fetchBrowserManifest();
    } catch (err) {
      output = err.toString();
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  @override
  void dispose() {
    urlController.dispose();
    selectorController.dispose();
    textController.dispose();
    super.dispose();
  }

  Future<void> openTarget(String key) async {
    setState(() {
      busy = true;
      output = 'Opening browser target...';
    });
    try {
      final result = await widget.api.openBrowserTarget(key);
      output = result['status']?.toString() ?? result.toString();
    } catch (err) {
      output = err.toString();
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  Future<void> navigate() async {
    setState(() {
      busy = true;
      output = 'Navigating...';
    });
    try {
      final result = await widget.api.browserNavigate(urlController.text.trim());
      output = '${result.status} ${result.url ?? ''}'.trim();
    } catch (err) {
      output = err.toString();
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  Future<void> click() async {
    setState(() {
      busy = true;
      output = 'Clicking selector...';
    });
    try {
      final result = await widget.api.browserClick(
        url: urlController.text.trim(),
        selector: selectorController.text.trim(),
      );
      output = '${result.status} ${result.selector ?? ''}'.trim();
    } catch (err) {
      output = err.toString();
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  Future<void> typeText() async {
    setState(() {
      busy = true;
      output = 'Typing text...';
    });
    try {
      final result = await widget.api.browserType(
        url: urlController.text.trim(),
        selector: selectorController.text.trim(),
        text: textController.text,
      );
      output = '${result.status} ${result.selector ?? ''}'.trim();
    } catch (err) {
      output = err.toString();
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final targets = manifest?.targets ?? const <BrowserConsoleTarget>[];
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(Icons.travel_explore, color: NeslaColors.cyan),
            const SizedBox(width: 8),
            const Text('Browser Automation', style: TextStyle(fontWeight: FontWeight.w700)),
            const Spacer(),
            if (busy)
              const SizedBox(
                width: 14,
                height: 14,
                child: CircularProgressIndicator(strokeWidth: 2, color: NeslaColors.cyan),
              ),
          ],
        ),
        const SizedBox(height: 10),
        Text(
          manifest == null
              ? 'Loading approved browser targets...'
              : 'Approved targets: ${targets.length}',
          style: const TextStyle(color: NeslaColors.darkGray),
        ),
        const SizedBox(height: 12),
        TextField(
          controller: urlController,
          decoration: const InputDecoration(labelText: 'URL to automate'),
        ),
        const SizedBox(height: 8),
        TextField(
          controller: selectorController,
          decoration: const InputDecoration(labelText: 'CSS selector'),
        ),
        const SizedBox(height: 8),
        TextField(
          controller: textController,
          decoration: const InputDecoration(labelText: 'Text to type'),
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: FilledButton(
                onPressed: busy ? null : navigate,
                child: const Text('Navigate'),
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: OutlinedButton(
                onPressed: busy ? null : click,
                child: const Text('Click'),
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: OutlinedButton(
                onPressed: busy ? null : typeText,
                child: const Text('Type'),
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: targets
              .map(
                (target) => OutlinedButton(
                  onPressed: busy ? null : () => openTarget(target.key),
                  child: Text(target.label),
                ),
              )
              .toList(),
        ),
        const SizedBox(height: 12),
        if (output != null)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: NeslaColors.mediumBlue.withAlpha(70),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: NeslaColors.mediumBlue.withAlpha(120)),
            ),
            child: Text(output!, style: const TextStyle(color: NeslaColors.mediumGray, fontSize: 12)),
          ),
      ],
    );
  }
}
