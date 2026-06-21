import 'package:cloud_functions/cloud_functions.dart';
import 'package:firebase_core/firebase_core.dart';

class FirebaseSdkBridge {
  bool get isConfigured => Firebase.apps.isNotEmpty;

  FirebaseFunctions? functionsForRegion(String region) {
    if (!isConfigured) return null;
    return FirebaseFunctions.instanceFor(region: region);
  }

  // Add Firebase.initializeApp(options: ...) in main.dart later after you
  // generate real Firebase options for your project.
}

class FirebaseServerCatalog {
  static const regions = [
    'us-central1',
    'us-east1',
    'us-west1',
    'europe-west1',
    'europe-west2',
    'asia-south1',
    'asia-east1',
    'asia-northeast1',
    'australia-southeast1',
    'southamerica-east1',
  ];
}
