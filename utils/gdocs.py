import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

const agents = [
  {
    id: "sop_gen",
    name: "SOP Generator",
    description: "Creates process documentation for any business operation.",
    modules: ["Doc Builder", "Google Docs Export", "Markdown Preview"]
  },
  {
    id: "client_discovery",
    name: "Lead Finder",
    description: "Finds and qualifies business leads in your target region.",
    modules: ["Google Maps Scanner", "Directory Scraper", "Lead Scoring"]
  },
  {
    id: "deal_closer",
    name: "Deal Closer",
    description: "Automates outreach and closes deals via email and templates.",
    modules: ["Email Templates", "Negotiation Rules", "CRM Logger"]
  }
];

export default function AgentDashboard() {
  const [selectedAgent, setSelectedAgent] = useState("sop_gen");
  const [apiKeys, setApiKeys] = useState({
    openai: "",
    google: "",
    sendgrid: "",
    twilio: ""
  });
  const [preview, setPreview] = useState("Generated SOP preview will appear here.");
  const [logs, setLogs] = useState([
    "[INFO] SOP Generator initialized.",
    "[INFO] Loaded Google Places API successfully.",
    "[INFO] Lead Finder scanned Windsor region."
  ]);
  const [grammarIssues, setGrammarIssues] = useState([]);

  const handleKeyChange = (key, value) => {
    setApiKeys({ ...apiKeys, [key]: value });
  };

  const checkGrammar = async () => {
    const res = await fetch("http://localhost:8010/v2/check", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams({
        text: preview,
        language: "en-US"
      })
    });
    const data = await res.json();
    setGrammarIssues(data.matches || []);
    setLogs((prev) => [...prev, `[INFO] Grammar check returned ${data.matches.length} issues.`]);
  };

  const exportToGoogleDocs = async () => {
    const res = await fetch("http://localhost:8000/api/export-doc", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ sop_text: preview })
    });
    const result = await res.json();
    if (result.url) {
      setLogs((prev) => [...prev, `[SUCCESS] Exported SOP to: ${result.url}`]);
      window.open(result.url, "_blank");
    } else {
      setLogs((prev) => [...prev, `[ERROR] Failed to export SOP.`]);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">🧠 AI Agent Control Center</h1>

      <Tabs value={selectedAgent} onValueChange={setSelectedAgent} className="w-full">
        <TabsList className="grid grid-cols-5 w-full">
          {agents.map((agent) => (
            <TabsTrigger key={agent.id} value={agent.id}>
              {agent.name}
            </TabsTrigger>
          ))}
          <TabsTrigger value="api_keys">API Keys</TabsTrigger>
          <TabsTrigger value="sop_preview">Preview</TabsTrigger>
          <TabsTrigger value="logs">Logs</TabsTrigger>
        </TabsList>

        {agents.map((agent) => (
          <TabsContent key={agent.id} value={agent.id} className="mt-4">
            <Card>
              <CardContent className="space-y-4 p-6">
                <h2 className="text-xl font-semibold">{agent.name}</h2>
                <p className="text-muted-foreground">{agent.description}</p>
                <div className="space-y-2">
                  <h3 className="text-lg font-medium">Modules</h3>
                  <ul className="list-disc list-inside">
                    {agent.modules.map((m) => (
                      <li key={m}>{m}</li>
                    ))}
                  </ul>
                </div>
                <div className="pt-4 space-x-2">
                  <Button variant="default">Launch Agent</Button>
                  <Button variant="secondary">Configure</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        ))}

        <TabsContent value="api_keys" className="mt-4">
          <Card>
            <CardContent className="space-y-4 p-6">
              <h2 className="text-xl font-semibold">🔐 API Key Manager</h2>
              <p className="text-muted-foreground">Paste your API keys for services below:</p>
              {Object.keys(apiKeys).map((key) => (
                <div key={key} className="space-y-1">
                  <Label htmlFor={key}>{key.toUpperCase()} Key</Label>
                  <Input
                    id={key}
                    type="password"
                    placeholder={`Enter ${key.toUpperCase()} API Key`}
                    value={apiKeys[key]}
                    onChange={(e) => handleKeyChange(key, e.target.value)}
                  />
                </div>
              ))}
              <Button variant="default">Save Keys</Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="sop_preview" className="mt-4">
          <Card>
            <CardContent className="space-y-4 p-6">
              <h2 className="text-xl font-semibold">📝 SOP Preview</h2>
              <Textarea
                className="w-full h-64"
                value={preview}
                onChange={(e) => setPreview(e.target.value)}
              />
              <div className="space-x-2">
                <Button variant="default" onClick={exportToGoogleDocs}>Export to Google Docs</Button>
                <Button variant="secondary" onClick={checkGrammar}>Check Grammar</Button>
              </div>
              {grammarIssues.length > 0 && (
                <div className="mt-4 text-sm text-yellow-600">
                  <h3 className="font-semibold">Grammar Suggestions:</h3>
                  <ul className="list-disc ml-4">
                    {grammarIssues.map((issue, i) => (
                      <li key={i}>{issue.message} (at position {issue.offset})</li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="logs" className="mt-4">
          <Card>
            <CardContent className="space-y-4 p-6">
              <h2 className="text-xl font-semibold">📊 Agent Logs</h2>
              <div className="bg-black text-green-400 font-mono p-4 rounded-md h-64 overflow-y-scroll">
                {logs.map((log, idx) => (
                  <div key={idx}>{log}</div>
                ))}
              </div>
              <Button variant="secondary" onClick={() => setLogs([])}>Clear Logs</Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
