import 'dart:convert';

import 'package:http/http.dart' as http;

import 'api_config.dart';

class LoadBalancerServer {
  final int id;
  final String name;
  final String host;
  final int port;
  final String protocol;
  final String status;
  final int weight;
  final int maxModules;
  final List<String> capabilities;

  const LoadBalancerServer({
    required this.id,
    required this.name,
    required this.host,
    required this.port,
    required this.protocol,
    required this.status,
    required this.weight,
    required this.maxModules,
    required this.capabilities,
  });

  factory LoadBalancerServer.fromJson(Map<String, dynamic> json) {
    return LoadBalancerServer(
      id: json['id'] as int,
      name: json['name'] as String,
      host: json['host'] as String,
      port: json['port'] as int,
      protocol: json['protocol'] as String,
      status: json['status'] as String,
      weight: json['weight'] as int,
      maxModules: json['max_modules'] as int,
      capabilities: List<String>.from(json['capabilities'] as List<dynamic>? ?? const []),
    );
  }

  String get baseUrl => '$protocol://$host:$port';
}

class ModulePlacement {
  final int id;
  final String moduleName;
  final String routePrefix;
  final int priority;
  final bool enabled;
  final LoadBalancerServer? server;

  const ModulePlacement({
    required this.id,
    required this.moduleName,
    required this.routePrefix,
    required this.priority,
    required this.enabled,
    this.server,
  });

  factory ModulePlacement.fromJson(Map<String, dynamic> json) {
    final serverJson = json['server'];
    return ModulePlacement(
      id: json['id'] as int,
      moduleName: json['module_name'] as String,
      routePrefix: json['route_prefix'] as String,
      priority: json['priority'] as int,
      enabled: json['enabled'] as bool,
      server: serverJson is Map<String, dynamic> ? LoadBalancerServer.fromJson(serverJson) : null,
    );
  }
}

class RoutingTarget {
  final String moduleName;
  final int serverId;
  final String serverName;
  final String baseUrl;
  final String routePrefix;
  final int priority;
  final double loadScore;

  const RoutingTarget({
    required this.moduleName,
    required this.serverId,
    required this.serverName,
    required this.baseUrl,
    required this.routePrefix,
    required this.priority,
    required this.loadScore,
  });

  factory RoutingTarget.fromJson(Map<String, dynamic> json) {
    return RoutingTarget(
      moduleName: json['module_name'] as String,
      serverId: json['server_id'] as int,
      serverName: json['server_name'] as String,
      baseUrl: json['base_url'] as String,
      routePrefix: json['route_prefix'] as String,
      priority: json['priority'] as int,
      loadScore: (json['load_score'] as num).toDouble(),
    );
  }
}

class RoutingPlan {
  final String moduleName;
  final List<RoutingTarget> targets;

  const RoutingPlan({
    required this.moduleName,
    required this.targets,
  });

  factory RoutingPlan.fromJson(Map<String, dynamic> json) {
    return RoutingPlan(
      moduleName: json['module_name'] as String,
      targets: (json['targets'] as List<dynamic>? ?? const [])
          .map((item) => RoutingTarget.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }
}

class BrowserConsoleTarget {
  final String key;
  final String label;
  final String url;
  final String purpose;

  const BrowserConsoleTarget({
    required this.key,
    required this.label,
    required this.url,
    required this.purpose,
  });

  factory BrowserConsoleTarget.fromJson(Map<String, dynamic> json) {
    return BrowserConsoleTarget(
      key: json['key'] as String,
      label: json['label'] as String,
      url: json['url'] as String,
      purpose: json['purpose'] as String,
    );
  }
}

class BrowserAccessManifest {
  final List<String> rules;
  final List<String> toolCapabilities;
  final List<BrowserConsoleTarget> targets;
  final String chromeApiHook;

  const BrowserAccessManifest({
    required this.rules,
    required this.toolCapabilities,
    required this.targets,
    required this.chromeApiHook,
  });

  factory BrowserAccessManifest.fromJson(Map<String, dynamic> json) {
    return BrowserAccessManifest(
      rules: List<String>.from(json['rules'] as List<dynamic>? ?? const []),
      toolCapabilities: List<String>.from(json['tool_capabilities'] as List<dynamic>? ?? const []),
      targets: (json['approved_console_targets'] as List<dynamic>? ?? const [])
          .map((item) => BrowserConsoleTarget.fromJson(item as Map<String, dynamic>))
          .toList(),
      chromeApiHook: json['chrome_api_hook'] as String? ?? '',
    );
  }
}

class BrowserActionResult {
  final String status;
  final String? url;
  final String? title;
  final String? selector;

  const BrowserActionResult({
    required this.status,
    this.url,
    this.title,
    this.selector,
  });

  factory BrowserActionResult.fromJson(Map<String, dynamic> json) {
    return BrowserActionResult(
      status: json['status'] as String? ?? 'unknown',
      url: json['url'] as String?,
      title: json['title'] as String?,
      selector: json['selector'] as String?,
    );
  }
}

class ModuleServerPolicy {
  final String moduleGroup;
  final List<String> preferredServers;
  final List<String> capabilities;
  final String notes;

  const ModuleServerPolicy({
    required this.moduleGroup,
    required this.preferredServers,
    required this.capabilities,
    required this.notes,
  });

  factory ModuleServerPolicy.fromJson(Map<String, dynamic> json) {
    return ModuleServerPolicy(
      moduleGroup: json['module_group'] as String,
      preferredServers: List<String>.from(json['preferred_servers'] as List<dynamic>? ?? const []),
      capabilities: List<String>.from(json['capabilities'] as List<dynamic>? ?? const []),
      notes: json['notes'] as String,
    );
  }
}

class CodeLocationPolicy {
  final String codeGroup;
  final String githubScope;
  final String pathHint;
  final List<String> owns;
  final String notes;

  const CodeLocationPolicy({
    required this.codeGroup,
    required this.githubScope,
    required this.pathHint,
    required this.owns,
    required this.notes,
  });

  factory CodeLocationPolicy.fromJson(Map<String, dynamic> json) {
    return CodeLocationPolicy(
      codeGroup: json['code_group'] as String,
      githubScope: json['github_scope'] as String,
      pathHint: json['path_hint'] as String,
      owns: List<String>.from(json['owns'] as List<dynamic>? ?? const []),
      notes: json['notes'] as String,
    );
  }
}

class ServerPreset {
  final String name;
  final String provider;
  final String host;
  final int port;
  final String protocol;
  final List<String> capabilities;
  final String notes;

  const ServerPreset({
    required this.name,
    required this.provider,
    required this.host,
    required this.port,
    required this.protocol,
    required this.capabilities,
    required this.notes,
  });

  factory ServerPreset.fromJson(Map<String, dynamic> json) {
    return ServerPreset(
      name: json['name'] as String,
      provider: json['provider'] as String,
      host: json['host'] as String,
      port: json['port'] as int,
      protocol: json['protocol'] as String,
      capabilities: List<String>.from(json['capabilities'] as List<dynamic>? ?? const []),
      notes: json['notes'] as String,
    );
  }
}

class GitStatus {
  final String branch;
  final bool clean;
  final List<String> changes;

  const GitStatus({
    required this.branch,
    required this.clean,
    required this.changes,
  });

  factory GitStatus.fromJson(Map<String, dynamic> json) {
    return GitStatus(
      branch: json['branch'] as String,
      clean: json['clean'] as bool,
      changes: List<String>.from(json['changes'] as List<dynamic>? ?? const []),
    );
  }
}

class LlmTaskResult {
  final String taskId;
  final String status;
  final String assistantMessage;
  final String nextAction;

  const LlmTaskResult({
    required this.taskId,
    required this.status,
    required this.assistantMessage,
    required this.nextAction,
  });

  factory LlmTaskResult.fromJson(Map<String, dynamic> json) {
    return LlmTaskResult(
      taskId: json['task_id'] as String,
      status: json['status'] as String,
      assistantMessage: json['assistant_message'] as String,
      nextAction: json['next_action'] as String,
    );
  }
}

class AdminAgentAction {
  final String key;
  final String title;
  final String risk;
  final String tool;
  final String status;

  const AdminAgentAction({
    required this.key,
    required this.title,
    required this.risk,
    required this.tool,
    required this.status,
  });

  factory AdminAgentAction.fromJson(Map<String, dynamic> json) {
    return AdminAgentAction(
      key: json['key'] as String,
      title: json['title'] as String,
      risk: json['risk'] as String,
      tool: json['tool'] as String,
      status: json['status'] as String,
    );
  }
}

class AdminAgentResult {
  final String taskId;
  final String status;
  final String assistantMessage;
  final String? confirmationToken;
  final String nextAction;
  final List<AdminAgentAction> actions;

  const AdminAgentResult({
    required this.taskId,
    required this.status,
    required this.assistantMessage,
    required this.confirmationToken,
    required this.nextAction,
    required this.actions,
  });

  factory AdminAgentResult.fromJson(Map<String, dynamic> json) {
    return AdminAgentResult(
      taskId: json['task_id'] as String,
      status: json['status'] as String,
      assistantMessage: json['assistant_message'] as String,
      confirmationToken: json['confirmation_token'] as String?,
      nextAction: json['next_action'] as String,
      actions: (json['actions'] as List<dynamic>? ?? const [])
          .map((item) => AdminAgentAction.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }
}

class AdminAgentConfirmResult {
  final String status;
  final String assistantMessage;

  const AdminAgentConfirmResult({
    required this.status,
    required this.assistantMessage,
  });

  factory AdminAgentConfirmResult.fromJson(Map<String, dynamic> json) {
    return AdminAgentConfirmResult(
      status: json['status'] as String,
      assistantMessage: json['assistant_message'] as String,
    );
  }
}

class LoadBalancerApi {
  LoadBalancerApi({String? baseUrl}) : baseUrl = baseUrl ?? ApiConfig.defaultBaseUrl;

  final String baseUrl;

  Future<List<LoadBalancerServer>> fetchServers() async {
    final response = await http.get(Uri.parse('$baseUrl/load-balancer/servers'));
    _ensureOk(response);
    final data = jsonDecode(response.body) as List<dynamic>;
    return data.map((item) => LoadBalancerServer.fromJson(item as Map<String, dynamic>)).toList();
  }

  Future<List<ModulePlacement>> fetchPlacements() async {
    final response = await http.get(Uri.parse('$baseUrl/load-balancer/placements'));
    _ensureOk(response);
    final data = jsonDecode(response.body) as List<dynamic>;
    return data.map((item) => ModulePlacement.fromJson(item as Map<String, dynamic>)).toList();
  }

  Future<RoutingPlan> fetchRoutingPlan(String moduleName) async {
    final response = await http.get(Uri.parse('$baseUrl/load-balancer/routing-plan?module_name=$moduleName'));
    _ensureOk(response);
    return RoutingPlan.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<List<ServerPreset>> fetchFirebasePresets({String projectId = 'your-project-id'}) async {
    final response = await http.get(Uri.parse('$baseUrl/load-balancer/presets/firebase?project_id=$projectId'));
    _ensureOk(response);
    final data = jsonDecode(response.body) as List<dynamic>;
    return data.map((item) => ServerPreset.fromJson(item as Map<String, dynamic>)).toList();
  }

  Future<List<ModuleServerPolicy>> fetchModulePolicies() async {
    final response = await http.get(Uri.parse('$baseUrl/load-balancer/policies'));
    _ensureOk(response);
    final data = jsonDecode(response.body) as List<dynamic>;
    return data.map((item) => ModuleServerPolicy.fromJson(item as Map<String, dynamic>)).toList();
  }

  Future<List<CodeLocationPolicy>> fetchCodeLocationPolicies() async {
    final response = await http.get(Uri.parse('$baseUrl/load-balancer/code-locations'));
    _ensureOk(response);
    final data = jsonDecode(response.body) as List<dynamic>;
    return data.map((item) => CodeLocationPolicy.fromJson(item as Map<String, dynamic>)).toList();
  }

  Future<BrowserAccessManifest> fetchBrowserManifest() async {
    final response = await http.get(Uri.parse('$baseUrl/llm/browser/manifest'));
    _ensureOk(response);
    return BrowserAccessManifest.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<Map<String, dynamic>> openBrowserTarget(String targetKey) async {
    final response = await http.post(Uri.parse('$baseUrl/llm/browser/open/$targetKey'));
    _ensureOk(response);
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<BrowserActionResult> browserNavigate(String url) async {
    final response = await http.post(
      Uri.parse('$baseUrl/llm/browser/navigate'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'url': url}),
    );
    _ensureOk(response);
    return BrowserActionResult.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<BrowserActionResult> browserClick({required String url, required String selector}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/llm/browser/click'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'url': url, 'selector': selector}),
    );
    _ensureOk(response);
    return BrowserActionResult.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<BrowserActionResult> browserType({
    required String url,
    required String selector,
    required String text,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/llm/browser/type'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'url': url, 'selector': selector, 'text': text}),
    );
    _ensureOk(response);
    return BrowserActionResult.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<void> createServer({
    required String name,
    required String host,
    required int port,
    required String protocol,
    required int weight,
    required int maxModules,
    required List<String> capabilities,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/load-balancer/servers'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': name,
        'host': host,
        'port': port,
        'protocol': protocol,
        'weight': weight,
        'max_modules': maxModules,
        'capabilities': capabilities,
      }),
    );
    _ensureOk(response);
  }

  Future<void> createServersFromPresets(List<ServerPreset> presets) async {
    final response = await http.post(
      Uri.parse('$baseUrl/load-balancer/servers/bulk'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'servers': presets
            .map(
              (preset) => {
                'name': preset.name,
                'host': preset.host,
                'port': preset.port,
                'protocol': preset.protocol,
                'weight': 1,
                'max_modules': 20,
                'capabilities': preset.capabilities,
                'notes': preset.notes,
              },
            )
            .toList(),
      }),
    );
    _ensureOk(response);
  }

  Future<void> createPlacement({
    required String moduleName,
    required int serverId,
    required String routePrefix,
    required int priority,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/load-balancer/placements'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'module_name': moduleName,
        'server_id': serverId,
        'route_prefix': routePrefix,
        'priority': priority,
      }),
    );
    _ensureOk(response);
  }

  Future<GitStatus> fetchGitStatus() async {
    final response = await http.get(Uri.parse('$baseUrl/load-balancer/git/status'));
    _ensureOk(response);
    return GitStatus.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<String> autoCommit({required String message, bool push = false}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/load-balancer/git/commit'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'message': message,
        'include_all': true,
        'push': push,
      }),
    );
    _ensureOk(response);
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    return data['output'] as String? ?? data['message'] as String;
  }

  Future<LlmTaskResult> runLlmTask({
    required String taskId,
    required String prompt,
    required Map<String, dynamic> localContext,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/load-balancer/llm/tasks'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'task_id': taskId,
        'prompt': prompt,
        'local_context': localContext,
      }),
    );
    _ensureOk(response);
    return LlmTaskResult.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<AdminAgentResult> runAdminAgentTask({
    required String taskId,
    required String prompt,
    required Map<String, dynamic> localContext,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/llm/browser/agent/tasks'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'task_id': taskId,
        'prompt': prompt,
        'local_context': localContext,
        'auto_execute_safe_actions': true,
      }),
    );
    _ensureOk(response);
    return AdminAgentResult.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<AdminAgentConfirmResult> confirmAdminAgentActions({
    required String confirmationToken,
    required bool approved,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/llm/browser/agent/confirm'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'confirmation_token': confirmationToken,
        'approved': approved,
      }),
    );
    _ensureOk(response);
    return AdminAgentConfirmResult.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  void _ensureOk(http.Response response) {
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception(response.body);
    }
  }
}
