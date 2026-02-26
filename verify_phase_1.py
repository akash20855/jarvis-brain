#!/usr/bin/env python3
"""
Jarvis Phase 1 - Post-Build Verification Script
Verify all Phase 1 components are in place and ready
"""

import os
import sys
from pathlib import Path

def check_file(path, description):
    """Check if a file exists"""
    exists = Path(path).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_directory(path, description):
    """Check if a directory exists"""
    exists = Path(path).is_dir()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def main():
    print("=" * 60)
    print("JARVIS PHASE 1 - BUILD VERIFICATION")
    print("=" * 60)
    print()

    all_ok = True

    # Check core database files
    print("📦 Database Layer:")
    all_ok &= check_file("database/schema.sql", "SQL Schema")
    all_ok &= check_file("database/init_db.py", "Database Init Script")
    all_ok &= check_file("core/database.py", "Database Manager")
    all_ok &= check_file("core/models.py", "ORM Models")
    print()

    # Check backend files
    print("🔌 Backend API:")
    all_ok &= check_file("backend/routes_persistence.py", "Persistence API Routes")
    all_ok &= check_file("backend/app.py", "Flask App")
    all_ok &= check_directory("backend", "Backend Directory")
    print()

    # Check dashboard files
    print("🎨 React Dashboard:")
    all_ok &= check_directory("dashboard", "Dashboard Directory")
    all_ok &= check_file("dashboard/package.json", "Package.json")
    all_ok &= check_file("dashboard/vite.config.js", "Vite Config")
    all_ok &= check_file("dashboard/index.html", "HTML Entry")
    all_ok &= check_directory("dashboard/src", "Source Directory")
    all_ok &= check_file("dashboard/src/App.jsx", "Main App Component")
    all_ok &= check_file("dashboard/src/main.jsx", "Entry Point")
    all_ok &= check_file("dashboard/src/index.css", "Global Styles")
    all_ok &= check_directory("dashboard/src/components", "Components")
    all_ok &= check_directory("dashboard/src/pages", "Pages")
    all_ok &= check_directory("dashboard/src/services", "Services")
    all_ok &= check_directory("dashboard/src/store", "Store")
    print()

    # Check configuration
    print("⚙️  Configuration:")
    all_ok &= check_file("docker-compose.yml", "Docker Compose")
    all_ok &= check_file("setup-database.sh", "Setup Script")
    all_ok &= check_file(".env.example", "Environment Example")
    all_ok &= check_file("requirements.txt", "Python Requirements")
    print()

    # Check documentation
    print("📚 Documentation:")
    all_ok &= check_file("PHASE_1_DATABASE.md", "Database Documentation")
    all_ok &= check_file("PHASE_1_COMPLETE.md", "Completion Summary")
    all_ok &= check_file("PHASE_1_STATUS.md", "Status Report")
    all_ok &= check_file("PHASE_1_QUICKSTART.sh", "Quick Start Guide")
    all_ok &= check_file("dashboard/README.md", "Dashboard README")
    print()

    # Summary
    print("=" * 60)
    if all_ok:
        print("✅ ALL PHASE 1 COMPONENTS VERIFIED!")
        print()
        print("🚀 NEXT STEPS:")
        print()
        print("1. Copy .env.example to .env:")
        print("   $ cp .env.example .env")
        print()
        print("2. Choose startup method:")
        print("   A) Docker (recommended):")
        print("      $ docker-compose up -d")
        print()
        print("   B) Automated (macOS):")
        print("      $ chmod +x setup-database.sh")
        print("      $ ./setup-database.sh")
        print()
        print("   C) Manual:")
        print("      $ pip install -r requirements.txt")
        print("      $ python3 database/init_db.py")
        print("      $ python3 backend/app.py")
        print("      (In another terminal)")
        print("      $ cd dashboard && npm install && npm run dev")
        print()
        print("3. Access the system:")
        print("   Dashboard: http://localhost:3000")
        print("   Backend:   http://localhost:8001")
        print("   Database:  pg_isready -h localhost")
        print()
        print("4. Verify everything works:")
        print("   curl http://localhost:8001/api/persistence/health")
        print()
        print("5. Read the documentation:")
        print("   - PHASE_1_DATABASE.md (detailed guide)")
        print("   - PHASE_1_COMPLETE.md (what was built)")
        print("   - dashboard/README.md (frontend guide)")
        print()
        return 0
    else:
        print("❌ SOME COMPONENTS ARE MISSING!")
        print()
        print("Please check the output above and ensure all files")
        print("and directories are present in the repository.")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
