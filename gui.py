import gradio as gr
import socket
from protocol import build_protocol_message

custom_css = """
.gradio-container {
    --primary-color: #ff9a3c;
    --secondary-color: #ff6b6b;
    --accent-color: #4ecdc4;
    --bg-primary: #f8f9fa;
    --bg-secondary: #ffffff;
    --text-primary: #2c3e50;
    --text-muted: #7f8c8d;
}

.gradio-container {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: 'Segoe UI', system-ui, sans-serif;
    border-radius: 1.5rem;
    padding: 2rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

h1 {
    color: var(--primary-color);
    text-align: center;
    font-size: 2.5rem;
    font-weight: 500;
    margin-bottom: 2.5rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.05);
}

#connect-btn, #disconnect-btn {
    padding: 1rem 2rem;
    border-radius: 2rem;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
    font-size: 1.1rem;
    width: 100%;
    max-width: 200px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

#connect-btn {
    background-color: var(--secondary-color);
    color: var(--bg-primary);
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
}

#disconnect-btn {
    background-color: var(--primary-color);
    color: var(--bg-primary);
    box-shadow: 0 4px 15px rgba(255, 154, 60, 0.3);
}

#connect-btn:hover, #disconnect-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

#get-time-btn, #get-name-btn, #get-rand-btn {
    background-color: var(--accent-color);
    color: var(--bg-primary);
    padding: 0.75rem 1.5rem;
    border-radius: 1.25rem;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
    margin: 0.5rem 0;
    box-shadow: 0 2px 8px rgba(78, 205, 196, 0.2);
}

#get-time-btn:hover, #get-name-btn:hover, #get-rand-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);
}

input, textarea {
    background-color: var(--bg-secondary);
    border: 2px solid var(--text-muted);
    color: var(--text-primary);
    padding: 1rem;
    border-radius: 1.25rem;
    font-size: 1rem;
    transition: all 0.3s ease;
    width: 100%;
}

input:focus, textarea:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(255, 154, 60, 0.2);
}

#communication-history {
    background-color: var(--bg-secondary);
    border: 2px solid var(--text-muted);
    padding: 1.5rem;
    border-radius: 1.25rem;
    color: var(--text-primary);
    margin-top: 1.5rem;
    overflow-y: auto;
    max-height: 300px;
}

/* Add subtle animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.gradio-container {
    animation: fadeIn 0.5s ease-out;
}

/* Responsive design */
@media (max-width: 768px) {
    .gradio-container {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    #connect-btn, #disconnect-btn {
        max-width: 100%;
        margin-bottom: 1rem;
    }
    
    #get-time-btn, #get-name-btn, #get-rand-btn {
        width: 100%;
        margin: 0.5rem 0;
    }
}
"""


class ClientGUI:
    def __init__(self):
        """Initialize our friendly client with a warm welcome!"""
        self.client_socket = None
        self.connected = False
        self.history = []
        print("👋 Welcome to the WIESNER server communication client!")

    def connect_to_server(self):
        """Try to connect to our server friend! ✨"""
        try:
            self.client_socket = socket.socket()
            self.client_socket.connect(('127.0.0.1', 1234))
            self.connected = True
            return "🎉 Successfully connected to server! ✅"
        except Exception as e:
            return f"😕 Oops! Connection failed: {str(e)} ❌"

    def disconnect(self):
        """Say goodbye to our server friend! 👋"""
        if self.client_socket:
            self.client_socket.close()
            self.connected = False
            return "👋 Disconnected from server! 🔴"
        return "Not connected."

    def send_command(self, command):
        """Send a message to our server friend! 📨"""
        if not self.connected:
            return "😕 Not connected to server!", self.history
        
        if command in ['T', 'N', 'R']:
            try:
                protocol_message = build_protocol_message(command)
                self.client_socket.send(protocol_message.encode('utf-8'))
                
                response_length = self.client_socket.recv(2).decode('utf-8')
                length = int(response_length)
                response_message = self.client_socket.recv(length).decode('utf-8')
                
                full_response = f"Response ({length}): {response_message}"
                self.history.append(f"> {command}\n< {full_response}")
                return full_response, "\n".join(self.history)
            except Exception as e:
                return f"😕 Oops! Error sending command: {str(e)}", self.history
        return "😕 Incorrect input value", self.history

def create_gui():
    """Create a friendly interface for our server communication! 🌟"""
    client = ClientGUI()
    
    with gr.Blocks(css=custom_css) as gui:
        # Header section
        gr.Markdown("<h1>🌟 Welcome to our Server Communication Friend! 🌟</h1>")
        
        # Connection controls
        with gr.Row():
            connect_btn = gr.Button("🤗 Connect", elem_id="connect-btn")
            disconnect_btn = gr.Button("👋 Disconnect", elem_id="disconnect-btn")
            connection_status = gr.Textbox(label="Status", interactive=False)
        
        # Command buttons
        with gr.Row():
            get_time_btn = gr.Button("⏰ Time", elem_id="get-time-btn")
            get_name_btn = gr.Button("👤 Name", elem_id="get-name-btn")
            get_rand_btn = gr.Button("🎲 Random", elem_id="get-rand-btn")
        
        # Output section
        response_output = gr.Textbox(label="Response", interactive=False)
        history_output = gr.Textbox(label="Chat History", interactive=False, lines=10)
        
        # Event handlers
        connect_btn.click(client.connect_to_server, outputs=[connection_status])
        disconnect_btn.click(client.disconnect, outputs=[connection_status])
        
        get_time_btn.click(
            lambda: "T",
            inputs=[],
            outputs=[response_output]
        ).then(
            client.send_command,
            inputs=[response_output],
            outputs=[response_output, history_output]
        )
        
        get_name_btn.click(
            lambda: "N",
            inputs=[],
            outputs=[response_output]
        ).then(
            client.send_command,
            inputs=[response_output],
            outputs=[response_output, history_output]
        )
        
        get_rand_btn.click(
            lambda: "R",
            inputs=[],
            outputs=[response_output]
        ).then(
            client.send_command,
            inputs=[response_output],
            outputs=[response_output, history_output]
        )
    
    return gui

if __name__ == "__main__":
    my_screen = create_gui()
    my_screen.launch(share=True)