import 'dart:convert';

import 'package:http/http.dart' as http;

import 'api_config.dart';

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

class BrowserAccessApi {
  BrowserAccessApi({String? baseUrl}) : baseUrl = baseUrl ?? ApiConfig.defaultBaseUrl;

  final String baseUrl;

  Future<BrowserAccessManifest> fetchManifest() async {
    final response = await http.get(Uri.parse('$baseUrl/llm/browser/manifest'));
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception(response.body);
    }
    return BrowserAccessManifest.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<Map<String, dynamic>> requestOpen(String targetKey) async {
    final response = await http.post(Uri.parse('$baseUrl/llm/browser/open/$targetKey'));
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception(response.body);
    }
    return jsonDecode(response.body) as Map<String, dynamic>;
  }
}
