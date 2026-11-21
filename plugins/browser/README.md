# sole-browser (optional)

Adds Google's [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) server (Apache-2.0) to Sole, configured for privacy:

| Setting | Why |
|---|---|
| `chrome-devtools-mcp@1.13.0` | Pinned version: tool names in Sole's recipes stay valid; no surprise updates |
| `--isolated` | Temporary browser profile: no access to your saved logins, cookies or history |
| `--headless` | No browser window pops up while Claude works |
| `--no-usage-statistics` | Google's usage statistics are on by default; turned off here |
| `--no-performance-crux` | Performance traces do not send page URLs to Google's CrUX service |

Requires Node.js (LTS) and Google Chrome.

To watch the browser, remove `--headless` from `.mcp.json`. To get real-user CrUX data in traces, remove `--no-performance-crux` (page URLs are then sent to Google).

Do not install Google's own `chrome-devtools-mcp` plugin at the same time; you would get the same tools twice.
