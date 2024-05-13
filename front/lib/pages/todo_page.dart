import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MaterialApp(
    home: TodoPage(),
  ));
}

class TodoPage extends StatefulWidget {
  @override
  _TodoListPageState createState() => _TodoListPageState();
}

class _TodoListPageState extends State<TodoPage> {
  List<Map<String, dynamic>> _todoItems = [];

  @override
  void initState() {
    super.initState();
    _fetchTodoList();
  }

  Future<void> _fetchTodoList() async {
    final url = Uri.parse('http://localhost:5000/tasks');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as List;
      _todoItems = data.map((item) => item as Map<String, dynamic>).toList();
      setState(() {});
    } else {
      // Tratar erro ao buscar a lista de tarefas
      print('Erro ao buscar lista de tarefas');
    }
  }

  Future<void> _addTodoItem(String task) async {
    final url = Uri.parse('http://localhost:5000/tasks');
    final response = await http.post(
      url,
      body: jsonEncode({'task': task}),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      _todoItems.add(data);
      setState(() {});
    } else {
      // Tratar erro ao adicionar tarefa
      print('Erro ao adicionar tarefa');
    }
  }

  Future<void> _deleteTodoItem(int id) async {
    final url = Uri.parse('http://localhost:5000/tasks/$id');
    final response = await http.delete(url);

    if (response.statusCode == 204) {
      _todoItems.removeWhere((item) => item['id'] == id);
      setState(() {});
    } else {
      // Tratar erro ao deletar tarefa
      print('Erro ao deletar tarefa');
    }
  }

  Widget _buildTodoList() {
    return ListView.builder(
      itemCount: _todoItems.length,
      itemBuilder: (BuildContext context, int index) {
        final task = _todoItems[index];
        return ListTile(
          title: Text(task['task']),
          trailing: IconButton(
            icon: Icon(Icons.delete),
            onPressed: () {
              _deleteTodoItem(task['id']);
            },
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Lista de Tarefas'),
      ),
      body: Column(
        children: <Widget>[
          TextField(
            onSubmitted: (String task) async {
              await _addTodoItem(task);
            },
            decoration: InputDecoration(
              hintText: 'Digite uma tarefa...',
              contentPadding: EdgeInsets.all(16.0),
            ),
          ),
          SizedBox(height: 12.0),
          ElevatedButton(
            onPressed: () {
              // Implementar a lógica para adicionar a tarefa
            },
            child: Text('Adicionar Tarefa'),
          ),
          SizedBox(height: 16.0),
          Expanded(
            child: _buildTodoList(),
          ),
        ],
      ),
    );
  }
}
