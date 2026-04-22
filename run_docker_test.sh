#!/bin/bash
set -e

echo "[+] Destroying old container if exists..."
docker rm -f sdn-test 2>/dev/null || true

echo "[+] Starting Docker container from a Mac-compatible Mininet image..."
# Use an image known to work beautifully on Apple Silicon (ARM64)
docker run -d --rm --privileged --name sdn-test -v $(pwd):/app ghcr.io/scc365/mininet:latest bash -c "service openvswitch-switch start && sleep infinity"
sleep 5

echo "[+] Installing Ryu controller in the container..."
docker exec sdn-test bash -c "pip3 install ryu eventlet==0.30.2 > /dev/null 2>&1 || true"
# Because it's python 3.8 based, ryu installs fine.

echo "[+] Starting Ryu Topology Detector in background..."
docker exec -d sdn-test bash -c "cd /app && ryu-manager --observe-links topology_detector.py > ryu.log 2>&1"
sleep 5

echo "[+] Triggering automated topology Mininet test..."
docker exec sdn-test bash -c "cd /app && python3 auto_test_topo.py"

echo "[+] Test Complete. Extracting Ryu logs from detector:"
echo "=========================================================="
docker exec sdn-test cat /app/ryu.log

echo "=========================================================="
echo "[+] Cleaning up Docker container..."
docker rm -f sdn-test
