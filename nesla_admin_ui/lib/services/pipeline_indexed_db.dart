import 'package:idb_shim/idb_browser.dart';

class PipelineMessage {
  final String id;
  final String role;
  final String text;
  final DateTime createdAt;

  const PipelineMessage({
    required this.id,
    required this.role,
    required this.text,
    required this.createdAt,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'role': role,
      'text': text,
      'createdAt': createdAt.toIso8601String(),
    };
  }

  factory PipelineMessage.fromJson(Map<String, dynamic> json) {
    return PipelineMessage(
      id: json['id'] as String,
      role: json['role'] as String,
      text: json['text'] as String,
      createdAt: DateTime.parse(json['createdAt'] as String),
    );
  }
}

class PipelineIndexedDb {
  static const _dbName = 'nesla_llm_pipeline';
  static const _messagesStore = 'messages';
  static const _contextStore = 'context';

  IdbFactory get _factory => getIdbFactory()!;

  Future<Database> _open() {
    return _factory.open(
      _dbName,
      version: 1,
      onUpgradeNeeded: (event) {
        final db = event.database;
        if (!db.objectStoreNames.contains(_messagesStore)) {
          db.createObjectStore(_messagesStore, keyPath: 'id');
        }
        if (!db.objectStoreNames.contains(_contextStore)) {
          db.createObjectStore(_contextStore, keyPath: 'key');
        }
      },
    );
  }

  Future<List<PipelineMessage>> readMessages() async {
    final db = await _open();
    final tx = db.transaction(_messagesStore, idbModeReadOnly);
    final store = tx.objectStore(_messagesStore);
    final rows = await store.getAll();
    await tx.completed;
    db.close();
    return rows
        .whereType<Map>()
        .map((row) => PipelineMessage.fromJson(Map<String, dynamic>.from(row)))
        .toList()
      ..sort((a, b) => a.createdAt.compareTo(b.createdAt));
  }

  Future<void> addMessage(PipelineMessage message) async {
    final db = await _open();
    final tx = db.transaction(_messagesStore, idbModeReadWrite);
    await tx.objectStore(_messagesStore).put(message.toJson());
    await tx.completed;
    db.close();
  }

  Future<Map<String, dynamic>> readLocalContext() async {
    final db = await _open();
    final tx = db.transaction(_contextStore, idbModeReadOnly);
    final rows = await tx.objectStore(_contextStore).getAll();
    await tx.completed;
    db.close();
    final context = <String, dynamic>{};
    for (final row in rows.whereType<Map>()) {
      final data = Map<String, dynamic>.from(row);
      context[data['key'] as String] = data['value'];
    }
    return context;
  }

  Future<void> writeContextValue(String key, Object? value) async {
    final db = await _open();
    final tx = db.transaction(_contextStore, idbModeReadWrite);
    await tx.objectStore(_contextStore).put({'key': key, 'value': value});
    await tx.completed;
    db.close();
  }
}
