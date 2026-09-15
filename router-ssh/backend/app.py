from flask import Flask, request, jsonify
import paramiko
import time

app = Flask(__name__)


# ==========================================
# Execute Cisco Router Command
# ==========================================
@app.route("/api/execute", methods=["POST"])
def execute_command():

    data = request.get_json()

    router_ip = data.get("router_ip")
    command = data.get("command")

    # Check input
    if not router_ip:
        return jsonify({
            "success": False,
            "error": "Router IP is required."
        }), 400

    if not command:
        return jsonify({
            "success": False,
            "error": "Router command is required."
        }), 400

    # Cisco router login
    username = "admin"
    password = "cisco"

    client = paramiko.SSHClient()

    # Automatically accept SSH host key
    client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    )

    try:

        print(f"Connecting to {router_ip}...")

        # SSH connection
        client.connect(
            hostname=router_ip,
            username=username,
            password=password,
            look_for_keys=False,
            allow_agent=False,
            timeout=10
        )

        print("SSH connected.")

        # Create interactive shell
        shell = client.invoke_shell()

        time.sleep(1)

        # Clear initial router output
        if shell.recv_ready():
            shell.recv(65535)

        # Send command
        print(f"Executing command: {command}")

        shell.send(command + "\n")

        time.sleep(2)

        # Receive output
        output = ""

        while shell.recv_ready():

            output += shell.recv(65535).decode(
                "utf-8",
                errors="ignore"
            )

            time.sleep(0.2)

        print("Command completed.")

        return jsonify({
            "success": True,
            "output": output
        })

    except paramiko.AuthenticationException:

        return jsonify({
            "success": False,
            "error": "Authentication failed. Please check username and password."
        }), 401

    except paramiko.SSHException as e:

        return jsonify({
            "success": False,
            "error": f"SSH error: {str(e)}"
        }), 500

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        client.close()

        print("SSH connection closed.")


# ==========================================
# Health Check
# ==========================================
@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "success": True,
        "message": "Backend is running."
    })


# ==========================================
# Start Flask Server
# ==========================================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
