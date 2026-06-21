import 'package:flutter/material.dart';

import '../services/firebase_server_catalog.dart';
import '../services/load_balancer_api.dart';
import '../theme/colors.dart';
import '../widgets/browser_automation_panel.dart';
import '../widgets/git_automation_panel.dart';
import '../widgets/llm_pipeline_chat.dart';

class LoadBalancerScreen extends StatefulWidget {
  const LoadBalancerScreen({super.key});

  @override
  State<LoadBalancerScreen> createState() => _LoadBalancerScreenState();
}

class _LoadBalancerScreenState extends State<LoadBalancerScreen> {
  final api = LoadBalancerApi();
  final nameController = TextEditingController(text: 'server-1');
  final hostController = TextEditingController(text: '127.0.0.1');
  final portController = TextEditingController(text: '8001');
  final weightController = TextEditingController(text: '1');
  final maxModulesController = TextEditingController(text: '8');
  final capabilitiesController = TextEditingController(text: 'brain,memory,sss');
  final moduleController = TextEditingController(text: 'brain');
  final routeController = TextEditingController(text: '/brain');
  final priorityController = TextEditingController(text: '1');
  final firebaseProjectController = TextEditingController(text: 'your-project-id');
  final huggingFaceSpaceController = TextEditingController(text: 'your-username/your-space');
  final routingModuleController = TextEditingController(text: 'brain');
  RoutingPlan? routingPlan;
  final firebaseBridge = FirebaseSdkBridge();

  List<LoadBalancerServer> servers = [];
  List<ModulePlacement> placements = [];
  List<ModuleServerPolicy> policies = [];
  List<CodeLocationPolicy> codeLocations = [];
  int? selectedServerId;
  bool loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    refresh();
  }

  @override
  void dispose() {
    nameController.dispose();
    hostController.dispose();
    portController.dispose();
    weightController.dispose();
    maxModulesController.dispose();
    capabilitiesController.dispose();
    moduleController.dispose();
    routeController.dispose();
    priorityController.dispose();
    firebaseProjectController.dispose();
    huggingFaceSpaceController.dispose();
    routingModuleController.dispose();
    super.dispose();
  }

  Future<void> refresh() async {
    setState(() {
      loading = true;
      error = null;
    });
    try {
      final nextServers = await api.fetchServers();
      final nextPlacements = await api.fetchPlacements();
      final nextPolicies = await api.fetchModulePolicies();
      final nextCodeLocations = await api.fetchCodeLocationPolicies();
      final nextRoutingPlan = await api.fetchRoutingPlan(routingModuleController.text.trim());
      setState(() {
        servers = nextServers;
        placements = nextPlacements;
        policies = nextPolicies;
        codeLocations = nextCodeLocations;
        routingPlan = nextRoutingPlan;
        selectedServerId = selectedServerId ?? (nextServers.isEmpty ? null : nextServers.first.id);
      });
    } catch (err) {
      setState(() => error = 'Backend connect korte parchi na. FastAPI server chalu ache kina check koro.');
    } finally {
      setState(() => loading = false);
    }
  }

  Future<void> addServer() async {
    await api.createServer(
      name: nameController.text.trim(),
      host: hostController.text.trim(),
      port: int.tryParse(portController.text) ?? 8000,
      protocol: 'http',
      weight: int.tryParse(weightController.text) ?? 1,
      maxModules: int.tryParse(maxModulesController.text) ?? 8,
      capabilities: capabilitiesController.text
          .split(',')
          .map((item) => item.trim())
          .where((item) => item.isNotEmpty)
          .toList(),
    );
    await refresh();
  }

  Future<void> addPlacement() async {
    final serverId = selectedServerId;
    if (serverId == null) return;
    await api.createPlacement(
      moduleName: moduleController.text.trim(),
      serverId: serverId,
      routePrefix: routeController.text.trim(),
      priority: int.tryParse(priorityController.text) ?? 1,
    );
    await refresh();
  }

  Future<void> addFirebasePresets() async {
    final presets = await api.fetchFirebasePresets(projectId: firebaseProjectController.text.trim());
    await api.createServersFromPresets(presets);
    await refresh();
  }

  Future<void> addHuggingFacePresets() async {
    final presets = await api.fetchHuggingFacePresets(spaceId: huggingFaceSpaceController.text.trim());
    await api.createServersFromPresets(presets);
    await refresh();
  }

  Future<void> previewRouting() async {
    final plan = await api.fetchRoutingPlan(routingModuleController.text.trim());
    setState(() => routingPlan = plan);
  }

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return const Center(child: CircularProgressIndicator(color: NeslaColors.cyan));
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Text('Load Balancer', style: Theme.of(context).textTheme.titleLarge),
            const Spacer(),
            IconButton(
              onPressed: refresh,
              icon: const Icon(Icons.refresh, color: NeslaColors.cyan),
            ),
          ],
        ),
        const SizedBox(height: 8),
        const Text(
          'Server add koro, tarpor kon NESLA module kon server e run korbe set koro.',
          style: TextStyle(color: NeslaColors.darkGray),
        ),
        if (error != null) ...[
          const SizedBox(height: 12),
          Text(error!, style: const TextStyle(color: NeslaColors.warningOrange)),
        ],
        const SizedBox(height: 20),
        LayoutBuilder(
          builder: (context, constraints) {
            final twoColumns = constraints.maxWidth > 900;
            return Wrap(
              spacing: 16,
              runSpacing: 16,
              children: [
                SizedBox(
                  width: twoColumns ? (constraints.maxWidth - 16) / 2 : constraints.maxWidth,
                  child: _panel('Add Server', _serverForm()),
                ),
                SizedBox(
                  width: twoColumns ? (constraints.maxWidth - 16) / 2 : constraints.maxWidth,
                  child: _panel('Assign Module', _placementForm()),
                ),
              ],
            );
          },
        ),
        const SizedBox(height: 20),
        _panel('Servers', _serverList()),
        const SizedBox(height: 16),
        _panel('Module Placements', _placementList()),
        const SizedBox(height: 16),
        _panel('Recommended Server Policies', _policyList()),
        const SizedBox(height: 16),
        _panel('GitHub Code Location Policy', _codeLocationList()),
        const SizedBox(height: 16),
        LayoutBuilder(
          builder: (context, constraints) {
            final twoColumns = constraints.maxWidth > 900;
            return Wrap(
              spacing: 16,
              runSpacing: 16,
              children: [
                SizedBox(
                  width: twoColumns ? (constraints.maxWidth - 16) / 2 : constraints.maxWidth,
                  child: _panel('Firebase / Hugging Face Presets', _firebasePresetPanel()),
                ),
                SizedBox(
                  width: twoColumns ? (constraints.maxWidth - 16) / 2 : constraints.maxWidth,
                  child: _panel('GitHub Auto Commit', GitAutomationPanel(api: api)),
                ),
                SizedBox(
                  width: twoColumns ? (constraints.maxWidth - 16) / 2 : constraints.maxWidth,
                  child: _panel('Browser Automation', BrowserAutomationPanel(api: api)),
                ),
              ],
            );
          },
        ),
        const SizedBox(height: 20),
        _panel(
          'Route Preview',
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _field(routingModuleController, 'Module to route'),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () => previewRouting().catchError((_) => refresh()),
                  icon: const Icon(Icons.alt_route),
                  label: const Text('Preview Route'),
                ),
              ),
              const SizedBox(height: 12),
              if (routingPlan == null)
                const Text('Routing plan ekhono load hoyনি.', style: TextStyle(color: NeslaColors.darkGray))
              else
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Module: ${routingPlan!.moduleName}',
                      style: const TextStyle(color: NeslaColors.white, fontWeight: FontWeight.w700),
                    ),
                    const SizedBox(height: 8),
                    ...routingPlan!.targets.map(
                      (target) => ListTile(
                        contentPadding: EdgeInsets.zero,
                        leading: const Icon(Icons.router, color: NeslaColors.cyan),
                        title: Text(target.serverName, style: const TextStyle(color: NeslaColors.white)),
                        subtitle: Text('${target.baseUrl}\n${target.routePrefix}'),
                        trailing: Text(
                          'P${target.priority}  L${target.loadScore.toStringAsFixed(1)}',
                          style: const TextStyle(color: NeslaColors.mediumGray),
                        ),
                      ),
                    ),
                  ],
                ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _panel(
          'LLM Task Chat - Browser IndexedDB Pipeline',
          LlmPipelineChat(api: api, servers: servers, placements: placements),
        ),
      ],
    );
  }

  Widget _serverForm() {
    return Column(
      children: [
        _field(nameController, 'Server name'),
        _field(hostController, 'Host/IP'),
        Row(
          children: [
            Expanded(child: _field(portController, 'Port', number: true)),
            const SizedBox(width: 12),
            Expanded(child: _field(weightController, 'Weight', number: true)),
          ],
        ),
        _field(maxModulesController, 'Max modules', number: true),
        _field(capabilitiesController, 'Capabilities comma separated'),
        const SizedBox(height: 12),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            onPressed: () => addServer().catchError((_) => refresh()),
            icon: const Icon(Icons.add),
            label: const Text('Add Server'),
          ),
        ),
      ],
    );
  }

  Widget _placementForm() {
    return Column(
      children: [
        DropdownButtonFormField<int>(
          initialValue: selectedServerId,
          decoration: _inputDecoration('Target server'),
          dropdownColor: NeslaColors.darkBlue,
          items: servers
              .map((server) => DropdownMenuItem(value: server.id, child: Text(server.name)))
              .toList(),
          onChanged: (value) => setState(() => selectedServerId = value),
        ),
        _field(moduleController, 'Module name'),
        _field(routeController, 'Route prefix'),
        _field(priorityController, 'Priority', number: true),
        const SizedBox(height: 12),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            onPressed: servers.isEmpty ? null : () => addPlacement().catchError((_) => refresh()),
            icon: const Icon(Icons.hub),
            label: const Text('Assign Module'),
          ),
        ),
      ],
    );
  }

  Widget _serverList() {
    if (servers.isEmpty) {
      return const Text('No server added yet.', style: TextStyle(color: NeslaColors.darkGray));
    }
    return Column(
      children: servers
          .map(
            (server) => ListTile(
              leading: const Icon(Icons.dns, color: NeslaColors.cyan),
              title: Text(server.name, style: const TextStyle(color: NeslaColors.white)),
              subtitle: Text('${server.baseUrl} | ${server.capabilities.join(', ')}'),
              trailing: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(server.status, style: const TextStyle(color: NeslaColors.onlineGreen)),
                  Text(
                    server.name.contains('firebase')
                        ? 'Firebase'
                        : server.name.contains('huggingface')
                            ? 'Hugging Face'
                            : 'Custom',
                    style: const TextStyle(color: NeslaColors.mediumGray, fontSize: 11),
                  ),
                ],
              ),
            ),
          )
          .toList(),
    );
  }

  Widget _placementList() {
    if (placements.isEmpty) {
      return const Text('No module placement yet.', style: TextStyle(color: NeslaColors.darkGray));
    }
    return Column(
      children: placements
          .map(
            (placement) => ListTile(
              leading: const Icon(Icons.account_tree, color: NeslaColors.cyan),
              title: Text(placement.moduleName, style: const TextStyle(color: NeslaColors.white)),
              subtitle: Text('${placement.routePrefix} -> ${placement.server?.name ?? 'unknown server'}'),
              trailing: Text('P${placement.priority}', style: const TextStyle(color: NeslaColors.mediumGray)),
            ),
          )
          .toList(),
    );
  }

  Widget _policyList() {
    if (policies.isEmpty) {
      return const Text('No server policy loaded.', style: TextStyle(color: NeslaColors.darkGray));
    }
    return Column(
      children: policies
          .map(
            (policy) => ListTile(
              leading: const Icon(Icons.policy, color: NeslaColors.cyan),
              title: Text(policy.moduleGroup, style: const TextStyle(color: NeslaColors.white)),
              subtitle: Text('${policy.preferredServers.join(' + ')}\n${policy.notes}'),
              isThreeLine: true,
              trailing: Text(
                policy.capabilities.join(', '),
                style: const TextStyle(color: NeslaColors.mediumGray, fontSize: 11),
              ),
            ),
          )
          .toList(),
    );
  }

  Widget _codeLocationList() {
    if (codeLocations.isEmpty) {
      return const Text('No GitHub code-location policy loaded.', style: TextStyle(color: NeslaColors.darkGray));
    }
    return Column(
      children: codeLocations
          .map(
            (policy) => ListTile(
              leading: const Icon(Icons.source, color: NeslaColors.cyan),
              title: Text(policy.codeGroup, style: const TextStyle(color: NeslaColors.white)),
              subtitle: Text('${policy.githubScope}\n${policy.pathHint}\n${policy.notes}'),
              isThreeLine: true,
              trailing: Text(
                policy.owns.join(' • '),
                style: const TextStyle(color: NeslaColors.mediumGray, fontSize: 11),
              ),
            ),
          )
          .toList(),
    );
  }

  Widget _firebasePresetPanel() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          firebaseBridge.isConfigured
              ? 'Firebase SDK configured'
              : 'Firebase SDK added. Add Firebase.initializeApp options later.',
          style: const TextStyle(color: NeslaColors.darkGray),
        ),
        const SizedBox(height: 8),
        _field(firebaseProjectController, 'Firebase project id'),
        const SizedBox(height: 4),
        Text(
          'Firebase regions: ${FirebaseServerCatalog.regions.length}',
          style: const TextStyle(color: NeslaColors.darkGray),
        ),
        const SizedBox(height: 12),
        _field(huggingFaceSpaceController, 'Hugging Face space id'),
        const SizedBox(height: 4),
        const Text(
          'Hugging Face presets are ready for a Space or inference endpoint.',
          style: TextStyle(color: NeslaColors.darkGray),
        ),
        const SizedBox(height: 12),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            onPressed: () => addFirebasePresets().catchError((_) => refresh()),
            icon: const Icon(Icons.cloud),
            label: const Text('Add 10 Firebase Server Presets'),
          ),
        ),
        const SizedBox(height: 10),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            onPressed: () => addHuggingFacePresets().catchError((_) => refresh()),
            icon: const Icon(Icons.psychology),
            label: const Text('Add Hugging Face Presets'),
          ),
        ),
      ],
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
        decoration: _inputDecoration(label),
      ),
    );
  }

  InputDecoration _inputDecoration(String label) {
    return InputDecoration(
      labelText: label,
      labelStyle: const TextStyle(color: NeslaColors.darkGray),
      enabledBorder: OutlineInputBorder(
        borderSide: BorderSide(color: NeslaColors.cyan.withAlpha((0.18 * 255).toInt())),
      ),
      focusedBorder: const OutlineInputBorder(borderSide: BorderSide(color: NeslaColors.cyan)),
    );
  }
}
