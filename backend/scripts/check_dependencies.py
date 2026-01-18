#!/usr/bin/env python3
"""
Script para verificar que todas las dependencias están instaladas
"""

import sys

missing_deps = []

# Check required dependencies
dependencies = [
    ("openai", "openai"),
    ("requests", "requests"),
    ("dotenv", "python-dotenv"),
]

print("🔍 Verificando dependencias...\n")

for module_name, package_name in dependencies:
    try:
        __import__(module_name)
        print(f"✅ {package_name}")
    except ImportError:
        print(f"❌ {package_name} - NO INSTALADO")
        missing_deps.append(package_name)

if missing_deps:
    print(f"\n⚠️  Faltan {len(missing_deps)} dependencia(s)")
    print("\nPara instalar las dependencias:")
    print("   cd /root/personal_page/backend && pip install -r requirements.txt")
    print("\nSi usas Docker:")
    print("   docker-compose exec backend pip install -r requirements.txt")
    sys.exit(1)
else:
    print("\n✅ Todas las dependencias están instaladas")
    sys.exit(0)
