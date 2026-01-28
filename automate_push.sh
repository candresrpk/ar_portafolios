#!/bin/bash

echo "📦 Agregando archivos..."
git add .

echo ""
echo "📝 Archivos preparados para commit:"
git status --short

echo ""
read -p "✏️  Escribe tu commit: " commit_message

if [ -z "$commit_message" ]; then
  echo "❌ El mensaje de commit no puede estar vacío."
  exit 1
fi

echo ""
echo "🚀 Haciendo commit..."
git commit -m "$commit_message"

echo ""
echo "📤 Haciendo push..."
git push

echo ""
echo "✅ Commit y push completados con éxito."