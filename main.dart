
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(OctopusApp());

class OctopusApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Octopus Set Keys',
      theme: ThemeData.dark(),
      home: SetKeysPage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class SetKeysPage extends StatefulWidget {
  @override
  _SetKeysPageState createState() => _SetKeysPageState();
}

class _SetKeysPageState extends State<SetKeysPage> {
  final TextEditingController _apiKeyController = TextEditingController();
  final TextEditingController _apiSecretController = TextEditingController();
  String responseMessage = "";
  bool keysSent = false;

  Future<void> sendKeys() async {
    final uri = Uri.parse('https://octopus-ai-docker.onrender.com/set_keys');

    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: {
        'api_key': _apiKeyController.text.trim(),
        'api_secret': _apiSecretController.text.trim(),
      },
    );

    setState(() {
      if (response.statusCode == 200) {
        responseMessage = "✅ Keys sent successfully: ${response.body}";
        keysSent = true;
      } else {
        responseMessage = "❌ Failed: ${response.statusCode} – ${response.body}";
        keysSent = false;
      }
    });

    print("Response ${response.statusCode}: ${response.body}");
  }

  Future<void> startTrading() async {
    final uri = Uri.parse('https://octopus-ai-docker.onrender.com/trade');

    final response = await http.post(uri);

    setState(() {
      if (response.statusCode == 200) {
        responseMessage = "🚀 Trading started: ${response.body}";
      } else {
        responseMessage = "❌ Could not start trading: ${response.statusCode} – ${response.body}";
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Send Binance API Keys")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            TextField(
              controller: _apiKeyController,
              decoration: InputDecoration(labelText: "API Key"),
            ),
            TextField(
              controller: _apiSecretController,
              decoration: InputDecoration(labelText: "API Secret"),
              obscureText: true,
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: sendKeys,
              child: Text("Send API Keys"),
            ),
            SizedBox(height: 20),
            if (keysSent)
              ElevatedButton(
                onPressed: startTrading,
                style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
                child: Text("Start Trading"),
              ),
            SizedBox(height: 20),
            Text(responseMessage, textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}
