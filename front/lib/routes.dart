import 'package:flutter/material.dart';
import 'package:front/pages/login_page.dart';
import 'package:front/pages/signup_page.dart';
import 'package:front/pages/todo_page.dart';

class Routes {
  static Map<String, Widget Function(BuildContext)> list =
      <String, WidgetBuilder>{
    '/login': (_) =>  LoginPage(),
    '/signup': (_) => SignUpPage(),
    '/todo': (_) => TodoPage(),
  };

  static String initial = '/login';

  static GlobalKey<NavigatorState>? navigatorKey = GlobalKey<NavigatorState>();
}
