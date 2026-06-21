import 'dart:convert';

import 'package:http/http.dart' as http;

import 'api_config.dart';

class AdminEnvConfig {
  final String openrouterApiKey;
  final String openrouterBaseUrl;
  final String openrouterModelIds;
  final String openrouterFallbackModelIds;
  final String openrouterAppName;
  final String openrouterReferer;
  final String openrouterTimeoutSeconds;

  const AdminEnvConfig({
    required this.openrouterApiKey,
    required this.openrouterBaseUrl,
    required this.openrouterModelIds,
    required this.openrouterFallbackModelIds,
    required this.openrouterAppName,
    required this.openrouterReferer,
    required this.openrouterTimeoutSeconds,
  });

  factory AdminEnvConfig.fromJson(Map<String, dynamic> json) {
    return AdminEnvConfig(
      openrouterApiKey: json['OPENROUTER_API_KEY'] as String? ?? '',
      openrouterBaseUrl: json['OPENROUTER_BASE_URL'] as String? ?? '',
      openrouterModelIds: json['OPENROUTER_MODEL_IDS'] as String? ?? '',
      openrouterFallbackModelIds: json['OPENROUTER_FALLBACK_MODEL_IDS'] as String? ?? '',
      openrouterAppName: json['OPENROUTER_APP_NAME'] as String? ?? '',
      openrouterReferer: json['OPENROUTER_REFERER'] as String? ?? '',
      openrouterTimeoutSeconds: json['OPENROUTER_TIMEOUT_SECONDS'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'openrouter_api_key': openrouterApiKey,
      'openrouter_base_url': openrouterBaseUrl,
      'openrouter_model_ids': openrouterModelIds,
      'openrouter_fallback_model_ids': openrouterFallbackModelIds,
      'openrouter_app_name': openrouterAppName,
      'openrouter_referer': openrouterReferer,
      'openrouter_timeout_seconds': openrouterTimeoutSeconds,
    };
  }
}

class AdminApi {
  AdminApi({String? baseUrl}) : baseUrl = baseUrl ?? ApiConfig.defaultBaseUrl;

  final String baseUrl;

  Future<AdminEnvConfig> fetchEnvConfig() async {
    final response = await http.get(Uri.parse('$baseUrl/admin/env'));
    _ensureOk(response);
    return AdminEnvConfig.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<AdminEnvConfig> saveEnvConfig(AdminEnvConfig config) async {
    final response = await http.put(
      Uri.parse('$baseUrl/admin/env'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(config.toJson()),
    );
    _ensureOk(response);
    return AdminEnvConfig.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  void _ensureOk(http.Response response) {
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception(response.body);
    }
  }
}
