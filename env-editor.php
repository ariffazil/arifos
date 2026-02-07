<?php
/**
 * arifOS Simple .env Editor
 * Upload to your VPS via Hostinger File Manager
 * Visit: http://your-vps-ip/env-editor.php
 */

$envFile = '/opt/openclaw/.env';
$dir = dirname($envFile);

// Create directory if not exists
if (!is_dir($dir)) {
    mkdir($dir, 0755, true);
}

$message = '';
$content = '';

// Handle save
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['env_content'])) {
    $content = $_POST['env_content'];
    if (file_put_contents($envFile, $content) !== false) {
        chmod($envFile, 0600);
        $message = '<div style="background:#10b981;color:white;padding:10px;margin-bottom:15px;border-radius:5px;">✅ Saved to ' . $envFile . '</div>';
    } else {
        $message = '<div style="background:#ef4444;color:white;padding:10px;margin-bottom:15px;border-radius:5px;">❌ Failed to save. Check permissions.</div>';
    }
}

// Load existing
if (file_exists($envFile)) {
    $content = file_get_contents($envFile);
}

?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>arifOS .env Editor</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; background: #0f0f0f; color: #e0e0e0; }
        h1 { color: #10b981; border-bottom: 2px solid #10b981; padding-bottom: 10px; }
        .box { background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 20px; margin: 20px 0; }
        textarea { width: 100%; height: 400px; background: #0a0a0a; color: #00ff88; border: 1px solid #333; padding: 15px; font-family: monospace; font-size: 14px; border-radius: 5px; }
        button { background: #10b981; color: white; border: none; padding: 15px 30px; font-size: 16px; border-radius: 5px; cursor: pointer; }
        button:hover { background: #059669; }
        .note { color: #888; font-size: 14px; margin-top: 10px; }
        code { background: #333; padding: 2px 6px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>🜏 arifOS .env Editor</h1>
    
    <?php echo $message; ?>
    
    <div class="box">
        <p><strong>File:</strong> <code><?php echo $envFile; ?></code></p>
        
        <form method="POST">
            <textarea name="env_content" placeholder="# Paste your API keys here
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
BRAVE_API_KEY=...
BROWSERBASE_API_KEY=...
DATABASE_URL=...
GITHUB_TOKEN=...
"><?php echo htmlspecialchars($content); ?></textarea>
            
            <p class="note">Format: KEY=value (one per line)</p>
            
            <button type="submit">💾 SAVE .ENV FILE</button>
        </form>
    </div>
    
    <div class="box">
        <h3>How to use:</h3>
        <ol>
            <li>Paste all your API keys in the box above (format: KEY=value)</li>
            <li>Click SAVE</li>
            <li>Done. File saved with secure permissions (600).</li>
        </ol>
        <p class="note">After saving, delete this file (env-editor.php) for security.</p>
    </div>
</body>
</html>
