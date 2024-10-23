from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Directory to store the generated Terraform files
TERRAFORM_DIR = "./terraform_configs"

# Route to handle requests for infrastructure provisioning
@app.route('/provision', methods=['POST'])
def provision():
    # Get the request data (e.g., instance type, ami, region)
    data = request.json
    instance_type = data.get("instance_type")
    ami = data.get("ami")
    region = data.get("region")
    name = data.get("name")
    
    # Create the Terraform configuration file dynamically
    terraform_config = f"""
    provider "aws" {{
      region = "{region}"
    }}

    resource "aws_instance" "web" {{
      ami           = "{ami}"
      instance_type = "{instance_type}"

      tags = {{
        Name = "{name}"
      }}
    }}
    """

    # Create a directory to store the Terraform configuration
    if not os.path.exists(TERRAFORM_DIR):
        os.makedirs(TERRAFORM_DIR)
    
    config_path = os.path.join(TERRAFORM_DIR, f'{name}_main.tf')

    # Write the configuration to a .tf file
    with open(config_path, 'w') as f:
        f.write(terraform_config)

    # Execute Terraform commands
    terraform_apply = subprocess.run(["terraform", "init", "-input=false"], cwd=TERRAFORM_DIR, capture_output=True)
    
    if terraform_apply.returncode != 0:
        return jsonify({"error": terraform_apply.stderr.decode('utf-8')}), 500

    terraform_apply = subprocess.run(["terraform", "apply", "-auto-approve"], cwd=TERRAFORM_DIR, capture_output=True)

    if terraform_apply.returncode != 0:
        return jsonify({"error": terraform_apply.stderr.decode('utf-8')}), 500

    return jsonify({"message": "Infrastructure provisioned successfully!"})

# Start the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
