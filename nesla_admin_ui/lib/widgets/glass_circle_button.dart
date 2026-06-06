import 'dart:ui';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

/// A circular glassmorphism-style button with hover and press animations.
class GlassCircleButton extends StatefulWidget {
  final Widget child;
  final double size;
  final VoidCallback? onPressed;

  const GlassCircleButton({
    Key? key,
    required this.child,
    this.size = 72,
    this.onPressed,
  }) : super(key: key);

  @override
  State<GlassCircleButton> createState() => _GlassCircleButtonState();
}

class _GlassCircleButtonState extends State<GlassCircleButton>
    with SingleTickerProviderStateMixin {
  bool _hover = false;
  bool _pressed = false;

  Duration get _kDur => const Duration(milliseconds: 180);

  void _onEnter(PointerEvent _) {
    setState(() => _hover = true);
  }

  void _onExit(PointerEvent _) {
    setState(() {
      _hover = false;
      _pressed = false;
    });
  }

  void _onTapDown(TapDownDetails _) {
    setState(() => _pressed = true);
  }

  void _onTapUp(TapUpDetails _) {
    setState(() => _pressed = false);
  }

  void _onTapCancel() {
    setState(() => _pressed = false);
  }

  @override
  Widget build(BuildContext context) {
    final double scale = _pressed ? 0.95 : (_hover ? 1.03 : 1.0);

    return MouseRegion(
      onEnter: _onEnter,
      onExit: _onExit,
      cursor: SystemMouseCursors.click,
      child: GestureDetector(
        onTapDown: _onTapDown,
        onTapUp: _onTapUp,
        onTapCancel: _onTapCancel,
        onTap: widget.onPressed,
        behavior: HitTestBehavior.translucent,
        child: AnimatedScale(
          scale: scale,
          duration: _kDur,
          curve: Curves.easeOutCubic,
          child: SizedBox(
            height: widget.size,
            width: widget.size,
            child: Stack(
              alignment: Alignment.center,
              children: [
                // Frosted glass backdrop
                ClipOval(
                  child: BackdropFilter(
                    filter: ImageFilter.blur(sigmaX: 10.0, sigmaY: 10.0),
                    child: Container(
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.white.withValues(alpha: 0.04),
                        border: Border.all(
                          color: Colors.white.withValues(alpha: 0.08),
                          width: 1.0,
                        ),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withValues(alpha: 0.35),
                            blurRadius: 18,
                            offset: const Offset(0, 6),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),

                // Inner subtle highlight
                ClipOval(
                  child: Container(
                    height: widget.size,
                    width: widget.size,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      gradient: LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [
                          Colors.white.withValues(alpha: 0.02),
                          Colors.white.withValues(alpha: 0.00),
                        ],
                      ),
                    ),
                  ),
                ),

                // Content
                DefaultTextStyle(
                  style: TextStyle(
                    color: Colors.white.withValues(alpha: 0.95),
                    fontSize: widget.size * 0.36,
                    fontWeight: FontWeight.w600,
                    letterSpacing: 0.6,
                  ),
                  child: Center(child: widget.child),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
