import 'package:flutter/material.dart';

class ResponsiveService {
  static bool isMobile(BuildContext context) => MediaQuery.sizeOf(context).width < 720;

  static bool isTablet(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    return width >= 720 && width < 1100;
  }

  static bool isWeb(BuildContext context) => MediaQuery.sizeOf(context).width >= 1100;

  static int getGridColumns(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    if (width < 720) return 1;
    if (width < 1100) return 2;
    return 3;
  }

  static double getResponsivePadding(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    if (width < 720) return 16;
    if (width < 1100) return 20;
    return 28;
  }
}

