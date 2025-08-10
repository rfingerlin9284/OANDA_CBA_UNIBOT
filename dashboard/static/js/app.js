const socket = io();
const terminal = document.getElementById("terminal");

// Socket event handlers
socket.on("terminal_output", function(msg) {
  const pre = document.createElement("pre");
  pre.textContent = msg.data;
  terminal.appendChild(pre);
  terminal.scrollTop = terminal.scrollHeight;
});

socket.on("trading_update", function(msg) {
  const div = document.createElement("div");
  div.className = "trade-entry";
  div.innerHTML = `
    <span class="timestamp">${new Date().toLocaleTimeString()}</span>
    <span class="pair">${msg.pair}</span>
    <span class="status ${msg.status}">${msg.status.toUpperCase()}</span>
    <span class="pnl ${msg.pnl >= 0 ? 'profit' : 'loss'}">$${msg.pnl.toFixed(2)}</span>
  `;
  terminal.insertBefore(div, terminal.firstChild);
  
  // Keep only last 50 entries
  while (terminal.children.length > 50) {
    terminal.removeChild(terminal.lastChild);
  }
  
  // Update stats
  updateStats();
});

// Update statistics
function updateStats() {
  fetch('/api/stats')
    .then(response => response.json())
    .then(data => {
      document.getElementById('total-trades').textContent = data.total_trades || '-';
      document.getElementById('total-pnl').textContent = '$' + (data.total_pnl || '-');
      document.getElementById('avg-pnl').textContent = '$' + (data.avg_pnl || '-');
      
      const statusElement = document.getElementById('bot-status');
      statusElement.textContent = data.bot_status || 'UNKNOWN';
      statusElement.className = 'status ' + (data.bot_status === 'RUNNING' ? 'running' : 'stopped');
    })
    .catch(error => {
      console.error('Error fetching stats:', error);
    });
}

// Initial load and periodic updates
updateStats();
setInterval(updateStats, 10000); // Update every 10 seconds
