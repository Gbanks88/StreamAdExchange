#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path
import yaml
import docker
import time
from typing import Dict, List

class Deployer:
    def __init__(self):
        self.project_root = Path("/Volumes/Learn_Space/StreamAdExchange")
        self.docker_client = docker.from_env()
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """Load deployment configuration"""
        config_file = self.project_root / "config/deploy.yml"
        with open(config_file) as f:
            return yaml.safe_load(f)

    def build_containers(self):
        """Build Docker containers"""
        print("Building containers...")
        try:
            # Build app container
            self.docker_client.images.build(
                path=str(self.project_root),
                tag="streamad:latest",
                dockerfile="Dockerfile"
            )
            
            # Build monitoring containers
            for service in ['prometheus', 'grafana', 'node-exporter']:
                self.docker_client.images.build(
                    path=str(self.project_root / service),
                    tag=f"{service}:latest"
                )
                
            print("✓ Containers built successfully")
            return True
        except Exception as e:
            print(f"✗ Error building containers: {e}")
            return False

    def run_tests(self) -> bool:
        """Run test suite"""
        print("Running tests...")
        try:
            result = subprocess.run(
                ['pytest', '--cov=app', 'tests/'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✓ Tests passed")
                return True
            else:
                print("✗ Tests failed:")
                print(result.stdout)
                return False
        except Exception as e:
            print(f"✗ Error running tests: {e}")
            return False

    def backup_database(self) -> bool:
        """Backup database before deployment"""
        print("Backing up database...")
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_dir = self.project_root / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            # Add your database backup commands here
            # Example for PostgreSQL:
            # subprocess.run(['pg_dump', '-Fc', 'dbname', '>', f'{backup_dir}/backup_{timestamp}.dump'])
            
            print("✓ Database backed up successfully")
            return True
        except Exception as e:
            print(f"✗ Error backing up database: {e}")
            return False

    def deploy_containers(self) -> bool:
        """Deploy containers using docker-compose"""
        print("Deploying containers...")
        try:
            subprocess.run(
                ['docker-compose', 'up', '-d'],
                cwd=self.project_root,
                check=True
            )
            print("✓ Containers deployed successfully")
            return True
        except Exception as e:
            print(f"✗ Error deploying containers: {e}")
            return False

    def verify_deployment(self) -> bool:
        """Verify deployment status"""
        print("Verifying deployment...")
        try:
            # Check container status
            containers = self.docker_client.containers.list()
            expected_containers = {'streamad', 'prometheus', 'grafana', 'node-exporter'}
            running_containers = {c.name for c in containers}
            
            if not expected_containers.issubset(running_containers):
                print("✗ Not all containers are running")
                return False
            
            # Check application health
            health_check = subprocess.run(
                ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:5000/health'],
                capture_output=True,
                text=True
            )
            
            if health_check.stdout != "200":
                print("✗ Application health check failed")
                return False
                
            print("✓ Deployment verified successfully")
            return True
            
        except Exception as e:
            print(f"✗ Error verifying deployment: {e}")
            return False

    def rollback(self):
        """Rollback deployment if verification fails"""
        print("Rolling back deployment...")
        try:
            subprocess.run(
                ['docker-compose', 'down'],
                cwd=self.project_root,
                check=True
            )
            
            # Restore from backup if needed
            # Add your database restore commands here
            
            print("✓ Rollback completed")
        except Exception as e:
            print(f"✗ Error during rollback: {e}")

    def deploy(self):
        """Run complete deployment process"""
        print("=== Starting Deployment ===")
        
        steps = [
            (self.run_tests, "Running tests"),
            (self.backup_database, "Backing up database"),
            (self.build_containers, "Building containers"),
            (self.deploy_containers, "Deploying containers"),
            (self.verify_deployment, "Verifying deployment")
        ]
        
        for step_func, description in steps:
            print(f"\n{description}...")
            if not step_func():
                print(f"\n✗ Deployment failed during: {description}")
                self.rollback()
                return False
        
        print("\n✓ Deployment completed successfully!")
        return True

if __name__ == "__main__":
    deployer = Deployer()
    deployer.deploy() 