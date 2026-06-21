import 'package:flutter/material.dart';

import '../services/load_balancer_api.dart';
import '../services/pipeline_indexed_db.dart';
import '../theme/colors.dart';

class LlmPipelineChat extends StatefulWidget {
  const LlmPipelineChat({
    super.key,
    required this.api,
    required this.servers,
    required this.placements,
  });

  final LoadBalancerApi api;
  final List<LoadBalancerServer> servers;
  final List<ModulePlacement> placements;

  @override
  State<LlmPipelineChat> createState() => _LlmPipelineChatState();
}

class _LlmPipelineChatState extends State<LlmPipelineChat> {
  final db = PipelineIndexedDb();
  final promptController = TextEditingController();
  final scrollController = ScrollController();
  List<PipelineMessage> messages = [];
  bool working = false;
  String typingText = '';
  String? pendingConfirmationToken;
  List<AdminAgentAction> pendingActions = [];

  @override
  void initState() {
    super.initState();
    loadMessages();
  }

  @override
  void dispose() {
    promptController.dispose();
    scrollController.dispose();
    super.dispose();
  }

  Future<void> loadMessages() async {
    messages = await db.readMessages();
    if (mounted) setState(() {});
    await _scrollToBottom();
  }

  Future<void> sendTask() async {
    final prompt = promptController.text.trim();
    if (prompt.isEmpty || working) return;

    final now = DateTime.now();
    final userMessage = PipelineMessage(
      id: 'user-${now.microsecondsSinceEpoch}',
      role: 'user',
      text: prompt,
      createdAt: now,
    );
    await db.writeContextValue('servers', widget.servers.map((server) => {
          'id': server.id,
          'name': server.name,
          'baseUrl': server.baseUrl,
          'capabilities': server.capabilities,
        }).toList());
    await db.writeContextValue('placements', widget.placements.map((placement) => {
          'id': placement.id,
          'moduleName': placement.moduleName,
          'routePrefix': placement.routePrefix,
          'serverName': placement.server?.name,
        }).toList());
    await db.addMessage(userMessage);

    setState(() {
      working = true;
      typingText = '';
      promptController.clear();
    });
    await loadMessages();
    await _typeStatus('I am working...');

    final context = await db.readLocalContext();
    final result = await widget.api.runAdminAgentTask(
      taskId: 'task-${DateTime.now().millisecondsSinceEpoch}',
      prompt: prompt,
      localContext: context,
    );
    final actionSummary = result.actions.isEmpty
        ? ''
        : '\n\nActions:\n${result.actions.map((action) => '- ${action.title} (${action.risk})').join('\n')}';
    final assistantMessage = PipelineMessage(
      id: 'assistant-${DateTime.now().microsecondsSinceEpoch}',
      role: 'assistant',
      text: '${result.assistantMessage}$actionSummary',
      createdAt: DateTime.now(),
    );
    await db.addMessage(assistantMessage);
    await db.writeContextValue('lastResult', assistantMessage.text);
    setState(() {
      working = false;
      typingText = '';
      pendingConfirmationToken = result.confirmationToken;
      pendingActions = result.actions.where((action) => action.risk == 'confirmation_required').toList();
    });
    await loadMessages();
  }

  Future<void> confirmActions(bool approved) async {
    final token = pendingConfirmationToken;
    if (token == null || working) return;
    setState(() {
      working = true;
      typingText = approved ? 'Confirming actions...' : 'Cancelling actions...';
    });
    final result = await widget.api.confirmAdminAgentActions(
      confirmationToken: token,
      approved: approved,
    );
    await db.addMessage(PipelineMessage(
      id: 'assistant-confirm-${DateTime.now().microsecondsSinceEpoch}',
      role: 'assistant',
      text: result.assistantMessage,
      createdAt: DateTime.now(),
    ));
    setState(() {
      working = false;
      typingText = '';
      pendingConfirmationToken = null;
      pendingActions = [];
    });
    await loadMessages();
  }

  Future<void> _scrollToBottom() async {
    await Future<void>.delayed(const Duration(milliseconds: 16));
    if (!mounted || !scrollController.hasClients) return;
    scrollController.animateTo(
      scrollController.position.maxScrollExtent,
      duration: const Duration(milliseconds: 220),
      curve: Curves.easeOutCubic,
    );
  }

  Future<void> _typeStatus(String text) async {
    for (var i = 0; i < text.length; i++) {
      if (!mounted) return;
      setState(() => typingText = text.substring(0, i + 1));
      await Future<void>.delayed(const Duration(milliseconds: 45));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: NeslaColors.deepBlue.withAlpha(160),
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: NeslaColors.cyan.withAlpha(34)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Icon(Icons.smart_toy_outlined, color: NeslaColors.cyan, size: 18),
                  const SizedBox(width: 8),
                  const Text(
                    'Browser IndexedDB Pipeline',
                    style: TextStyle(fontWeight: FontWeight.w700),
                  ),
                  const Spacer(),
                  Text(
                    messages.isEmpty ? 'Empty' : '${messages.length} messages',
                    style: const TextStyle(color: NeslaColors.darkGray, fontSize: 12),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              SizedBox(
                height: 320,
                child: messages.isEmpty && !working
                    ? Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: const [
                            Icon(Icons.chat_bubble_outline, color: NeslaColors.darkGray),
                            SizedBox(height: 8),
                            Text(
                              'No local IndexedDB messages yet.',
                              style: TextStyle(color: NeslaColors.darkGray),
                            ),
                          ],
                        ),
                      )
                    : ListView(
                        controller: scrollController,
                        children: [
                          ...messages.map(_messageBubble),
                          if (working)
                            _messageBubble(PipelineMessage(
                              id: 'typing',
                              role: 'assistant',
                              text: typingText,
                              createdAt: DateTime.now(),
                            )),
                        ],
                      ),
                ),
              ),
            ],
          ),
        ),
        if (pendingConfirmationToken != null) ...[
          const SizedBox(height: 10),
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: NeslaColors.warningOrange.withAlpha(18),
              border: Border.all(color: NeslaColors.warningOrange.withAlpha(120)),
              borderRadius: BorderRadius.circular(14),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Row(
                  children: [
                    Icon(Icons.verified_user_outlined, color: NeslaColors.warningOrange, size: 18),
                    SizedBox(width: 8),
                    Text('Admin confirmation required'),
                  ],
                ),
                const SizedBox(height: 6),
                ...pendingActions.map(
                  (action) => Padding(
                    padding: const EdgeInsets.only(bottom: 4),
                    child: Text(
                      '- ${action.title}',
                      style: const TextStyle(fontSize: 12, color: NeslaColors.mediumGray),
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                Row(
                  children: [
                    FilledButton(
                      style: FilledButton.styleFrom(backgroundColor: NeslaColors.onlineGreen),
                      onPressed: working ? null : () => confirmActions(true),
                      child: const Text('Approve'),
                    ),
                    const SizedBox(width: 8),
                    OutlinedButton(
                      onPressed: working ? null : () => confirmActions(false),
                      child: const Text('Cancel'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: TextField(
                controller: promptController,
                minLines: 1,
                maxLines: 3,
                decoration: const InputDecoration(
                  labelText: 'Give NESLA a task',
                  hintText: 'Example: review placements and suggest the safest next step',
                ),
              ),
            ),
            const SizedBox(width: 8),
            FilledButton(
              onPressed: working ? null : sendTask,
              child: const Icon(Icons.send),
            ),
          ],
        ),
      ],
    );
  }

  Widget _messageBubble(PipelineMessage message) {
    final isUser = message.role == 'user';
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 8),
        padding: const EdgeInsets.all(12),
        constraints: const BoxConstraints(maxWidth: 620),
        decoration: BoxDecoration(
          color: isUser ? NeslaColors.cyan.withAlpha(34) : NeslaColors.mediumBlue.withAlpha(110),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: isUser ? NeslaColors.cyan.withAlpha(120) : NeslaColors.mediumBlue),
        ),
        child: Text(
          message.text,
          style: const TextStyle(color: NeslaColors.white, height: 1.35),
        ),
      ),
    );
  }
}
