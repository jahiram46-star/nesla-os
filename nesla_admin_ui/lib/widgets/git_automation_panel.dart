import 'package:flutter/material.dart';

import '../services/load_balancer_api.dart';
import '../theme/colors.dart';

class GitAutomationPanel extends StatefulWidget {
  const GitAutomationPanel({super.key, required this.api});

  final LoadBalancerApi api;

  @override
  State<GitAutomationPanel> createState() => _GitAutomationPanelState();
}

class _GitAutomationPanelState extends State<GitAutomationPanel> {
  final messageController = TextEditingController(text: 'auto: nesla os update');
  GitStatus? status;
  String? output;
  bool busy = false;
  bool pushToRemote = false;

  @override
  void initState() {
    super.initState();
    refresh();
  }

  @override
  void dispose() {
    messageController.dispose();
    super.dispose();
  }

  Future<void> refresh() async {
    setState(() => busy = true);
    try {
      status = await widget.api.fetchGitStatus();
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  Future<void> commit() async {
    setState(() {
      busy = true;
      output = 'Committing local changes...';
    });
    try {
      output = await widget.api.autoCommit(message: messageController.text.trim(), push: pushToRemote);
      status = await widget.api.fetchGitStatus();
    } catch (err) {
      output = err.toString();
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(Icons.commit_outlined, color: NeslaColors.cyan, size: 18),
            const SizedBox(width: 8),
            Text(
              status == null ? 'Git status loading...' : 'Branch: ${status!.branch}',
              style: const TextStyle(fontWeight: FontWeight.w700),
            ),
            const Spacer(),
            if (busy)
              const SizedBox(
                width: 14,
                height: 14,
                child: CircularProgressIndicator(strokeWidth: 2, color: NeslaColors.cyan),
              ),
          ],
        ),
        const SizedBox(height: 8),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: NeslaColors.deepBlue,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: NeslaColors.cyan.withAlpha(28)),
          ),
          child: Text(
            status == null
                ? 'Checking working tree...'
                : status!.clean
                    ? 'Working tree clean'
                    : '${status!.changes.length} changed files ready for auto commit',
            style: TextStyle(color: status?.clean == true ? NeslaColors.onlineGreen : NeslaColors.warningOrange),
          ),
        ),
        const SizedBox(height: 12),
        TextField(
          controller: messageController,
          decoration: const InputDecoration(labelText: 'Commit message'),
        ),
        CheckboxListTile(
          contentPadding: EdgeInsets.zero,
          value: pushToRemote,
          onChanged: busy ? null : (value) => setState(() => pushToRemote = value ?? false),
          title: const Text('Push to GitHub remote after commit'),
          subtitle: const Text('Requires your local git remote/auth to already be configured.'),
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: FilledButton.icon(
                onPressed: busy ? null : commit,
                icon: const Icon(Icons.commit),
                label: const Text('Auto Commit Local Repo'),
              ),
            ),
            const SizedBox(width: 8),
            IconButton.filledTonal(
              onPressed: busy ? null : refresh,
              icon: const Icon(Icons.refresh),
            ),
          ],
        ),
        if (output != null) ...[
          const SizedBox(height: 10),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: NeslaColors.mediumBlue.withAlpha(70),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: NeslaColors.mediumBlue.withAlpha(120)),
            ),
            child: Text(output!, style: const TextStyle(color: NeslaColors.mediumGray, fontSize: 12, height: 1.35)),
          ),
        ],
      ],
    );
  }
}
