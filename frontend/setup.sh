#!/bin/sh

echo "Eneo Frontend\nRunning first setup..."
echo "\nRunning pnpm install..."
pnpm install

echo "\nBuilding dependencies..."

if [ -n "${GITHUB}" ]; then
  echo "Setup for Github actions..."
  pnpm run --recursive --filter @intric/ui... build
  echo "Github setup done."
else
  echo "Build all"
  pnpm run --recursive --filter @intric/ui... build
  echo "\nDone.\n\nStart developing by running 'pnpm -w run dev'"
fi
