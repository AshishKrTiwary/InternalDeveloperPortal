const express = require('express');
const fs = require('fs');
const { exec } = require('child_process');
const path = require('path');

const app = express();
app.use(express.json());

const TERRAFORM_DIR = path.join(__dirname, 'terraform_configs');

// Route to handle infrastructure provisioning
app.post('/provision', (req, res) => {
    const { instance_type, ami, region, name } = req.body;

    // Create the Terraform configuration dynamically
    const terraformConfig = `
    provider "aws" {
      region = "${region}"
    }

    resource "aws_instance" "web" {
      ami           = "${ami}"
      instance_type = "${instance_type}"

      tags = {
        Name = "${name}"
      }
    }
    `;

    // Create the directory if it doesn't exist
    if (!fs.existsSync(TERRAFORM_DIR)) {
        fs.mkdirSync(TERRAFORM_DIR);
    }

    const configPath = path.join(TERRAFORM_DIR, `${name}_main.tf`);

    // Write the configuration to a .tf file
    fs.writeFileSync(configPath, terraformConfig);

    // Run Terraform commands (init and apply)
    exec(`terraform init -input=false && terraform apply -auto-approve`, { cwd: TERRAFORM_DIR }, (err, stdout, stderr) => {
        if (err) {
            console.error(`Error applying Terraform: ${stderr}`);
            return res.status(500).json({ error: stderr });
        }
        res.json({ message: "Infrastructure provisioned successfully!", output: stdout });
    });
});

// Start the Express server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
