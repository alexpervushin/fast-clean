#!/bin/bash

set -e

generate_lock() {
  local service_dir=$1
  echo "--- Generating lock file for $service_dir ---"
  if [ -d "$service_dir" ]; then
    original_dir=$(pwd)
    cd "$service_dir"
    echo "Changed directory to $(pwd)"
    if uv lock; then
      echo "Successfully generated uv.lock in $service_dir"
    else
      echo "ERROR: Failed to generate uv.lock in $service_dir"
      cd "$original_dir"
      exit 1
    fi
    cd "$original_dir"
    echo "Returned to $(pwd)"
  else
    echo "ERROR: Directory $service_dir not found."
    exit 1
  fi
  echo "-------------------------------------------"
  echo ""
}

generate_lock "microservices/users"
generate_lock "microservices/settings"

echo "All lock files generated successfully."
exit 0